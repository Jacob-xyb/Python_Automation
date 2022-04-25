from pywinauto.application import Application
app = Application(backend="uia").start("notepad.exe")
# app.UntitledNotepad.type_keys("%FX")    # English System
app["无标题 - 记事本"].type_keys("%FX")

