
import json
import random
import requests
import pandas as pd
import time

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
    def __init__(self):
        start = time.time()
        problemset_problems = json.loads(requests.get(
            "https://codeforces.com/api/problemset.problems").text)
        allProblems = problemset_problems["result"]["problems"]
        self.allProblems_df = pd.DataFrame(allProblems)
        self.allProblems_df.drop(
            ["name", "type", "points"], axis=1, inplace=True)
        print(f"{time.time() - start} s in init")

    def getUserProblemsFunction(self, user):
        time.sleep(0.5)
        print("delayed")
        try:
            start = time.time()
            res = requests.get(
                "https://codeforces.com/api/user.status?handle="+user)
            print(len(res.text),user)
            print(res.status_code)
            user_status = json.loads(res.text)
            temp_userProblems = user_status["result"]
            temp_userProblems_df = pd.DataFrame(temp_userProblems)

            # here verdict has been ignored all problems has been included irrespective of result whether accpeted or not
            userProblems_df = pd.DataFrame(
                temp_userProblems_df["problem"].to_dict())
            userProblems_df = userProblems_df.transpose()
            userProblems_df.drop(["name", "type", "points"], axis=1, inplace=True)

            userProblems_df.drop_duplicates(
                subset=["contestId", "index"], inplace=True)
            print(f"{time.time() - start} s in getUserProblemsFunction")
            return userProblems_df
        except:
            print("exception occured  retrying")
            self.getUserProblemsFunction(user)
    def createUserProblems(self, userlist):
        start = time.time()
        # userlist=["maxrage","Dev_Manus","Dipankar_Kumar_Singh","akashsingh_10"]
        self.userProblems_df = self.getUserProblemsFunction(userlist[0])
        for user in userlist[1:]:
            self.userProblems_df = pd.concat([self.userProblems_df, self.getUserProblemsFunction(
                user)]).drop_duplicates(subset=["contestId", "index"])
        print(f"{time.time() - start} s in createUserProblems")

    def getProblemLinks(self, low, high, userlist, need):
        start = time.time()
        self.createUserProblems(userlist)
        self.allProblems_df = self.allProblems_df.loc[(
            self.allProblems_df.rating >= low) & (self.allProblems_df.rating <= high)]
        print(f"{time.time() - start} s in createUserProblems")
        return self.allProblems_df.sample(need).loc[:, ["contestId", "index"]].to_dict()


if __name__ == "__main__":
    obj = problems()
    userlist = ["maxrage", "Dev_Manus",
                "Dipankar_Kumar_Singh", "akashsingh_10"]
    low = 1400
    high = 1600
    need = 1
    print(obj.getProblemLinks(low, high, userlist, need))
