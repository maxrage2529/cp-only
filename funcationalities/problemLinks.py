
import json
import random
import requests
import pandas as pd
import time

import os

# python -m venv folder_name
# venv\Scripts\activate
# pip install pandas requests flask gunicorn
# pip freeze > requirements.txt
# git init

# git add .
# git commit -m "message"
# git push

# heroku cli install
# echo "web: gunicorn app:app" > Procfile
# Create application inside heroku dashboard
# git remote add origin ssh_link/htt_link
# git branch -M main


class problems:
    dirname = os.path.dirname(__file__)

    def __init__(self, forceReload):
        if not os.path.exists(os.path.join(self.dirname, "database")):
            print("Creating new db directory")
            os.mkdir(os.path.join(self.dirname, "database"))
        start = time.time()
        filename = os.path.join(self.dirname, "database\problemCounts_df.csv")
        print(filename)
        if (not os.path.exists(filename)):
            pd.DataFrame({"username": [], "count": []}
                         ).to_csv(filename, index=False)
        self.problemCounts_df = pd.read_csv(filename)
        filename = os.path.join(self.dirname, 'database\mainProblems_df.csv')
        if ((not os.path.exists(filename)) or forceReload):
            self.refresh()
        self.allProblems_df = pd.read_csv(filename)
        print(f"{time.time() - start} initialisation compteted")

    def refresh(self):
        try:
            start = time.time()
            filename = os.path.join(
                self.dirname, 'database\mainProblems_df.csv')
            problemset_problems = json.loads(requests.get(
                "https://codeforces.com/api/problemset.problems").text)
            mainProblems = problemset_problems["result"]["problems"]
            mainProblems_df = pd.DataFrame(mainProblems)
            mainProblems_df.drop(
                ["name", "type", "points"], axis=1, inplace=True)

            mainProblems_df.to_csv(filename, index=False)

            print(f"{time.time() - start} refresh completed")
        except:
            self.refresh()

    def getUserProblemsFunction(self, user, startFrom=1, count=100000):
        try:
            # time is directly proportional to count
            # print(user,startFrom,count)
            # print("https://codeforces.com/api/user.status?handle="+user+"&from="+str(startFrom)+"&count="+str(count))
            start = time.time()
            res = requests.get(
                "https://codeforces.com/api/user.status?handle="+user+"&from="+str(startFrom)+"&count="+str(count))
            # print(res.text[:5])
            # print(res.status_code)
            # if time starts from here total time will be near to 0.04
            self.user_status = json.loads(res.text)
        except:
            self.getUserProblemsFunction(user, startFrom, count)
        if (self.user_status["status"] == "FAILED" or len(self.user_status["result"]) == 0):
            return pd.DataFrame([])
        temp_userProblems = self.user_status["result"]
        temp_userProblems_df = pd.DataFrame(temp_userProblems)

        # here verdict has been ignored all problems has been included irrespective of result whether accpeted or not
        userProblems_df = pd.DataFrame(
            temp_userProblems_df["problem"].to_dict())
        userProblems_df = userProblems_df.transpose()

        newCount = userProblems_df.shape[0]

        if (startFrom == 1):
            # self.problemCounts_df=self.problemCounts_df.append([{"username":user,"count":newCount}],ignore_index=True)
            print(self.problemCounts_df)
            if (self.problemCounts_df.loc[self.problemCounts_df["username"] == user, "count"].shape[0] > 0):
                self.problemCounts_df.loc[self.problemCounts_df["username"]
                                          == user, "count"] += newCount-1
            else:
                self.problemCounts_df = pd.concat([self.problemCounts_df, pd.DataFrame(
                    [{"username": user, "count": newCount}])], ignore_index=True)

        filename = os.path.join(self.dirname, "database\problemCounts_df.csv")
        self.problemCounts_df.to_csv(filename, index=False)
        # userProblems_df.drop(["name", "type", "points"], axis=1, inplace=True)
        userProblems_df = userProblems_df[[
            "contestId", "index", "rating", "tags"]]
        userProblems_df.drop_duplicates(
            subset=["contestId", "index"], inplace=True)
        print(f"{time.time() - start} s in getUserProblemsFunction")
        return userProblems_df

    def mergeUserProblems(self, user):
        # try:
        filename = os.path.join(self.dirname, f"database\{user}.csv")
        print(os.path.exists(filename))
        if (not os.path.exists(filename)):
            try:
                self.getUserProblemsFunction(
                    user).to_csv(filename, index=False)
            except:
                self.getUserProblemsFunction(
                    user).to_csv(filename, index=False)
        else:
            print(user)
            print(
                self.problemCounts_df.loc[self.problemCounts_df.username == user])
            totalSize = self.problemCounts_df.loc[self.problemCounts_df.username ==
                                                  user]["count"].iloc[0]
            # print(totalSize)
            count = self.getUserProblemsFunction(user, totalSize+1).shape[0]
            print(totalSize, count)
            if (count > 0):
                filename = os.path.join(os.path.dirname(
                    __file__), f"database\{user}.csv")
                tempUser_df = pd.read_csv(filename)
                newSolvedProblems = self.getUserProblemsFunction(
                    user, 1, count+1)
                print(newSolvedProblems)
                tempUser_df = pd.concat(
                    [newSolvedProblems, tempUser_df], ignore_index=True)
                print(tempUser_df)
                tempUser_df.to_csv(filename, index=False)
        # except:
        #     self.mergeUserProblems(user)

    def createUserProblems(self, userlist):
        # try:
        start = time.time()
        # userlist=["maxrage","Dev_Manus","Dipankar_Kumar_Singh","akashsingh_10"]
        self.mergeUserProblems(userlist[0])
        filename = os.path.join(self.dirname, f"database\{userlist[0]}.csv")
        self.userProblems_df = pd.read_csv(filename)
        for user in userlist[1:]:
            self.mergeUserProblems(user)
            filename = os.path.join(self.dirname, f"database\{user}.csv")
            # print(pd.concat([self.userProblems_df, pd.read_csv(filename)]
            #     ,ignore_index=True))
            self.userProblems_df = pd.concat(
                [self.userProblems_df, pd.read_csv(filename)], ignore_index=True)
            self.userProblems_df = self.userProblems_df.drop_duplicates(
                subset=["contestId", "index"], ignore_index=True)

        # user="userProblems_df"
        # filename = os.path.join(self.dirname, f"database\{user}.csv")
        # self.userProblems_df.to_csv(filename,index=False)
        print(f"{time.time() - start} s in createUserProblems")
        # except:
        #     self.createUserProblems(userlist)

    def getProblemLinks(self, low, high, userlist, need):
        # try:
        start = time.time()
        self.createUserProblems(userlist)
        self.allProblems_df = self.allProblems_df.loc[(
            self.allProblems_df.rating >= low) & (self.allProblems_df.rating <= high)]
        print(f"{time.time() - start} s in getProblemLinks or total time take")
        return self.allProblems_df.sample(need).loc[:, ["contestId", "index"]].to_dict()
        # except:
        #     self.getProblemLinks(self, low, high, userlist, need)


if __name__ == "__main__":
    obj = problems(False)
    userlist = ["maxrage", "Dev_Manus",
                "Dipankar_Kumar_Singh", "akashsingh_10"]
    low = 1400
    high = 1600
    need = 1
    print(obj.getProblemLinks(low, high, userlist, need))
