<!-- VERTICAL SLICE - NOT FOR PRODUCTION -->
<!-- Validation Question: Can a new player feel that care means observing, asking, and accepting shared cost within five minutes without guidance, and can one such loop be produced in one build day at representative quality? -->
<!-- Date: 2026-07-23 -->

# 《雨停之后》垂直切片

这是独立验证工程，不是正式游戏代码。正式工程不得从本目录导入或复制实现。

## 启动

从仓库根目录执行：

```powershell
$env:APPDATA='E:\Longzu\.renpy\appdata'
& 'E:\Longzu\.tools\renpy-8.5.3-sdk\lib\py3-windows-x86_64\python.exe' `
  'E:\Longzu\.tools\renpy-8.5.3-sdk\renpy.py' `
  'E:\Longzu\prototypes\rain-after-vertical-slice' run `
  --savedir 'E:\Longzu\.renpy\slice-saves'
```

也可把 `prototypes` 添加为 Ren'Py Launcher 项目目录后选择本项目。

## 验证

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File .\prototypes\rain-after-vertical-slice\tools\run-tests.ps1
```

详细范围见 [SCOPE.md](SCOPE.md)，素材来源见 [ASSET-SOURCES.md](ASSET-SOURCES.md)。

