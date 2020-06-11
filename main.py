from kivy.app import App
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.theming import ThemeManager, ThemableBehavior
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from database import Database
from kivymd.uix.list import MDList, OneLineListItem

import re, os


class LoginPage(Screen):
    prev_email = ""
    prev_passw = ""
    prev_chkbox = False

    def on_enter(self, *args):
        if os.path.isfile('prev_details.txt'):
            self.details_file = open('prev_details.txt', 'r')
            for line in self.details_file:
                if line != "":
                    details = line.strip().split('|')
                    self.prev_email = details[0]
                    self.prev_passw = details[1]
                    self.prev_chkbox = True
            self.details_file.close()


    def login(self):
        email = self.ids.email.text
        password = self.ids.passw.text
        rem = self.ids.chkbox.active

        chk = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

        if email != "" and password != "":
            if db.validate(email, password) and re.match(chk, email):   #validate and check regex

                AccountPage.detail = email      #send details to AccountPage

                #save last login details
                if rem:
                    with open('prev_details.txt', 'w') as f:
                        f.write("{}|{}".format(email,password))
                else:
                    with open('prev_details.txt', 'w') as f:
                        f.write("")

                self.reset()        #reset fields
                login_app.root.current = "Account"      #change screen
            else:
                warning('Invalid Login', 'Incorrect email or password')
        else:
            warning('Invalid Login', 'Required field cannot be blank')

    def reset(self):
        self.ids.email.text = ""
        self.ids.passw.text = ""
        self.ids.chkbox.active = False


class SignupPage(BoxLayout):

    def signup(self):
        email = self.ids.email_su.text
        password = self.ids.passw_su.text
        password_c = self.ids.passw_suc.text
        name = self.ids.namee.text
        print(email, password, password_c, name)
        # chk = re.compile(r'[a-z0-9]+([-+._][a-z0-9]+){0,2}@.*?(\.(a(?:[cdefgilmnoqrstuwxz]|ero|(?:rp|si)a)|b(?:)))')
        chk = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

        if email != "" and password != "" and name != "" and password_c != "":
            if  re.match(chk, email):
                if password == password_c:
                    db.add_user(email, password, name)
                    print("Account created")
                    self.reset()
                    login_app.root.current = "Login"
                else:
                    warning('Invalid Signup', 'Confirm password incorrect')
            else:
                em = self.ids.email_su
                em.color_mode = 'custom'
                em.line_color_normal = (1, 0, 0, 1)
                em.helper_text = "Invalid email address"
                em.helper_text_mode = 'persistent'
        else:
            warning('Invalid Signup', 'Required field cannot be blank')

    def reset(self):
        self.ids.email_su.text = ""
        self.ids.passw_su.text = ""
        self.ids.passw_suc.text = ""
        self.ids.namee.text = ""

class AccountPage(Screen):
    detail = ""
    selected = []

    def on_enter(self, *args):
        password, name, date = db.get_user(self.detail)
        # self.ids.name_lbl.text = "Account name: "+name
        # self.ids.email_lbl.text = "Email: "+self.detail
        # self.ids.date_lbl.text = "Date created: "+date

        for i in range(10):
            self.ids.container.add_widget(
                OneLineListItem(text=f"Single-line item {i}", on_release=self.pressed))

    def pressed(self, item):
        self.set_color_item(item)

    def set_color_item(self, item):
        if len(self.selected) > 0:
            for i in self.selected:
                i.theme_text_color='Custom'
                i.text_color=(1,1,1,1)
        self.selected.clear()
        item.theme_text_color='Custom'
        item.text_color=login_app.theme_cls.primary_color
        self.selected.append(item)
        print("presseddd", item.text)


class WindowManager(ScreenManager):
    pass


def warning(title, msg):
    pop = Popup(title=title, content=MDLabel(text=msg, halign='center', theme_text_color="Custom",
                                             text_color=(1, 1, 1, 1)),
                size_hint=(None, None), size=(300, 200))
    pop.open()


class MainApp(MDApp):
    def build(self):
        # return Builder.load_file("main.kv")
        self.theme_cls.primary_palette = 'Green'
        self.theme_cls.accent_palette = 'Blue'
        self.theme_cls.theme_style = 'Dark'



db = Database("users.txt")


if __name__ == '__main__':
    login_app = MainApp()
    login_app.run()
