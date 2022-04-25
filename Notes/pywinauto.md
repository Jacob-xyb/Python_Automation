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