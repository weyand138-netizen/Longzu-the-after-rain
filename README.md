# 雨停之后

《龙族》非官方同人视觉小说。玩家以路明非的有限视角，陪绘梨衣度过七天，并通过持续的理解、尊重与准备改变故事走向。

基于 Ren'Py 8.5.3 开发，当前仓库包含可玩的序章至 Day 7、六个确定性结局、无障碍设置，以及运行所需的原创图像资源。

> 本项目为免费、非商业、非官方同人作品，与原作者、出版社及任何官方授权方无关。项目不复制原著段落，不使用官方插画、音乐、Logo 或游戏素材。

## 当前状态

项目处于制作阶段。仓库已包含：

- Ren'Py 8.5.3 工程骨架；
- 五条隐藏因果轴与确定性结局判定；
- 从序章《从雨里逃走》到 Day 7 的完整七日主线；
- 六个由既有选择与状态确定的结局；
- 11 项独立本地成就目录（结局与章节回忆使用各自收藏记录）；
- 纯 Python 结局逻辑测试和 Ren'Py 自动流程测试；
- GDD、架构、控制清单和会话状态。

## 本地运行

1. 下载并解压 Ren'Py 8.5.3 SDK。
2. 在 Ren'Py Launcher 中把项目目录设为本仓库的父目录，选择 `雨停之后`。
3. 点击“启动项目”。仓库不包含 Ren'Py SDK、缓存或存档；SDK 由本机安装提供。

也可从 SDK 根目录执行：

```powershell
.\lib\py3-windows-x86_64\python.exe renpy.py E:\Longzu run
```

## 验证

在已安装并解压 Ren'Py 8.5.3 SDK 的前提下，可从仓库根目录运行：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\run-renpy-tests.ps1 -Suite global
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\tools\test-content-constraints.ps1
```

内容硬约束：绘梨衣不能进行完整口语对白。她只能通过肢体语言、视线、物件操作或“嗯”等简单单音节回应；该约束由上述内容检查脚本覆盖。

## 仓库说明

- 项目定位：免费、非商业的同人视觉小说原型与开发资料库；
- 运行时：Ren'Py 8.5.3；
- 发布范围：仅提交原创代码、原创文本、经登记的素材与可复现的验证证据；本机 SDK、缓存、存档和日志均不纳入版本控制；
- 相关声明：详见 [非商业同人作品声明](docs/legal/fan-work-notice.md) 与 [素材登记表](docs/legal/asset-register.md)。

## 内容与授权

- 制作人署名：Andwey
- 游戏文本、原创 UI、原创测试代码：权利保留，未授予商业复用许可。
- 通用框架未来会与衍生内容拆分后单独以 MIT 许可证发布。
- 第三方素材必须先登记在 `docs/legal/asset-register.md`，再进入发布包。
