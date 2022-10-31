
import json
import random
import requests
import pandas as pd

# python -m venv folder_name
# venv\Scripts\activate
# pip install pandas requests
# pip freeze > requirements.txt
class problems:
    def __init__(self):
        problemset_problems = json.loads(requests.get("https://codeforces.com/api/problemset.problems").text)
        allProblems = problemset_problems["result"]["problems"]
        self.allProblems_df = pd.DataFrame(allProblems)
        self.allProblems_df.drop(["name","type","points"],axis=1,inplace=True)
    
    def getUserProblemsFunction(self,user):
        user_status = json.loads(requests.get("https://codeforces.com/api/user.status?handle="+user).text)
        temp_userProblems = user_status["result"]
        temp_userProblems_df = pd.DataFrame(temp_userProblems)

        #here verdict has been ignored all problems has been included irrespective of result whether accpeted or not 
        userProblems_df=pd.DataFrame(temp_userProblems_df["problem"].to_dict())
        userProblems_df=userProblems_df.transpose()
        userProblems_df.drop(["name","type","points"],axis=1,inplace=True)

        userProblems_df.drop_duplicates(subset=["contestId","index"],inplace=True)
        return userProblems_df

    def createUserProblems(self,userlist):
        # userlist=["maxrage","Dev_Manus","Dipankar_Kumar_Singh","akashsingh_10"]
        self.userProblems_df=self.getUserProblemsFunction(userlist[0])
        for user in userlist[1:]:
                self.userProblems_df=pd.concat([self.userProblems_df,self.getUserProblemsFunction(user)]).drop_duplicates(subset=["contestId","index"])

    def getProblemLinks(self,low,high,userlist,need):
        self.createUserProblems(userlist)
        self.allProblems_df=self.allProblems_df.loc[(self.allProblems_df.rating>=low) & (self.allProblems_df.rating<=high)]
        return self.allProblems_df.sample(need).loc[:,["contestId","index"]].to_dict()
if __name__ == "__main__":
    obj=problems()
    userlist=["maxrage","Dev_Manus","Dipankar_Kumar_Singh","akashsingh_10"]
    low=1400
    high=1600
    need=1
    print(obj.getProblemLinks(low,high,userlist,need))
