import datetime
import os

class Database:
    def __init__(self, filename):
        self.filename = filename
        self.users = None
        self.file = None
        self.load()

    def load(self):
        if os.path.isfile(self.filename):
            self.file = open(self.filename, 'r')
            self.users = {}

            for line in self.file:
                if line != "":
                    email, password, name, date_created = line.strip().split("|")
                    self.users[email] = (password, name, date_created)

            self.file.close()
        else:
            with open(self.filename, 'w') as f:
                f.write('')


    def get_user(self, email):
        if email in self.users:
            return self.users[email]
        else:
            return -1

    def add_user(self, email, password, name):
        if email.strip() not in self.users:
            self.users[email] = (password.strip(), name.strip(), self.get_date())
            self.save()
            return 1
        else:
            print("User already exist")
            return -1

    def validate(self, email, password):
        if self.get_user(email) != -1:
            return self.users[email][0] == password
        else:
            return False

    def save(self):
        with open(self.filename, 'w') as f:
            for user in self.users:
                f.write(user + "|" + self.users[user][0] + "|" + self.users[user][1] + "|" + self.users[user][2] + "\n")


    def get_date(self):
        return str(datetime.datetime.now()).split(" ")[0]


