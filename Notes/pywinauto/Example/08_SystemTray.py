# https://pywinauto.readthedocs.io/en/latest/HowTo.html#how-to-access-the-system-tray-aka-systray-aka-notification-area

# too hard

from pywinauto import application
app = application.Application().connect(path=r"wechat.exe")
app.top_window().draw_outline()
# systray_icons = app.WeChatMainWndForPC.NotificationAreaToolbar
# systray_icons.click_input()
# taskbar.ClickSystemTrayIcon("Microsoft Outlook")
