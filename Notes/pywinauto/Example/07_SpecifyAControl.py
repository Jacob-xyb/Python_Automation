from pywinauto import application

# 如果是用win32，那么
# app = application.Application(backend='win32')
# app["无标题 - 记事本"].menu_select("编辑(&E) -> 替换(&R)")

app = application.Application(backend='uia')
try:
    # app.connect(title="无标题 - 记事本")
    app.connect(path="Notepad.exe")
    print("connect")
except:
    app.start("Notepad.exe")


app["无标题 - 记事本"].menu_select("编辑(&E) -> 替换(&R)")
'''
# 菜单单独调用就很繁琐
app["无标题 - 记事本"]["编辑(&E)"].click_input()        # win32 模式无法这样调用, 但是 win32 可显示的控件非常少
app["无标题 - 记事本"]["替换(R)...	Ctrl+H"].click_input()
'''



