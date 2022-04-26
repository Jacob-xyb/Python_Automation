from pywinauto import application
app = application.Application()
app.start("Notepad.exe")
dlg = app.UntitledNotepad
# or equivalently
dlg = app["无标题 - 记事本"]
# The next easiest method is to ask for the top_window()
dlg = app.top_window()      # 这个方法的弊端是输入控件中，最上层窗口可能为输入法
# You can use the same parameters as can be passed to。
dlg = app.window(title_re="Page Setup", class_name="#32770")

# Finally to have the most control you can use
dialogs = app.windows()     # 返回 app 的所有窗口
# this will return a list of all the visible, enabled, top level windows of the application.

# You can then use some of the methods in handleprops module select the dialog you want.
# Once you have the handle you need then use
# app.window(handle=win)

# 注意：如果对话框的标题很长 - 那么属性访问可能会很长，在这种情况下通常更容易使用
# app.window(title_re=".*Part of Title.*")
dlg = app.window(title_re=".*记事本.*")



