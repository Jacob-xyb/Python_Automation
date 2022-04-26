from pywinauto.application import Application
app = Application(backend="uia").start('notepad.exe')

# describe the window inside Notepad.exe process
# dlg_spec = app.UntitledNotepad
dlg_spec = app["无标题 - 记事本"]
# wait till the window is really open
actionable_dlg = dlg_spec.wait('visible')

dlg_spec.print_control_identifiers()