from pywinauto.application import Application

# notepad 适用 win32
app_win32 = Application()
app_win32.start(r"notepad.exe")
win = app_win32['无标题 - 记事本']
win.wait('ready')
win.menu_select("文件->页面设置")
# win_page_setup = app["页面设置"]
app_win32["页面设置"]['确定'].close_click()
app_win32['无标题 - 记事本']['Edit'].set_edit_text("I am typing s\xe4me text to Notepad"
                                             "\r\n\r\nAnd then I am going to quit")
# exit notepad
app_win32['无标题 - 记事本'].menu_select("文件->退出")
app_win32['记事本']['不保存'].close_click()

# app_uia = Application(backend="uia")
# app_uia.connect(title="无标题 - 记事本")
# # win_uia = app_uia['Notepad']    # 错误, uia 用title名才可以调用
# win_uia = app_uia['无标题 - 记事本']
# win_uia.wait("ready")       # 找不到会 time out
# win_uia.menu_select("文件->页面设置")


