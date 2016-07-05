# 开机自动登陆 IP网关

## 安装
- 本脚本需要`Python3`运行环境

  > 请搜索Python官网，在Download页面选择下载Python3.5的Windows版本的安装包安裝

  > 安裝完成后將python及pip的路径添加到系统的Path变量中

  > 使用命令 `pip install requests` 安装requests

- 在本地新建文件夹，将本目录中的文件保存到文件夹中

## 配置

- 用文本编辑器打开`ipgw.bat`, 将`<your-username>`和`<your-password>`部分替换为你自己的校园网账号和密码

  > 本脚本只是代为登陆，不会上传或保存你的密码

- 使用快捷键`Win+R`打开运行，输入`taskschd.msc`回车，打开`Task Scheduler`。

 ![截图](img/screen.png)

- 点击`Task Scheduler Library`，在右侧点击`Create task...`
- 在`General`标签下填写`name`(如`LoginIPGW`)
- 切换到`Trigger`标签下，点击`New`,`Begin the Task` 选择 `At log on`。`Advanced Settings`下勾上`Delay task for`，输入`15 seconds`，点击`OK`
- 切换到`Action` 标签下，点击`New`, 在`Program/script`中点击`Browse`，找到下载的`ipgw.bat`文件。在`Add arguments`中输入`-i`,点击 `OK`
- 配置完成

## 说明

暂无