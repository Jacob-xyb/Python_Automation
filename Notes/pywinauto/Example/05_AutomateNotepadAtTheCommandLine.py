from pywinauto import application

'''
English
app = application.Application()
app.start("Notepad.exe")
app.UntitledNotepad.draw_outline()
app.UntitledNotepad.menu_select("Edit -> Replace")
app.Replace.print_control_identifiers()
app.Replace.Cancel.click()
app.UntitledNotepad.Edit.type_keys("Hi from Python interactive prompt %s" % str(dir()), with_spaces = True)
app.UntitledNotepad.menu_select("File -> Exit")
app.Notepad.DontSave.click()
'''

app = application.Application()
app.start("Notepad.exe")
app["无标题 - 记事本"].draw_outline()
app["无标题 - 记事本"].menu_select("编辑(&E) -> 替换(&R)")
app["替换"].print_control_identifiers()
# 由于是中文，要么确定控件的匹配项 ['Button4']
app["替换"].Button4.click()
# 要么用标准调用方式
app["替换"].child_window(title="取消", class_name="Button").click()
# 当然最安全可靠的方式是 close_click()
app["替换"].child_window(title="取消", class_name="Button").close_click()
# 没有 with_spaces 参数空格将不会被输入。
app["无标题 - 记事本"].Edit.type_keys("Hi from Python interactive prompt %s" % str(dir()), with_spaces=True)
app["无标题 - 记事本"].menu_select("文件(&F) -> 退出(&X)")
# app["记事本"].print_control_identifiers()
app["记事本"].child_window(title="不保存(&N)", class_name="Button").close_click()
