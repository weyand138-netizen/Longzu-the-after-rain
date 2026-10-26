# 雨停之后

[English](README_EN.md) · [游戏版本发布页](https://github.com/weyand138-netizen/Longzu-the-after-rain/releases) · [全部版本](docs/versions.md) · [反馈与联系](SUPPORT.md)

《雨停之后》是一部免费、非商业的《龙族》非官方同人视觉小说。

玩家以路明非的有限视角，陪绘梨衣度过七天。在观察、询问、准备与承担中作出选择，让每一次回应都留下后续的回响，并走向六种不同的结局。

制作：**Andwey** · 游戏语言：**简体中文** · 目标平台：**Windows 10 / 11 x86-64**

## 下载与版本

**[下载 Windows RC.1 游戏包](https://github.com/weyand138-netizen/Longzu-the-after-rain/releases/tag/v1-rc.1-local-20261024)** · [游戏版本发布页](https://github.com/weyand138-netizen/Longzu-the-after-rain/releases) · [全部版本与下载索引](docs/versions.md)

当前公开版本为 `1-rc.1-local-20261024`，仍是 RC 预发布候选，正式版尚未公开。具体内容、已知问题和文件校验值见对应 Release。

下载 Release 附件中的 **Windows 游戏 ZIP**，完整解压后启动，无需安装 Python 或 Ren'Py。当前 RC.1 的程序名为 `雨停之后.exe`；早期公开测试版为 `After rain.exe`，以所下载版本的说明为准。GitHub 的 `Source code` ZIP/TAR 是源码归档，不是独立游戏包。

升级前请保留旧目录和存档。安装、兼容范围与升级帮助见[常见问题](docs/faq.md)。

## 游戏内容概述

故事从雨中的站台开始。你将陪绘梨衣走过七天，在短暂的日常与逐渐展开的真相之间，留意她写下的话、递来的物件和沉默中的反应。

何时解释，何时等待，怎样为接下来的路做准备，都由你作出选择。此前的回应会在后续情节中留下回响，最终形成不同的去向。

- 从序章到 Day 7 的七日故事。
- 六个由选择与准备决定的结局，以及各自对应的尾声。
- 18 张结局事件 CG，与章节背景、角色动作共同呈现故事。
- 背景音乐、环境声与剧情音效。
- 存档、读档、回退、快进和自动阅读。
- 字体缩放、高对比、减少动态效果与自朗读相关设置。

游戏目前没有角色配音。部分结局包含离别和情绪较沉重的描写；分享截图或讨论结局时，请标注剧透。

[当前版本发布说明](https://github.com/weyand138-netizen/Longzu-the-after-rain/releases/tag/v1-rc.1-local-20261024) · [正式版介绍草案](docs/releases/v1.0.0.md) · [English release notes](docs/releases/v1.0.0_EN.md)

游戏可离线游玩，反馈由玩家自行通过邮箱或 GitHub 提交。具体设备支持范围以所下载版本的发布说明为准。

<details>
<summary>从源码构建（开发者）</summary>

使用 [Ren’Py 8.5.3 官方 SDK](https://www.renpy.org/release/8.5.3)打开本项目并构建 Windows ZIP，再用公开打包脚本生成玩家包：

```console
python scripts/package-player-windows.py --input After-Rain-v1-rc.1-local-20261024-win.zip --sdk-zip renpy-8.5.3-sdk.zip --output 雨停之后-Windows.zip
```

脚本会核验官方 SDK ZIP 的 SHA-256，使用原始官方启动器，将入口命名为 `雨停之后.exe`，并移除随包说明和测试材料。游戏代码与资源保持构建产物身份；运行所需引擎、字体许可证继续保留。

</details>

## 反馈与联系

**反馈邮箱：[weyand138@gmail.com](mailto:weyand138@gmail.com)**

也可以通过 [GitHub Issues](https://github.com/weyand138-netizen/Longzu-the-after-rain/issues) 报告问题。

邮件标题建议：`[雨停之后][版本号][问题类型] 简短描述`。请附上版本、章节、复现步骤及相关截图；完整反馈格式见 [SUPPORT.md](SUPPORT.md)。

[已知问题](docs/known-issues.md) · [更新日志](CHANGELOG.md)

## 支持作品

如果你喜欢《雨停之后》，欢迎给仓库点一个 **Star**，将仓库或 Release 链接分享给感兴趣的朋友，或留下具体的游玩反馈。

帮助发现错字、流程问题和阅读体验问题，就是对作品的支持。分享时请注明版本，并为结局内容标注剧透。

本项目保持免费、非商业，不设置赞助、打赏、付费解锁或付费内容。

## 内容与授权

本作是《龙族》非官方同人作品，与原作者、出版社及任何官方授权方无关。原作人物与世界观的相关权利属于各自权利人。

游戏文本、原创 UI、图像及音频等内容的使用以仓库 [LICENSE](LICENSE) 和各文件声明为准；第三方内容仍受各自条款约束。仓库公开不代表授予商业复用或自由再分发许可。

如需反馈署名、内容来源或权利相关问题，请联系 [weyand138@gmail.com](mailto:weyand138@gmail.com)。

**AI 制作说明**：本项目在制作过程中使用了生成式 AI 和 AI 辅助工具，涉及文案构思与整理、程序开发及测试辅助、部分美术素材生成与处理等环节；音频制作也使用了程序合成等工具。项目内容并非全部由纯手工制作。制作人负责内容取舍、编辑整合与最终发布决定；原作及第三方材料的权利声明仍然适用。

