from pywinauto.application import Application

# Tips:
# 1: win32[] 调用的是 ClassName， uia[] 调用的是 Name
# 2: print_control_identifiers:  - "Title" 坐标

# Keyboard
"""
pywinauto.keyboard.send_keys()
"""

# Mouse
"""
pywinauto.mouse.click(button='left', coords=(0, 0))
pywinauto.mouse.double_click(button='left', coords=(0, 0))
pywinauto.mouse.move(coords=(0, 0))
pywinauto.mouse.press(button='left', coords=(0, 0))
pywinauto.mouse.release(button='left', coords=(0, 0))
pywinauto.mouse.right_click(coords=(0, 0))
pywinauto.mouse.scroll(coords=(0, 0), wheel_dist=1)
pywinauto.mouse.wheel_click(coords=(0, 0))
"""

# app
"""
app.kill(soft=False)        # 强制关闭
app.cpu_usage()             # 返回指定秒数期间的CPU使用率百分比
app.wait_cpu_usage_lower(threshold=2.5, timeout=None, usage_interval=None)  # 等待进程CPU使用率百分比小于指定的阈值threshold%
app.is64bit()       # 如果操作的进程是64-bit，返回True
app.windows()       # 查看app所有窗口

层级查找控件的方法：
# 带 window 则返回 WindowSpecification 对象
# 否则返回 BaseWrapper 对象
window(**kwargs) # 用于窗口的查找,不确定时不建议用。 # 全部后代
child_window(**kwargs) # 可以不管层级的找后代中某个符合条件的元素，最常用
    '''
    title: Inspect 中的 Name 属性
    control_type: Group,Button.
    auto_id: 对应  Inspect 中的 AutomationId
    class_name: 对应 Inspect 中的 ClassName
    ...
    '''
"""

# dlg
"""
dlg.parent() # 返回此元素的父元素,没有参数
dlg.children(**kwargs) # 返回符合条件的子元素列表,支持索引，是BaseWrapper对象（或子类）
dlg.descendants(**kwargs) # 返回符合条件的所有后代元素列表,是BaseWrapper对象（或子类）
dlg.iter_children(**kwargs) # 符合条件后代元素迭代器，是BaseWrapper对象（或子类）, 测试是 app 整个符合条件的子类

# 以下几个只支持窗口模式的控件
dlg.close() # 关闭界面
dlg.minimize() # 最小化界面
dlg.maximize() # 最大化界面
dlg.restore() # 将窗口恢复为正常大小，比如最小化的让他正常显示在桌面  **
dlg.get_show_state() # 正常0，最大化1，最小化2
dlg.exists(timeout=None, retry_interval=None) # 判断是否存在  **
    #timeout：等待时间，一般默认5s
    #retry_interval：timeout内重试时间
dlg.wait(wait_for, timeout=None, retry_interval=None) # 等待窗口处于特定状态
dlg.wait_not(wait_for_not, timeout=None, retry_interval=None) # 等待窗口不处于特定状态，即等待消失
    # wait_for/wait_for_not:
    # * 'exists' means that the window is a valid handle
    # * 'visible' means that the window is not hidden
    # * 'enabled' means that the window is not disabled
    # * 'ready' means that the window is visible and enabled
    # * 'active' means that the window is active
    # timeout:等待多久
    # retry_interval:timeout内重试时间
    # eg: dlg.wait('ready')
"""

# 鼠标键盘操作
"""
# 我只列举常用形式，他们有很多默认参数但不常用，可以在源码中查看
ctrl.click_input()  # 最常用的点击方法，一切点击操作的基本方法（底层调用只是参数不同），左键单击，使用时一般都使用默认不需要带参数
ctrl.right_click_input()  # 鼠标右键单击
# 键盘输入,底层还是调用keyboard.send_keys
ctrl.type_keys(keys, pause=None, with_spaces=False, )
# keys：要输入的文字内容
# pause：每输入一个字符后等待时间，默认0.01就行
# with_spaces：是否保留keys中的所有空格，默认去除0
ctrl.double_click_input(button="left", coords=(None, None))  # 左键双击
ctrl.press_mouse_input(coords=(None, None))  # 指定坐标按下左键，不传坐标默认左上角
ctrl.release_mouse_input(coords=(None, None))  # 指定坐标释放左键，不传坐标默认左上角
ctrl.move_mouse_input(coords=(0, 0))  # 将鼠标移动到指定坐标，不传坐标默认左上角
ctrl.drag_mouse_input(dst=(0, 0))  # 将ctrl拖动到dst,是press-move-release操作集合

# 控件的常用属性===================================================================================
ctrl.children_texts()  # 所有子控件的文字列表，对应inspect中Name字段  **
ctrl.window_text()  # 控件的标题文字，对应inspect中Name字段   **
# ctrl.element_info.name
ctrl.class_name()  # 控件的类名，对应inspect中ClassName字段，有些控件没有类名
# ctrl.element_info.class_name
ctrl.element_info.control_type  # 控件类型，inspect界面LocalizedControlType字段的英文名
ctrl.is_child(parent)  # ctrl是否是parent的子控件
ctrl.legacy_properties().get('Value')  # 可以获取inspect界面LegacyIAccessible开头的一系列字段，在源码uiawraper.py中找到了这个方法，非常有用
# 如某些按钮显示值是我们想要的，但是window_text获取到的是固定文字‘修改群昵称’，这个值才是我们修改后的新名字

# 控件常用操作========================================================================================
ctrl.draw_outline(colour='green')  # 空间外围画框，便于查看，支持'red', 'green', 'blue'
ctrl.print_control_identifiers(depth=None, filename=None)  # 打印其包含的元素，详见打印元素
ctrl.scroll(direction, amount, count=1, )  # 滚动
# direction ："up", "down", "left", "right"
# amount："line" or "page"
# count：int 滚动次数
ctrl.capture_as_image()  # 返回控件的 PIL image对象，可继续使用其方法如下：
eg:
ctrl.capture_as_image().save(img_path)
ret = ctrl.rectangle()  # 控件上下左右坐标，(L430, T177, R1490, B941)，可.输出上下左右
eg:
ret.top = 177
ret.bottom = 941
ret.left = 430
ret.right = 1490

# 输入输出操作
# 先ctrl+a选中所有然后再type_keys替换，和我们选中然后修改一样的
edit_btn.type_keys('^a').type_keys('备注名字', with_spaces=True)

# mouse操作========================================================================================
from pywinauto import mouse

mouse.move(coords=(x, y))  # 移动鼠标
mouse.click(button='left', coords=(40, 40))  # 指定位置，鼠标左击
mouse.double_click(button='left', coords=(140, 40))  # 鼠标双击
mouse.press(button='left', coords=(140, 40))  # 将鼠标移动到（140，40）坐标处按下不放
mouse.release(button='left', coords=(300, 40))  # 将鼠标移动到（300，40）坐标处释放，
mouse.right_click(coords=(400, 400))  # 右键单击指定坐标
mouse.wheel_click(coords=(400, 400))  # 鼠标中键单击指定坐标(很少用的到)
mouse.scroll(coords=(1200, 300), wheel_dist=-3)  # 滚动鼠标 wheel_dist指定鼠标滚轮滑动，正数往上，负数往下。


# 以控件中心为起点，滚动
def mouse_scroll(control, distance):
    rect = control.rectangle()
    cx = int((rect.left + rect.right) / 2)
    cy = int((rect.top + rect.bottom) / 2)
    mouse.scroll(coords=(cx, cy), wheel_dist=distance)


mouse_scroll(control=win_main_Dialog.child_window(control_type='List', title='联系人'), distance=-5)

# keyboard操作========================================================================================
# 比type_keys更快
import keyboard
import io

for line in io.StringIO(msg):
    keyboard.write(line.strip())  #
    keyboard.send('ctrl+enter')
keyboard.write(chat_name)
keyboard.send('enter')
keyboard.send('ctrl+v')
"""