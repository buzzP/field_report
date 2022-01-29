import os

from kivy.core.window import Window
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.utils import platform

from applayout.photoscreen1 import PhotoScreen1
from applayout.createprojectwindow import CreateProjectWindow
from applayout.openornewprojwindow import OpenOrNewProjWindow
from applayout.fieldreportwindow import FieldReportWindow
from applayout.newitemwindow import NewItemWindow
from applayout.openprojwindow import OpenProjWindow
from applayout.windowmanager import WindowManager

from database import DataBase
from mfrdata import MFRdata
import time

#import logging
#Logger.setLevel(logging.TRACE)


if platform == 'android':
    from jnius import autoclass
    from android.permissions import request_permissions, check_permission, \
        Permission
    from android import api_version
    from android.runnable import run_on_ui_thread
    from android import mActivity
    View = autoclass('android.view.View')

    @run_on_ui_thread
    def hide_landscape_status_bar(instance, width, height):
        # width,height gives false layout events, on pinch/spread
        # so use Window.width and Window.height
        if Window.width > Window.height:
            # Hide status bar
            option = View.SYSTEM_UI_FLAG_FULLSCREEN
        else:
            # Show status bar
            option = View.SYSTEM_UI_FLAG_VISIBLE
        mActivity.getWindow().getDecorView().setSystemUiVisibility(option)
else:
    # Dispose of that nasty red dot, required for gestures4kivy.
    from kivy.config import Config
    Config.set('input', 'mouse', 'mouse, disable_multitouch')




def invalidLogin():
    pop = Popup(title='Invalid Login',
                content=Label(text='Invalid username or password.'),
                size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                content=Label(text='Please fill in all inputs with valid information.'),
                size_hint=(None, None), size=(400, 400))

    pop.open()


def get_all_proj():  # being static may be an issue as I want this dependent on state of the object (not static)
    # return keys of database, which is project number
    print(f'get_all_proj: {db.get_all_proj()}')
    return


class MyMainApp(App):
    def build(self):

        # this is so can change screens within code, not within kv file
        # this line deleted - CameraWindow(name="camera"),
        screens = [OpenOrNewProjWindow(name="new_open"),
                   CreateProjectWindow(name="create"),
                   OpenProjWindow(name="open_window"),
                   FieldReportWindow(name="field_report"),
                   NewItemWindow(name="new_item"),
                   ExportWindow(name="export"),
                   PhotoScreen1(name="1")]
        for screen in screens:
            sm.add_widget(screen)

        # this makes the starting window the "new_open" window
        # name is referenced from the kv file
        sm.current = "new_open"

        if platform == 'android':
            Window.bind(on_resize=hide_landscape_status_bar)
            permissions = [Permission.CAMERA, Permission.RECORD_AUDIO]
            if api_version < 29:
                permissions.append(Permission.WRITE_EXTERNAL_STORAGE)
            request_permissions(permissions, self.permissions_callback)
            self.enable_swipe = check_permission(Permission.CAMERA)
        else:
            print("platform is not android")
            self.enable_swipe = True

        print("BUILT")

        return sm

    def permissions_callback(self, permissions, grants):
        self.enable_swipe = check_permission(Permission.CAMERA)

    def swipe_screen(self, right):
        if self.enable_swipe:
            i = int(self.sm.current)
            if right:
                self.sm.transition.direction = 'right'
                self.sm.current = str((i-1) % len(self.screens))
            else:
                self.sm.transition.direction = 'left'
                self.sm.current = str((i+1) % len(self.screens))


if __name__ == "__main__":
    # loads in kv file (display options)
    kv = Builder.load_file("my.kv")

    sm = WindowManager()
    db = DataBase("projects.txt")
    mfr = MFRdata()
    script_dir = os.path.dirname(__file__)
    print(f' script path director is {script_dir}')

    MyMainApp().run()
