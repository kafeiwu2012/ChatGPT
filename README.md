# Windows 离线便携博客

适用于 Windows 10 / 11 64 位。自带 Python 运行环境，日常使用无需联网，无需安装数据库或 Python。

## 下载和启动

**推荐：**打开仓库内的 [PortableBlog-Windows-x64.zip](./PortableBlog-Windows-x64.zip)，点击 GitHub 文件页面的 **Download raw file（下载原始文件）** 按钮，下载约 14 MB 的便携包。

也可以使用仓库的 **Code → Download ZIP** 下载整个仓库。下载后完整解压，使用其中的 `PortableBlog` 文件夹即可。

1. 将完整 `PortableBlog` 文件夹放到 `E:\PortableBlog` 或任意可写目录。
2. 双击 `启动博客.bat`，保持启动窗口开启。
3. 浏览器会自动打开；若未打开，请输入启动窗口显示的本地地址（默认 `http://127.0.0.1:8765`）。
4. 点击“管理后台”，首次设置至少 8 位密码。

## 功能

- 纯文本文章、草稿与发布、标题和正文搜索。
- 图片、视频、音频、PDF / TXT 附件存储与下载，单个文件最大 1GB。
- 年月归档、类目管理、媒体库。
- 后台配置菜单名称、顺序及目标，以及博客名称、副标题、主题色和背景色。
- 密码修改与数据 ZIP 备份。

视频播放依赖浏览器支持，推荐 MP4（H.264/AAC）；其他编码可保存下载，但不保证直接播放。

## 整目录迁移

先保存内容并关闭启动窗口，再复制**整个 PortableBlog 文件夹**到另一台 Windows 10/11 64 位电脑，双击启动即可。路径和盘符可以改变。

`data` 文件夹在首次运行时自动创建，包含文章、媒体、设置和密码校验信息。请勿删除，切勿在运行中直接复制。后台密码不对磁盘文件加密；数据备份应妥善保管。

详细操作见 [使用说明](./PortableBlog/使用说明.txt)，测试范围及限制见 [验证记录](./PortableBlog/验证记录.txt)。

## 验证范围

已在 Linux 云端用同一应用代码和 Chromium 验证文章、上传、视频播放、后台设置、访问控制及跨目录备份恢复。尚未在真实 Windows 系统执行自带 python.exe 或双击 BAT，需要在目标电脑确认启动。

## 运行环境来源

Python Software Foundation 发布的 Python 3.12.10 Windows x64 NuGet 包，运行环境许可见 `PortableBlog/runtime/LICENSE.txt`。应用仅使用 Python 标准库和本地页面，无 CDN 或云服务依赖。

便携包 SHA-256：

`6936b52a5abd3cda80658ff73791bfd53856c04bcfe980d6fc5e264bfe03626a`
