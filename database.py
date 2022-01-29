import datetime


class DataBase:
    def __init__(self, filename):
        self.filename = filename
        self.projects = None    # was 'users'
        # should add constructor for a text file within databased, to store MFR items
        self.file = None
        self.load()

    def load(self):
        # load list of projects from projects.txt file, saved in main folder
        self.file = open(self.filename, "r")
        self.projects = {}

        for line in self.file:
            # this may be wrong and need to be updated for this function to work
            num, dist, name, eor, created = line.strip().split(";")
            self.projects[num] = (dist, name, eor, created)

        self.file.close()

    def get_proj(self, num):
        if num in self.projects:
            # return project name (position 0)
            return self.projects[num][0]
        else:
            return -1

    def get_all_proj(self):
        keylst = list(self.projects.keys())
        print(f'key list is {keylst}')
        return list(keylst)

    def add_proj(self, num, name, eor, dist):
        # strip gets rid of leading or trailing whitespace
        # add project to project list
        if num.strip() not in self.projects:
            # save by project number
            self.projects[num.strip()] = (name.strip(), eor.strip(), dist.strip(), DataBase.get_date())
            self.save2()
            return 1
        else:
            print("Project already exists")
            return -1

    def validate(self, email, password):
        if self.get_user(email) != -1:
            return self.projects[email][0] == password
        else:
            return False

    # this method for saving projects to different files
    def save1(self, n):
        # write data into the text file
        with open('{0}{1}.txt'.format(n, '-MFR')) as f:
            f.write('blank project' + '\n')
            f.write(str(datetime.now))
            f.write('\n')

    # this method for saving projects to database txt file
    def save2(self):
        # write data into the text file
        with open(self.filename, "w") as f:
            for proj in self.projects:
                f.write(proj + ";" + self.projects[proj][0] + ";" + self.projects[proj][1] + ";" + self.projects[proj][2] + ";" + self.projects[proj][3] + "\n")
            print("project added in save2 method")

    @staticmethod
    def get_date():
        return str(datetime.datetime.now()).split(" ")[0]  # only the date (not time) (time adds an error due to split)


