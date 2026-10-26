# 雨停之后

《龙族》免费、非商业、非官方同人视觉小说。制作：Andwey。

## 下载与游玩

[下载 Windows RC.1 游戏包](https://github.com/weyand138-netizen/Longzu-the-after-rain/releases/tag/v1-rc.1-local-20261024) · [全部版本](https://github.com/weyand138-netizen/Longzu-the-after-rain/releases)

完整解压 Release 的 Windows ZIP，双击 `雨停之后.exe`。无需另外安装 Python 或 Ren’Py，并请保留同目录的运行文件。目标平台为 Windows 10/11 x86-64，本轮实际启动验证在 Windows 11 完成。

当前内容包含序章至 Day 7、六个结局及 18 张结局 CG。当前版本为 `1-rc.1-local-20261024`；修复说明、已知问题和文件校验值见对应 Release。原存档格式和目录标识继续沿用。

## 从源码构建

使用 [Ren’Py 8.5.3 官方 SDK](https://www.renpy.org/release/8.5.3)打开本项目并构建 Windows ZIP，再用公开打包脚本生成玩家包：

```console
python scripts/package-player-windows.py --input After-Rain-v1-rc.1-local-20261024-win.zip --sdk-zip renpy-8.5.3-sdk.zip --output 雨停之后-Windows.zip
```

脚本会核验官方 SDK ZIP 的 SHA-256，使用原始官方启动器，将入口命名为 `雨停之后.exe`，并移除随包说明和测试材料。游戏代码与资源保持构建产物身份；运行所需引擎、字体许可证继续保留。

## 问题反馈与许可

请在 [Issues](https://github.com/weyand138-netizen/Longzu-the-after-rain/issues) 记录版本、章节或路线、复现步骤、设备信息和截图或错误信息。

当前为 RC 候选。完整人工体验、中文自朗读实听和目标硬件验证仍有待完成；本轮跳过长时间稳定性测试。软件测试结果不代表这些项目已经获得人工验收。

本作与原作者、出版社及任何官方授权方无关联。项目原创内容的使用条件见 `LICENSE`；第三方软件及字体遵循其各自许可证。
