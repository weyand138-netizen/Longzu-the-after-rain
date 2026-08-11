# Ren'Py 8.5.3 Windows 构建能力 Spike

状态：`CONFIRMED WITH BOUNDARIES`  
验证日期：2026-08-09  
关闭目标：`BUILD-Q1`、`ENG-01`  
范围：只验证 Windows 构建能力；不实现 SYS-BUILD 完整发布流水线，不修改游戏设计语义。

## 结论

仓库内固定的 Ren'Py 8.5.3 Windows SDK 可以通过 CLI 生成可运行的 Windows ZIP 包。可复用入口为：

```text
工作目录：E:\Longzu\.tools\renpy-8.5.3-sdk
命令：renpy.exe launcher distribute --destination <output> --package win --format zip --no-update <project>
```

`launcher` 是 `basedir` 参数，`distribute` 是 launcher 注册的命令，`<project>` 是最后的项目路径参数。工作目录必须使 `launcher` 能解析到 SDK 下的 `launcher` 目录；本次实测使用 SDK 根目录。CLI 探针和完整帮助输出保存在 [distribute-help stdout](evidence/2026-08-09-build-q1-spike/cli-probes/distribute-help/stdout.txt)。

版本探针输出为 `Ren'Py 8.5.3.26051504`，对应固定版本 8.5.3。版本化能力清单见 [capability-manifest-v1.json](capability-manifest-v1.json)。

## CLI 与参数

已实测的构建参数：

| 参数 | 作用 | Spike 结论 |
|---|---|---|
| `--destination` / `--dest` | 输出目录 | 可用；成功包直接写入该目录 |
| `--package` | 选择 `build.package` 声明 | Windows-only 包使用 `win` |
| `--format` | 强制包格式 | `zip` 可用；未知格式触发构建失败 |
| `--no-update` | 禁止生成 updater/update 产物 | 本次使用 |
| `--packagedest` | 指定单个包的无扩展名路径 | 已由 help/源码核对，未作为主场景展开 |
| `--no-archive` | 不将文件放入 Ren'Py archive | 已由 help/源码核对，未作为主场景展开 |
| `--macapp` | 指定 macOS app | 非 Windows 范围 |

项目中的 Windows 包声明必须把 Windows runtime 文件列表纳入包。本次夹具使用：

```renpy
build.package("win", "zip", "windows renpy all")
```

仅使用 `all` 会得到缺少 Windows executable/runtime 的不完整 ZIP；这是构建配置约束，不是发布流水线实现。

Lint 入口为：

```text
renpy.exe <project> lint [--compile]
```

## 退出码与场景

最终实测结果如下。`中断`与`超时`指本次监督器对 launcher 及其扫描子进程执行的 Windows 进程树终止，不等同于尚未实测的控制台 Ctrl+C。

| 场景 | 实际命令 | 退出码 | 输出包 | 临时目录 | 原始证据 |
|---|---|---:|---|---|---|
| lint 成功 | `<project> lint --compile` | `0` | 无 | 保留 | [result](evidence/2026-08-09-build-q1-spike/cases/lint-success/result.json) |
| Windows 构建成功 | `launcher distribute ... --package win --format zip --no-update` | `0` | 1 个 ZIP | 保留 | [result](evidence/2026-08-09-build-q1-spike/cases/build-success/result.json) |
| lint 失败 | `<project> lint`，故意缺少 `:` | `1` | 无 | 未创建 | [stdout](evidence/2026-08-09-build-q1-spike/cases/lint-failure/stdout.txt) |
| 构建失败 | `--format not-a-real-format` | `1` | 无 | 保留 | [stdout](evidence/2026-08-09-build-q1-spike/cases/build-failure-invalid-format/stdout.txt) |
| 中断 | 1500 ms 后进程树终止 | `-1` | 无 | 保留 | [result](evidence/2026-08-09-build-q1-spike/cases/interrupted/result.json) |
| 超时 | 2500 ms 超时后进程树终止 | `-1` | 无 | 保留 | [result](evidence/2026-08-09-build-q1-spike/cases/timeout/result.json) |

`-1` 是本次 Windows/.NET `Process.Kill()` 监督器观察到的终止进程退出码；Ren'Py 没有在该场景返回自己的“超时”或“取消”业务码。实现监督器时应保留 `timed_out` / `externally_terminated` 语义，不能把 `-1` 静默映射为成功。

## stdout、stderr 与日志

Ren'Py 的 TextReporter 和异常传播都出现在 stdout：

- 成功构建 stdout 包含 `Scanning project files...`、`Scanning Ren'Py files...`、包写入进度和 `All packages have been built.`。
- lint 失败 stdout 包含 `game/broken.rpy` 的语法定位。
- 构建失败 stdout 包含 `Exception: Format 'not-a-real-format' is unknown.` 及 traceback。
- 最终六个场景的 stderr 均为空；原始文件仍分别保留在每个 case 下的 `stdout.txt` 和 `stderr.txt`。
- 设置 `RENPY_LOG_BASE` 后每个 case 生成 `logs/log.txt`。日志是 stdout/stderr 之外的副本/内部运行日志，并不替代 stdout。
- 构建过程另外写入 SDK 临时目录中的 `tmp/<project>/distribute.txt`。失败和进程树终止后该文件仍存在；中断/超时场景中它为 0 字节。

代表性原始文件： [成功 stdout](evidence/2026-08-09-build-q1-spike/cases/build-success/stdout.txt)、[成功 log](evidence/2026-08-09-build-q1-spike/cases/build-success/logs/log.txt)、[失败 stdout](evidence/2026-08-09-build-q1-spike/cases/build-failure-invalid-format/stdout.txt)、[中断 distribute.txt](evidence/2026-08-09-build-q1-spike/cases/interrupted/distribute.txt)。

## 输出目录与 Windows 包格式

成功 case 的 `--destination` 目录只产生一个包：

```text
renpy-build-spike-0.0.1-win.zip
```

实测大小为 30,950,699 bytes，SHA-256 为 `4e3d7ce35e30312512c3840410482d5ac0c130b89929e7d250c61948d4764943`。ZIP 根目录为 `renpy-build-spike-0.0.1-win/`，包含：

- `renpy-build-spike.exe`；
- `lib/py3-windows-x86_64/` 下的 `python.exe`、`pythonw.exe`、`libpython3.12.dll`、SDL/OpenGL 及其他 Windows runtime；
- `game/cache/bytecode-312.rpyb`、`py3analysis.rpyb`、编译后的 `.rpyc`；
- `renpy/` runtime 和 `renpy-build-spike.py`。

完整 ZIP 成员清单及大小见 [zip-list](evidence/2026-08-09-build-q1-spike/cases/build-success/renpy-build-spike-0.0.1-win.zip-list.txt)，输出树与 SHA-256 见 [output-tree-after](evidence/2026-08-09-build-q1-spike/cases/build-success/output-tree-after.txt)。实际 ZIP 二进制也保留在该 case 的 `artifacts/` 目录中。

## 中断、超时与残留

slow fixture 在 Ren'Py 初始化阶段等待 30 秒，用于让监督器有机会终止 launcher 拉起的扫描子进程。只终止顶层 PID 不可靠：首次尝试中 launcher 子进程继续完成构建；最终 runner 已改为按父子关系递归终止进程树，并以空的匹配进程快照作为收敛条件。

最终中断和超时行为一致：

- stdout 只保留 `Scanning project files...` 的前缀；stderr 为空；
- 输出目录为空，没有半成品 ZIP；
- SDK `tmp/<project>/` 仍保留；
- `distribute.txt` 被创建但为 0 bytes；
- case 结束后的匹配 Ren'Py 进程快照为空；
- `result.json` 保留实际 kill 时间、退出码、输出文件数和临时目录存在性。

这意味着后续 SYS-BUILD 若加入超时/取消，必须把进程树清理、SDK `tmp` 清理策略和残留包隔离作为显式控制项；Ren'Py CLI 本身不会替调用方清理这些残留。

## 证据与复跑

最终原始证据根目录：[evidence/2026-08-09-build-q1-spike/](evidence/2026-08-09-build-q1-spike/)。每个 case 均保留：

```text
command.txt              实际 executable、参数、工作目录、环境和超时设置
stdout.txt / stderr.txt  原始标准输出与错误输出
logs/log.txt             RENPY_LOG_BASE 下的 Ren'Py 日志
distribute.txt           SDK tmp 下的构建日志副本（若已创建）
result.json              退出码、时间、进程控制和产物摘要
output-tree-*.txt        产物路径、大小、mtime、SHA-256
sdk-tmp-*.txt            SDK 临时目录快照
*.zip-list.txt           ZIP 成员路径、未压缩大小、压缩大小
```

可复跑 runner：[tools/spike-renpy-build.ps1](../../../tools/spike-renpy-build.ps1)。它生成隔离夹具，不写入 `game/`；如要重复运行，请传入新的 `-EvidenceRoot`，避免覆盖原始证据。

## 边界

本 Spike 没有实现 source/catalog/asset/legal manifest、candidate identity、release evidence binding、archive closure 或发布归档，也没有改变任何游戏设计语义。它只为 `BUILD-Q1` 提供可执行的 Ren'Py Windows 构建事实，为 `ENG-01` 提供版本化 engine capability manifest。
