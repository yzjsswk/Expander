这是一款命令式代码(文本)召唤器，能够在Windows平台任何可以输入的地方通过预设的命令召唤你的代码...

#### 注意

* 由于本召唤器是作者为了自用而开发，因此并未考虑程序健壮性，请在输入命令的时候尽量一气呵成，而不要换行或者切换窗口之类的，否则可能导致奇奇怪怪的行为！（如果输完没有反应，那就删了重输吧！）

* 本召唤器需要使用系统剪切板，请在使用前保存好你的剪切板内原来的内容！

#### 使用说明

* 命令配置
  * 命令保存在根目录下的commands(关键路径，不可更改)文件夹内。
  * commands文件夹下的一级文件夹是命令组(或命名空间)，同一个命令组内的命令名不可重复，不同命名组内的命令名可以重复。一级文件夹名作为命令组名，只允许使用大小写英文和数字，在切换命令组时需要用到。
  * 命令组文件夹内二级及以上文件夹可以自由创建用于对命令进行分类，文件夹名没有要求。
  * 一个命令由一个txt格式的文件定义，你可以在二级及以上文件夹内任意添加自己的命令，命令文件名没有要求。
  * 命令文件的第一行定义了命令名，剩余部分作为展开体。以##开头的行作为注释行，会被忽略。一个命令的展开体中允许放置一些{id}格式的参数，在调用命令时可以进行填充。
  * 默认的commands文件夹中给出了一些例子供参考。
* 使用命令
  * 任何可以输入文本的地方都可以调用命令。
  * 使用@@@+命令组名+空格切换命令组。程序不会自动加载默认命令组，因此你启动程序后的第一件事是主动加载一个命令组。
  * 使用@@+命令名+空格调用命令。
  * 如果展开体中有参数，使用@@+命令名+\_+参数1+\_+参数2+...+空格的形式来填充展开体中参数。你也可以不输入参数，展开后手动填充。
  * 内置命令: @@version 查看当前版本，@@exit退出程序。
  * 预设命令: commands/yzjsswk是作者的使用习惯，如果你想使用可以参考commands/yzjsswk/yzjsswk.md。

#### 已知问题

* 使用的按键检测库没法检测右边3x3那块的数字按键，所以只能使用键盘上面那个一行的来输入数字。
* 有缩进的时候进行展开，后面的行不能自动跟着缩进。暂时没有想到什么好的解决办法。
