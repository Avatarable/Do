import datetime

from kivy.properties import ObjectProperty, StringProperty
from kivymd.app import MDApp
import os
import re

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.dialog import MDDialog

from database import Database


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
    password = ""
    content = ObjectProperty(None)

    def on_enter(self, *args):
        password, name, date = db.get_user(self.detail)
        self.content.ids.account_name.text = name
        self.content.ids.account_email.text = self.detail
        self.content.listas = {
            "Monday": "2020-06-09",
            "Practise": "2020-07-15",
            "Market": "2020-07-16",
        }
        self.content.data = {
            "Monday": ["buy bread", "eat akara"],
            "Practise": ["sleep a bit", "learn dance", "wash clothes"],
            "Market": ["play games"]
        }
        self.content.load_list()

        # for i in range(10):
        #     self.ids.container.add_widget(
        #         OneLineListItem(text=f"Single-line item {i}", on_release=self.pressed))

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


class Content(BoxLayout):
    pass
class NewDialog(MDDialog):
    pass

class ContentNavDrawer(BoxLayout):
    dialog = None
    master = ObjectProperty(None)
    listas = {}
    data = {}

    def new_list(self):
        self.list_name_dialog()

    def load_list(self):
        if len(self.listas) > 0:
            for list_name in self.listas.keys():
                self.ids.md_list.add_widget(
                    ItemDrawer(text=list_name)
                )
                self.add_screen(list_name)

    def list_name_dialog(self):
        if not self.dialog:
            self.dialog = NewDialog(
                title="Add New List",
                type="custom",
                content_cls=Content(),
                buttons=[
                    MDFlatButton(text="Cancel", text_color=login_app.theme_cls.primary_color, on_release=self.closeDialog),
                    MDFlatButton(text="Ok", text_color=login_app.theme_cls.primary_color, on_release=self.add)
                ]

            )
            self.dialog.set_normal_height()
            self.dialog.open()

    def add(self, inst):
        for obj in self.dialog.content_cls.children:
            if isinstance(obj, MDTextField):
                self.listas[obj.text] = datetime.datetime.now().strftime("%Y-%m-%d")
                self.ids.md_list.add_widget(ItemDrawer(text=obj.text))
                self.add_screen(obj.text)
                self.master.ids.nav_drawer.set_state("close")
                self.master.ids.screen_man.current = obj.text
        self.dialog.dismiss()
        self.dialog = None

    def add_screen(self, titlee):
        scr = ListScreen(name=titlee, lists=self.data[titlee])
        self.master.ids.screen_man.add_widget(scr)



    def closeDialog(self, inst):
        self.dialog.dismiss()
        self.dialog = None



class ItemDrawer(OneLineListItem):
    pass

class DrawerList(ThemableBehavior, MDList):
    def actions(self, instance_item):
        '''Called when tap on a menu item.'''

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color

        # close nav_drawer and switch screen
        self.parent.parent.master.ids.nav_drawer.set_state("close")
        self.parent.parent.master.ids.screen_man.current = instance_item.text



class ListScreen(Screen):
    lists = ObjectProperty(None)
    selected = []
    selected_item = ""

    def on_enter(self, *args):
        for item in self.lists:
            self.ids.list_content.add_widget(
                OneLineListItem(text=f"{item}", on_release=self.pressed))

    def openNav(self):
        self.parent.master.ids.nav_drawer.set_state("open")

    def pressed(self, item):
        self.selected_item = item.text
        self.set_color_item(item)
        self.ids.upd_btn.disabled = False
        self.ids.del_btn.disabled = False

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

    def add_item(self):
        if self.ids.item_input.text:
            item = self.ids.item_input.text
            self.ids.list_content.add_widget(
                OneLineListItem(text=f"{item}", on_release=self.pressed))
            self.ids.item_input.text = ""

    def upd_item(self):
        if self.ids.item_input.text:
            item = self.ids.item_input.text
            self.selected[0].text = item
            self.ids.item_input.text = ""
            self.ids.upd_btn.disabled = True
            self.ids.del_btn.disabled = True

    def del_item(self):
        self.ids.list_content.remove_widget(self.selected[0])
        self.ids.del_btn.disabled = True
        self.ids.upd_btn.disabled = True










class WindowManager(ScreenManager):
    pass


def warning(title, msg):
    pop = Popup(title=title, content=MDLabel(text=msg, halign='center', theme_text_color="Custom",
                                             text_color=(1, 1, 1, 1)),
                size_hint=(None, None), size=(300, 200))
    pop.open()



class MainApp(MDApp):
    dialog = None
    def build(self):
        # return Builder.load_file("main.kv")
        self.theme_cls.primary_palette = 'Green'
        self.theme_cls.accent_palette = 'Blue'
        self.theme_cls.theme_style = 'Dark'

    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                text="Discard draft?",
                buttons=[
                    MDFlatButton(
                        text="CANCEL", text_color=self.theme_cls.primary_color
                    ),
                    MDFlatButton(
                        text="DISCARD", text_color=self.theme_cls.primary_color
                    ),
                ],
            )
        self.dialog.open()




db = Database("users.txt")


if __name__ == '__main__':
    login_app = MainApp()
    login_app.run()
