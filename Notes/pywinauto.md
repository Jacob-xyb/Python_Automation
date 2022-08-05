# 安装

https://github.com/pywinauto/pywinauto/releases

[pywinauto docs](https://pywinauto.readthedocs.io/en/latest/)

[gui-inspect-tool](https://github.com/blackrosezy/gui-inspect-tool)

- 自动安装

  `pip install pywinauto`

  最好是安装的全一点，少不了文件操作。

  ```python
  comtypes==1.1.11.whl
  keyboard==0.13.5
  Pillow==9.0.0
  psutil==5.7.2
  pypiwin32==223
  pywin32==303
  pywinauto==0.6.8
  six==1.16.0
  xlrd==1.2.0
  xlwt==1.3.0
  ```

- 手动安装

  pywin32、six、comtypes、pillow、pywinauto

## 支持列表

- **Win32 API** (`backend="win32"`) - 现在的默认backend

  - MFC, VB6, VCL, 简单的WinForms控件和大多数旧的遗留应用程序

- **MS UI Automation** (`backend="uia"`)

  - WinForms, WPF, Store apps, Qt5, 浏览器

  注意: Chrome在启动之前需要`--force-renderer-accessibility` cmd标志。 由于comtypes Python库限制，不支持自定义属性和控件。

## GUI对象检查/Spy工具

如果您仍然不确定哪个backend最适合您，请尝试使用免费提供的对象检查/Spy工具：从GitHub repo [gui-inspect-tool](https://github.com/blackrosezy/gui-inspect-tool)下载它们.

- **Inspect.exe** 是Microsoft创建的另一个很棒的工具。 它包含在Windows SDK中，因此可以在x64 Windows上的以下位置找到它：

  ```
  C:\Program Files (x86)\Windows Kits\<winver>\bin\x64     
  ```

  将Inspect.exe切换到**UIA mode**（使用MS UI Automation）。 如果它可以显示比Spy ++更多的控件及其属性，那么可能是 `"uia"`backend是你的选择。
  
- [py_inspect](https://github.com/pywinauto/py_inspect) is a prototype of multi-backend spy tool based on pywinauto. Switching between available backends can show you a difference in hierarchies with “win32” and “uia” backends. **py_inspect** is a future replacement of [SWAPY](https://github.com/pywinauto/SWAPY) which supports “win32” backend only at the moment when pywinauto==0.5.4 was out. Initial implementation of py_inspect contains just about 150 lines of code thanks to modern pywinauto 0.6.0+ architecture.

  `py_inspect.py` 源码在项目里面也有

# Reference

## 检测是否安装成功

```python
from pywinauto.application import Application
app = Application(backend="uia").start("notepad.exe")
# app.UntitledNotepad.type_keys("%FX")    # English System
app["无标题 - 记事本"].type_keys("%FX")
```

## Entry Points For Automation

- 一个主进程限制所有线程的

```python
from pywinauto.application import Application

# First you should start your application or connect to an existing app instance.
# an entry point for further automation limiting all the scope by process boundaries.
app = Application(backend="uia").start("notepad.exe")
# describe the window inside Notepad.exe process
dlg_spec = app["无标题 - 记事本"]
# wait till the window is really open
actionable_dlg = dlg_spec.wait('visible')
```

- 多线程的应用

```python
# If you want to navigate across process boundaries
# (say Win10 Calculator surprisingly draws its widgets in more than one process)
# your entry point is a Desktop object.
# 简单点说, 计算器是多线程的，需要将入口设置为 Desktop
from subprocess import Popen
from pywinauto import Desktop
Popen('calc.exe', shell=True)
dlg = Desktop(backend="uia").Calculator
dlg.wait('visible')
```

**Application** and **Desktop** objects are both backend-specific. No need to use backend name in further actions explicitly.

## Window Specification

这是高级 pywinauto API 的核心概念。您可以大致或更详细地描述任何窗口或控件，即使它尚不存在或已关闭。窗口规范还保留有关将用于获取真实窗口或控件的匹配/搜索算法的信息。

让我们创建一个详细的窗口规范：

```python
from pywinauto.application import Application
app = Application(backend="uia").start('notepad.exe')

# describe the window inside Notepad.exe process
# dlg_spec = app.UntitledNotepad
dlg_spec = app["无标题 - 记事本"]
# wait till the window is really open
actionable_dlg = dlg_spec.wait('visible')
```

实际的窗口查找是通过`wrapper_object()`方法来执行的。它为真实的现有窗口/控件或 raises 返回一些包装器`ElementNotFoundError`。这个包装器可以通过发送动作或检索数据来处理窗口/控件。

但是 Python 可以隐藏此`wrapper_object()`调用，以便您在生产中拥有更紧凑的代码。以下语句完全相同：

```python
dlg_spec.wrapper_object().minimize() # while debugging
dlg_spec.minimize() # in production
```

创建窗口规范有许多可能的标准。这些只是几个例子。

```python
# can be multi-level
app.window(title_re='.* - Notepad$').window(class_name='Edit')

# can combine criteria
dlg = Desktop(backend="uia").Calculator
dlg.window(auto_id='num8Button', control_type='Button')
```

## Attribute Resolution Magic

Python 通过动态解析对象属性来简化创建窗口规范。但是属性名称与任何变量名称具有相同的限制：**不能有空格、逗号和其他特殊符号**。但幸运的是 pywinauto 使用“最佳匹配”算法使查找能够抵抗拼写错误和小变化。

```python
app.UntitledNotepad
# is equivalent to
app.window(best_match='UntitledNotepad')
```

Unicode characters and special symbols usage is possible through an item access in a dictionary like manner.

```python
app['Untitled - Notepad']
# is the same as
app.window(best_match='Untitled - Notepad')
```

## How to know magic attribute names

There are several principles how “best match” gold names are attached to the controls. So if a window specification is close to one of these names you will have a successful name matching.

1. By title (window text, name): `app.Properties.OK.click()`
2. By title and control type: `app.Properties.OKButton.click()`
3. By control type and number: `app.Properties.Button3.click()` (*Note*: Button0 and Button1 match the same button, Button2 is the next etc.)
4. By top-left label and control type: `app.OpenDialog.FileNameEdit.set_text("")`
5. By control type and item text: `app.Properties.TabControlSharing.select("General")`

## How to disable magic attribute names

In some cases, you might prefer disable the magic lookup system, so that Pywinauto immediately raises if you access an attribute which exists neither on the WindowSpecification object, nor on the underlying element-wrapper object. Indeed, by default, Pywinauto will add your attribute name to the search system, and will only fail on a subsequent attribute access or method call.

In this case, turn off the allow_magic_lookup argument of your Desktop or Application instance:

```python
desktop = Desktop(backend='win32', allow_magic_lookup=False)
# or 
app = Application(allow_magic_lookup=False)
```

## Look at the examples

The following examples are included: **Note**: Examples are language dependent - they will only work on the language of product that they were programmed for. All examples have been programmed for English Software except where highlighted.

- `mspaint.py` Control MSPaint
- `notepad_fast.py` Use fast timing settings to control Notepad
- `notepad_slow.py` Use slow timing settings to control Notepad
- `notepad_item.py` Use item rather then attribute access to control Notepad.
- `misc_examples.py` Show some exceptions and how to get control identifiers.
- `save_from_internet_explorer.py` Save a Web Page from Internet Explorer.
- `save_from_firefox.py` Save a Web Page from Firefox.
- `get_winrar_info.py` Example of how to do multilingual automation. This is not an ideal example (works on French, Czech and German WinRar)
- `forte_agent_sample.py` Example of dealing with a complex application that is quite dynamic and gives different dialogs often when starting.
- `windowmediaplayer.py` Just another example - deals with check boxes in a ListView.
- `test_sakura.py`, `test_sakura2.py` Two examples of automating a Japanase product.

## Automate notepad at the command line

```python
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
```

打印替换对话框上控件的标识符，例如替换对话框上的第一个编辑控件可以由以下任何标识符引用：

```python
app.Replace.Edit
app.Replace.Edit0
app.Replace.Edit1
app.FindwhatEdit
```

The last is the one that gives the user reading the script aftewards the best idea of what the script does.

关闭替换对话框。(在脚本文件中，使用`close_click()`比使用`click()`更安全，因为close_click()会等待更长的时间来给windows关闭对话框的时间。)

# How To’s

## Definitions

Some important defitions may be helpful for beginners.

- **对话框**是包含几个其他 GUI 元素/控件（如按钮、编辑框等）的窗口。对话框不一定是主窗口。主窗体顶部的消息框也是一个对话框。pywinauto 也将主窗体视为对话框。
- 控件是层次结构中任何级别的 GUI 元素。该定义包括窗口、按钮、编辑框、网格、网格单元、栏等
- Win32 API 技术（pywinauto 中的“win32”后端）为每个控件提供了一个标识符。这是一个称为**句柄(handle)**的唯一整数。**This definition includes window, button, edit box, grid, grid cell, bar etc.**
- UI Automation  API（pywinauto 中的“uia”后端）可能不会为每个 GUI 元素提供窗口**句柄。**这样的元素对“win32”后端不可见。但如果可用，`Inspect.exe`可以显示属性。`NativeWindowHandle`

## How to specify a usable Application instance

An `Application()` instance is the point of contact for all work with the application you are automating. So the Application instance needs to be connected to a process. There are two ways of doing this:

```python
start(self, cmd_line, timeout=app_start_timeout)  # instance method:
# or
connect(self, **kwargs)  # instance method:
```

`start()` is used when the application is not running and you need to start it. Use it in the following way:

```python
app = Application().start(r"c:\path\to\your\application -a -n -y --arguments")
```

The timeout parameter is optional, it should only be necessary to use if the application takes a long time to start up.

timeout参数是可选的，只有在应用程序需要很长时间启动时才应该使用它。

`connect()` is used when the application to be automated is already launched. To specify an already running application you need to specify one of the following:

| process:    | the process id of the application, e.g.                      |
| :---------- | ------------------------------------------------------------ |
|             | `app = Application().connect(process=2341)`                  |
| **handle:** | The windows handle of a window of the application, e.g.      |
|             | `app = Application().connect(handle=0x010f0c) `              |
| path:       | The path of the executable of the process (`GetModuleFileNameEx` is used to find the path of each process and compared against the value passed in) e.g. |
|             | `app = Application().connect(path=r"c:\windows\system32\notepad.exe") ` |

or any combination of the parameters that specify a window, these get passed to the [`pywinauto.findwindows.find_elements()`](https://pywinauto.readthedocs.io/en/latest/code/pywinauto.findwindows.html#pywinauto.findwindows.find_elements) function. e.g.


```python
app = Application().connect(title_re=".*Notepad", class_name="Notepad")
```

**Note**: The application has to be ready before you can use connect*(). There is no timeout or retries like there is when finding the application after start(). So if you start the application outside of pywinauto you need to either sleep or program a wait loop to wait until the application has fully started.

**注意**：应用程序必须准备好才能使用 connect*()。没有像在 start() 之后找到应用程序时那样的超时或重试。因此，如果您在 pywinauto 之外启动应用程序，您需要休眠或编写一个等待循环以等待应用程序完全启动。

## How to specify a dialog of the application

Once the application instance knows what application it is connected to a dialog to work on needs to be specified.

There are many different ways of doing this. The most common will be using item or attribute access to select a dialog based on it’s title. e.g

```python
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
```

## How to specify a control on a dialog

There are a number of ways to specify a control, the simplest are

```python
app.dlg.control
app['dlg']['control']
# The 2nd is better for non English OS’s where you need to pass unicode strings e.g.
app[u'your dlg title'][u'your ctrl title']
```

The code builds up multiple identifiers for each control from the following:

> - title
> - friendly class
> - title + friendly class

If the control’s title text is empty (after removing non char characters) this text is not used. Instead we look for the closest title text above and to the right of the control. And append the friendly class. So the list becomes

> - friendly class
> - closest text + friendly class

## How to deal with controls that do not respond as expected (e.g. OwnerDraw Controls)

某些控件（尤其是 Ownerdrawn 控件）不会按预期响应事件。例如，如果您查看任何 HLP 文件并转到索引选项卡（单击“搜索”按钮），您将看到一个列表框。在此运行 Spy 或 Winspector 将显示它确实是一个列表框 - 但它是所有者绘制的。这意味着开发人员已告知 Windows，他们将覆盖项目的显示方式并自行执行。在这种情况下，他们已经做到了，因此无法检索字符串:-(。

那么这会导致什么问题呢？

```python
app.HelpTopics.ListBox.texts()                # 1
app.HelpTopics.ListBox.select("ItemInList")   # 2
```

1. Will return a list of empty strings, all this means is that pywinauto has not been able to get the strings in the listbox
2. This will fail with an IndexError because the select(string) method of a ListBox looks for the item in the Texts to know the index of the item that it should select.

The following workaround will work on this control

```python
app.HelpTopics.ListBox.select(1)
```

不幸的是，即使这样也不会总是奏效。开发人员可以使控件不响应 Select 等标准事件。在这种情况下，您可以在列表框中选择项目的唯一方法是使用 TypeKeys() 的键盘模拟。

```python
app.Helptopics.ListBox1.type_keys("{HOME}{DOWN 2}{ENTER}")
```

- `{HOME}` will make sure that the first item is highlighted.
- `{DOWN 2}` will then move the highlight down two items
- `{ENTER}` will select the highlighted item

TODO: WinHelp example?

## How to Access the System Tray (aka SysTray, aka ‘Notification Area’)

在时钟附近有代表正在运行的应用程序的图标，这个区域通常被称为“系统托盘”。事实上，这个区域有很多不同的窗口/控件。包含图标的控件实际上是一个工具栏。它是具有类 TrayNotifyWnd 的窗口内的 Pager 控件的子控件，该类位于具有类 Shell_TrayWnd 的另一个窗口内，并且所有这些窗口都是正在运行的资源管理器实例的一部分。谢天谢地，您不需要记住所有这些:-)。

需要记住的重要一点是，您正在“Explorer.exe”应用程序中寻找一个具有“Shell_TrayWnd”类的窗口，该窗口具有标题为“通知区域”的工具栏控件。

一种方法是执行以下操作

```python
import pywinauto.application
app = pywinauto.application.Application().connect(path="explorer")
systray_icons = app.ShellTrayWnd.NotificationAreaToolbar
```

The taskbar module provides very preliminary access to the System Tray.

It defines the following variables:

| explorer_app:        | defines an Application() object connected to the running explorer. You probably don’t need to use it directly very much. |
| :------------------- | ------------------------------------------------------------ |
| TaskBar:             | The handle to the task bar (the bar containing Start Button, the QuickLaunch icons, running tasks, etc |
| StartButton:         | “Start me up” :-) I think you might know what this is!       |
| QuickLaunch:         | The Toolbar with the quick launch icons                      |
| SystemTray:          | The window that contains the Clock and System Tray Icons     |
| Clock:               | The clock                                                    |
| SystemTrayIcons:     | The toolbar representing the system tray icons               |
| RunningApplications: | The toolbar representing the running applications            |

这部分理解困难：https://pywinauto.readthedocs.io/en/latest/HowTo.html#how-to-access-the-system-tray-aka-systray-aka-notification-area

# Waiting for Long Operation

## Application methods

```python
app.wait_cpu_usage_lower(threshold=5) # wait until CPU usage is lower than 5%
```

NOTE: this method is available for the whole application process only, not for a window/element.

## WindowSpecification methods

[wait_until](https://pywinauto.readthedocs.io/en/latest/code/pywinauto.timings.html?highlight=wait_until#pywinauto.timings.wait_until)

[wait_until_passes](https://pywinauto.readthedocs.io/en/latest/code/pywinauto.timings.html?highlight=wait_until_passes#pywinauto.timings.wait_until_passes)

# Methods available to each different control type

一般查阅这个比较快

https://pywinauto.readthedocs.io/en/latest/controls_overview.html#methods-available-to-each-different-control-type

# Mouse and Keyboard

https://pywinauto.readthedocs.io/en/latest/code/pywinauto.mouse.html#pywinauto-mouse

https://pywinauto.readthedocs.io/en/latest/code/pywinauto.keyboard.html#pywinauto-keyboard

## Mouse

```python
pywinauto.mouse.click(button='left', coords=(0, 0))
pywinauto.mouse.double_click(button='left', coords=(0, 0))
pywinauto.mouse.move(coords=(0, 0))
pywinauto.mouse.press(button='left', coords=(0, 0))
pywinauto.mouse.release(button='left', coords=(0, 0))
pywinauto.mouse.right_click(coords=(0, 0))
pywinauto.mouse.scroll(coords=(0, 0), wheel_dist=1)
pywinauto.mouse.wheel_click(coords=(0, 0))
```

## Keyboard

`pywinauto.keyboard.send_keys()`

- **Available key codes:**

```python
{SCROLLLOCK}, {VK_SPACE}, {VK_LSHIFT}, {VK_PAUSE}, {VK_MODECHANGE},
{BACK}, {VK_HOME}, {F23}, {F22}, {F21}, {F20}, {VK_HANGEUL}, {VK_KANJI},
{VK_RIGHT}, {BS}, {HOME}, {VK_F4}, {VK_ACCEPT}, {VK_F18}, {VK_SNAPSHOT},
{VK_PA1}, {VK_NONAME}, {VK_LCONTROL}, {ZOOM}, {VK_ATTN}, {VK_F10}, {VK_F22},
{VK_F23}, {VK_F20}, {VK_F21}, {VK_SCROLL}, {TAB}, {VK_F11}, {VK_END},
{LEFT}, {VK_UP}, {NUMLOCK}, {VK_APPS}, {PGUP}, {VK_F8}, {VK_CONTROL},
{VK_LEFT}, {PRTSC}, {VK_NUMPAD4}, {CAPSLOCK}, {VK_CONVERT}, {VK_PROCESSKEY},
{ENTER}, {VK_SEPARATOR}, {VK_RWIN}, {VK_LMENU}, {VK_NEXT}, {F1}, {F2},
{F3}, {F4}, {F5}, {F6}, {F7}, {F8}, {F9}, {VK_ADD}, {VK_RCONTROL},
{VK_RETURN}, {BREAK}, {VK_NUMPAD9}, {VK_NUMPAD8}, {RWIN}, {VK_KANA},
{PGDN}, {VK_NUMPAD3}, {DEL}, {VK_NUMPAD1}, {VK_NUMPAD0}, {VK_NUMPAD7},
{VK_NUMPAD6}, {VK_NUMPAD5}, {DELETE}, {VK_PRIOR}, {VK_SUBTRACT}, {HELP},
{VK_PRINT}, {VK_BACK}, {CAP}, {VK_RBUTTON}, {VK_RSHIFT}, {VK_LWIN}, {DOWN},
{VK_HELP}, {VK_NONCONVERT}, {BACKSPACE}, {VK_SELECT}, {VK_TAB}, {VK_HANJA},
{VK_NUMPAD2}, {INSERT}, {VK_F9}, {VK_DECIMAL}, {VK_FINAL}, {VK_EXSEL},
{RMENU}, {VK_F3}, {VK_F2}, {VK_F1}, {VK_F7}, {VK_F6}, {VK_F5}, {VK_CRSEL},
{VK_SHIFT}, {VK_EREOF}, {VK_CANCEL}, {VK_DELETE}, {VK_HANGUL}, {VK_MBUTTON},
{VK_NUMLOCK}, {VK_CLEAR}, {END}, {VK_MENU}, {SPACE}, {BKSP}, {VK_INSERT},
{F18}, {F19}, {ESC}, {VK_MULTIPLY}, {F12}, {F13}, {F10}, {F11}, {F16},
{F17}, {F14}, {F15}, {F24}, {RIGHT}, {VK_F24}, {VK_CAPITAL}, {VK_LBUTTON},
{VK_OEM_CLEAR}, {VK_ESCAPE}, {UP}, {VK_DIVIDE}, {INS}, {VK_JUNJA},
{VK_F19}, {VK_EXECUTE}, {VK_PLAY}, {VK_RMENU}, {VK_F13}, {VK_F12}, {LWIN},
{VK_DOWN}, {VK_F17}, {VK_F16}, {VK_F15}, {VK_F14}

~ is a shorter alias for {ENTER}
```

- **Modifiers:**

`'+': {VK_SHIFT}`

`'^': {VK_CONTROL}`

`'%': {VK_MENU}` a.k.a. Alt key

```python
send_keys('^a^c') # select all (Ctrl+A) and copy to clipboard (Ctrl+C)
send_keys('+{INS}') # insert from clipboard (Shift+Ins)
send_keys('%{F4}') # close an active window with Alt+F4
```

Repetition count can be specified for special keys. `{ENTER 2}` says to press Enter twice.

演示如何按住或释放键盘上的一个键:

```python
send_keys("{VK_SHIFT down}"
          "pywinauto"
          "{VK_SHIFT up}") # to type PYWINAUTO

# 意思就是说，按住字母键是无效的
send_keys("{h down}"
          "{e down}"
          "{h up}"
          "{e up}"
          "llo") # to type hello
```

使用花括号来转义修饰符，并将保留符号输入为单个键:

```python
send_keys('{^}a{^}c{%}') # type string "^a^c%" (Ctrl will not be pressed)
send_keys('{{}ENTER{}}') # type string "{ENTER}" without pressing Enter key
```

For Windows only, pywinauto defaults to sending a virtual key packet (VK_PACKET) for textual input. For applications that do not handle VK_PACKET appropriately, the `vk_packet` option may be set to `False`. In this case pywinauto will attempt to send the virtual key code of the requested key. This option only affects the behavior of keys matching [-=[];’,./a-zA-Z0-9 ]. Note that upper and lower case are included for a-z. Both reference the same virtual key for convenience.

# Main User Modules

通常，并非所有这些匹配名称都同时可用。要检查指定对话框的这些名称，您可以使用`print_control_identifiers()` 方法。可能的“最佳匹配”名称显示为树中每个控件的 Python 列表。更详细的窗口规范也可以从方法输出中复制。

·`app.Properties.child_window(title="Contains:", auto_id="13087", control_type="Edit")`

## .findwindows

### .find_elements()

```python
pywinauto.findwindows.find_elements(class_name=None, class_name_re=None, parent=None, process=None, title=None, title_re=None, top_level_only=True, visible_only=True, enabled_only=False, best_match=None, handle=None, ctrl_index=None, found_index=None, predicate_func=None, active_only=False, control_id=None, control_type=None, auto_id=None, framework_id=None, backend=None, depth=None)
```

WARNING! Direct usage of this function is not recommended! It’s a very low level API. Better use Application and WindowSpecification objects described in the Getting Started Guide.

Possible values are:

- **class_name** Elements with this window class

  Inspect 中的 **ClassName**

- **class_name_re** Elements whose class matches this regular expression

- **parent** Elements that are children of this

- **process** Elements running in this process

  这个基本不用，每次启动进程都会变化

- **title** Elements with this text

  Inspect 中的 **Name** 属性

- **title_re** Elements whose text matches this regular expression

- **top_level_only** Top level elements only (default=**True**)

- **visible_only** Visible elements only (default=**True**)

- **enabled_only** Enabled elements only (default=False)

- **best_match** Elements with a title similar to this

- **handle** The handle of the element to return

- **ctrl_index** The index of the child element to return

- **found_index** The index of the filtered out child element to return

- **predicate_func** A user provided hook for a custom element validation

- **active_only** Active elements only (default=False)

- **control_id** Elements with this control id

- **control_type** Elements with this control type (string; for UIAutomation elements)

- **auto_id** Elements with this automation id (for UIAutomation elements)

   Inspect 中的 **AutomationId**

- **framework_id** Elements with this framework id (for UIAutomation elements)

- **backend** Back-end name to use while searching (default=None means current active backend)

# 使用

## 进阶用法

### 底层属性调用

```python
# region PATTERNS
AutomationElement = IUIA().ui_automation_client.IUIAutomationElement
DockPattern = IUIA().ui_automation_client.IUIAutomationDockPattern
ExpandCollapsePattern = IUIA().ui_automation_client.IUIAutomationExpandCollapsePattern
GridItemPattern = IUIA().ui_automation_client.IUIAutomationGridItemPattern
GridPattern = IUIA().ui_automation_client.IUIAutomationGridPattern
InvokePattern = IUIA().ui_automation_client.IUIAutomationInvokePattern
ItemContainerPattern = IUIA().ui_automation_client.IUIAutomationItemContainerPattern
LegacyIAccessiblePattern = IUIA().ui_automation_client.IUIAutomationLegacyIAccessiblePattern
MultipleViewPattern = IUIA().ui_automation_client.IUIAutomationMultipleViewPattern
RangeValuePattern = IUIA().ui_automation_client.IUIAutomationRangeValuePattern
ScrollItemPattern = IUIA().ui_automation_client.IUIAutomationScrollItemPattern
ScrollPattern = IUIA().ui_automation_client.IUIAutomationScrollPattern
SelectionItemPattern = IUIA().ui_automation_client.IUIAutomationSelectionItemPattern
SelectionPattern = IUIA().ui_automation_client.IUIAutomationSelectionPattern
SynchronizedInputPattern = IUIA().ui_automation_client.IUIAutomationSynchronizedInputPattern
TableItemPattern = IUIA().ui_automation_client.IUIAutomationTableItemPattern
TablePattern = IUIA().ui_automation_client.IUIAutomationTablePattern
TextPattern = IUIA().ui_automation_client.IUIAutomationTextPattern
TogglePattern = IUIA().ui_automation_client.IUIAutomationTogglePattern
TransformPattern = IUIA().ui_automation_client.IUIAutomationTransformPattern
ValuePattern = IUIA().ui_automation_client.IUIAutomationValuePattern
VirtualizedItemPattern = IUIA().ui_automation_client.IUIAutomationVirtualizedItemPattern
WindowPattern = IUIA().ui_automation_client.IUIAutomationWindowPattern
# endregion
```

如果需要获取 `LegacyIAccessible` 开头的一系列字段，可以使用此方法

`ctrl.legacy_properties()`

返回一个字典：

```
{'ChildId': 0,
 'DefaultAction': '',
 ...,
 'Description': '',
 'Help': ''}
```

但是其他属性并没有这么方便的接口调用，但是源码中预留了调用方法。

```python
def iface_expand_collapse(self)
def iface_selection(self)
def iface_selection_item(self)
def iface_invoke(self)
def iface_toggle(self)
def iface_text(self)
def iface_value(self)
def iface_range_value(self)
def iface_grid(self)		*
def iface_grid_item(self)
def iface_table(self)
def iface_table_item(self)
def iface_scroll_item(self)
def iface_scroll(self)
def iface_transform(self)
def iface_transformV2(self)
def iface_window(self)
def iface_item_container(self)
def iface_virtualized_item(self)
```

以 `def iface_grid(self)` 为例：

`ctrl.iface_grid` 返回一个对应的对象 `GridPattern`

- **dir(Pattern)**

  查看对象的`key`：

  ```python
  dir(ctrl.iface_grid)
  
  ['AddRef',
   'CachedColumnCount',
   'CachedRowCount',
   'CurrentColumnCount',
   ....
   'CurrentRowCount',
   'GetItem',
   'QueryInterface',
   'Release',
   '_AddRef']
  ```

- **getattr(ctrl.iface_grid, "prop")**

  获取属性对应的值

  ```python
  getattr(VTable.iface_grid, "CurrentColumnCount")
  
  3
  ```

  

# 案例

## 记事本

```python
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
```



# API

[github源码地址](https://github.com/pywinauto/pywinauto)

[参考文档](https://www.kancloud.cn/gnefnuy/pywinauto_doc/1193035)

## 常用接口

```python
from pywinauto.application import Application

# Tips:
# 1: win32[] 调用的是 ClassName， uia[] 调用的是 Name
# 2: print_control_identifiers:  - "Title" 坐标
# 3: dlg.window_text() 获取标题， dlg.texts() 获取文本

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
dlg.children(**kwargs) # 只查找一层，返回符合条件的子元素列表,支持索引，是BaseWrapper对象（或子类）
dlg.descendants(**kwargs) # 返回符合条件的所有后代元素列表,是BaseWrapper对象（或子类）,很多函数无法调用
dlg.iter_children(**kwargs) # 符合条件后代元素迭代器，是BaseWrapper对象（或子类）, 测试是 app 整个符合条件的子类
list(dlg.iter_children(**kwargs))	# 很方便使用
dlg.child_window()	# 不管层级查找

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
```

## Inspect字段获取方式

`WindowSpecification` 继承于 `Wrapper` 控件， `WindowSpecification` 可调用函数更为丰富

主要多出：window() 、 child_window() 、 wait()、exists() 等封装过的函数。

### 常见、易获取字段

![image-20220805171305030](https://s2.loli.net/2022/08/05/AVxDlOvcHGqZUfk.png)

以 box 为这个控件为例

- **get_properties()**

可以获取这个控件比较容易获取的属性：`box.get_properties()`

```python
{'class_name': 'QComboBox',
 'friendly_class_name': 'ComboBox',
 'texts': ['Browse',
  'profile1-film-1000nm.txt',
  'profile1-film-25nm.txt',
  'oclibrary.oclib'],
 'control_id': None,
 'rectangle': <RECT L2479, T100, R2779, B130>,
 'is_visible': True,
 'is_enabled': True,
 'control_count': 1,
 'is_keyboard_focusable': True,
 'has_keyboard_focus': False,
 'automation_id': ''}

# 比如需要查看 class_name:
box.class_name()	# 'QComboBox'
```

- **legacy_properties()**

此方法返回一个字典：`box.legacy_properties()`

```python
{'ChildId': 0,
 'DefaultAction': '按',
 'Description': '',
 'Help': '',
 'KeyboardShortcut': 'Down',
 'Name': 'cboProfile',
 'Role': 46,
 'State': 1048576,
 'Value': 'profile1-film-25nm.txt'}

# 获取 LegacyIAccessible 一系列的值
box.legacy_properties().get('Value')		# 'profile1-film-25nm.txt'
```

- **_control_types**

查看控件类型： `box._control_types`

```python
box._control_types		# ['ComboBox']
box._control_types[0]	# 'ComboBox'
```

- **Name**

Name:	"cboProfile"

`box.window_text()` : cboProfile

- **AutomationId**

AutomationId:	""

`box.automation_id()` : ''

- **ClassName**

ClassName:	"QComboBox"

`box.class_name()` : QComboBox

- **BoundingRectangle**

BoundingRectangle:	{l:2479 t:100 r:2779 b:130}

`box.rectangle()` :  <RECT L2479, T100, R2779, B130>

```python
print(box.wrapper_object().rectangle())  # (L2479, T100, R2779, B130)
rect = box.wrapper_object().rectangle()

# rect 函数一览
rect.left		# 2479 
rect.right		# 2779
rect.top		# 100
rect.bottom		# 130
rect.width()	# 300
rect.height()	# 30
rect.mid_point()	#  <pywinauto.win32structures.POINT at 0x1f4cbb7c340>
rect.mid_point().x		# 2629
rect.mid_point().y		# 115
```

### 另外一种实现方式： element_info

![image-20220805171305030](https://s2.loli.net/2022/08/05/AVxDlOvcHGqZUfk.png)

还是以 box 为例

这个调用很贴切 Inspect

```python
box.element_info			#  <uia_element_info.UIAElementInfo - 'cboProfile', QComboBox, None>
type(box.element_info)		# pywinauto.uia_element_info.UIAElementInfo
.name				# 'cboProfile'
.framework_id		# 'Qt'
.automation_id		# ''
.rectangle			# <RECT L2479, T100, R2779, B130>
.class_name			# 'QComboBox'
.control_type		# 'ComboBox'
.process_id			# 13780
```

## 控件的 Action

- **ComboBox**

```python
# ControlType:  UIA_ComboBoxControlTypeId (0xC353)
ComboBox.select(item: str)		# 直接选中(只能操作当前页面存在的Item)
ComboBox.expand()		# 展开
ComboBox.collapse()		# 收回
ComboBox.is_expanded()		# 判断是否展开
ComboBox.is_collapsed()		# 判断是否收回
ComboBox.is_enabled()		# 是否可用
```

