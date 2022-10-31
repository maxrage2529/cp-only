self.userProblems_df.drop_duplicates(subset=["contestId", "index"],inplace=True)
        user="userProblems_df"
        filename = os.path.join(self.dirname, f"database\{user}.csv") 
        se