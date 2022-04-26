from pywinauto.application import Application

# First you should start your application or connect to an existing app instance.
# an entry point for further automation limiting all the scope by process boundaries.
app = Application(backend="uia").start("notepad.exe")
# describe the window inside Notepad.exe process
dlg_spec = app["无标题 - 记事本"]
# wait till the window is really open
actionable_dlg = dlg_spec.wait('visible')


# If you want to navigate across process boundaries
# (say Win10 Calculator surprisingly draws its widgets in more than one process)
# your entry point is a Desktop object.
# 简单点说, 计算器是多线程的，需要将入口设置为 Desktop
from subprocess import Popen
from pywinauto import Desktop
Popen('calc.exe', shell=True)
dlg = Desktop(backend="uia").Calculator
dlg.wait('visible')

