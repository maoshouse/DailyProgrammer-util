import praw
import os
import re

class Reader(object):
    def __init__(self):
        self.r = praw.Reddit("Daily Programmer Utility by /u/maoshouse")
        self.subreddit = self.r.get_subreddit('dailyprogrammer')
        self.submissionList = []
        self.submissionListTitles = []
        self.newSubmissionIndices = []
        self.rootDirectory = ""
        # read config file and get list of folders in the projects directory
        self.projects = self.read_cfg()

    def read_cfg(self):
        cfg = open('config.cfg', 'r')
        # config file has one line, gives the location of Projects directory
        line = cfg.readline()
        self.rootDirectory = line[13:len(line)-2]
        subDirs = next(os.walk(self.rootDirectory))[1]
        cfg.close()
        return subDirs

    def get_submissions(self):
        for submission in self.subreddit.get_new():
            # only append if submission is valid
            if(self.is_valid_submission(submission.title)):
                self.submissionList.append(submission)
                self.submissionListTitles.append(self.make_title(submission.title))
    
    def is_valid_submission(self, title):
        # A valid submission can must contain the words "Challenge" or "Weekly"
        splt = title.split()
        for s in splt:
            if(s == "Challenge" or s == "[Weekly"):
                return True

        return False
    
    def make_title(self, title):
        # Determine if Challenge or Weekly
        splt = title.split()
        for i in range(0,len(splt)):
            if(splt[i] == "Challenge"):
                res = '_'.join(splt[i:i+3])
                return re.sub('[!@#$\[\]]', '', res).lower()

            if(splt[i] == "[Weekly"):
                res = '_'.join(splt[i:i+2])
                return re.sub('[!@#$\[\]]', '', res).lower()
        

    def process_data(self):
        # find indices of unique Daily Programmer submissions
        self.newSubmissionIndices = []
        for i in range(0, len(self.submissionListTitles)):
            if(not(self.submissionListTitles[i] in self.projects)):
                self.newSubmissionIndices.append(i)
        
        print("Found", len(self.newSubmissionIndices), "assignments!")

    def choose_assignments(self):
        counter = 1
        for i in self.newSubmissionIndices:
            print("=====", counter, "of", len(self.newSubmissionIndices), "=====")
            print(self.submissionList[i].title)
            print(self.submissionList[i].url)
            print(self.submissionList[i].selftext[:1000], "\n[END OF PREVIEW]")
            choice = self.get_choice("Accept?") 
            if choice:
                self.create_project(i)
            print("\n\n")
            counter+=1

    def create_project(self, choiceIndex):
        projectPath = os.path.join(self.rootDirectory, self.submissionListTitles[choiceIndex])
        if not(os.path.exists(projectPath)):
            os.makedirs(projectPath)
        
        readmePath = os.path.join(projectPath, "README.md")

        file = open(readmePath, "w")
        file.write(self.submissionList[choiceIndex].selftext)
        file.close()
        

    def get_choice(self, prompt):
        while True:
            choice = input(prompt + " [Y/n] ")
            if not(choice in ["Y","y","N","n", ""]):
                print("Invalid entry!")
                continue
            else:
                break
        if choice in ["N","n"]:
            return False
        else:
            return True

    def read(self):
        self.get_submissions()
        self.process_data()

        if(len(self.newSubmissionIndices) > 0):
            choice = self.get_choice("Choose assignments?")
            if choice:
                self.choose_assignments()
            
