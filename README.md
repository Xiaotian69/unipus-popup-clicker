# Unipus Popup Clicker

> 一个在本机运行的 Playwright 小工具：打开学习页面后，持续检测常规通知弹窗，并自动点击“确定”。
>
> A small local Playwright utility that opens a page in Chromium and clicks a routine notification button (default: `确定`) whenever it appears.

![Unipus Popup Clicker](docs/assets/hero.png)

**它只做一件事：** 在页面及其内嵌框架中查找文字匹配的可见按钮并点击。它不会代替你学习、答题、计时或登录，也不是完整的学习平台自动化工具。

## 功能说明

- 使用本地 Chromium 打开目标页面（默认是代码中预置的一个 Unipus 课程页面，可用 `--url` 换成你自己的页面）。
- 每隔 `--poll-seconds` 秒，在所有打开的标签页及其 iframe 中查找文字为 `--button-text` 的可见按钮，点击第一个匹配项。
- 登录态保存在本地持久化浏览器目录 `.browser-profile/`，下次启动无需重复登录。
- 运行日志写入 `logs/popup_clicker.log`。
- 按 <kbd>Ctrl</kbd>+<kbd>C</kbd> 停止。

如果网站要求登录，请在弹出的浏览器窗口中**手动完成**。程序不会索取、填写或保存账号密码。

## 使用边界

- 本项目与 Unipus（U 校园）无隶属、认可或维护关系。
- 仅用于确认你有权使用的页面中的常规通知弹窗。
- 请遵守网站规则以及课程或学校的要求；不要用它绕过考勤、规定学习时长、测评、访问控制或反自动化措施。
- 工具按文字匹配按钮，请使用足够明确的按钮文字，并在长时间运行前确认目标页面无误。

## Windows 快速开始

需要 Windows、Python 3.10+；首次安装依赖与 Chromium 时需要联网。

1. 克隆或下载本仓库。
2. 双击 `setup_windows.bat`：创建 `.venv`、安装依赖与 Chromium，并运行单元测试。
3. 双击 `run_windows.bat`：使用默认设置启动（打开代码中预置的页面）。
4. 如页面要求登录，在 Chromium 窗口中手动登录。
5. 保持浏览器和命令行窗口打开；在命令行窗口按 <kbd>Ctrl</kbd>+<kbd>C</kbd> 停止。

要打开其他页面，请改用命令行并传入 `--url`（见下文）。

## 命令行使用

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m playwright install chromium

.\.venv\Scripts\python.exe popup_clicker.py `
  --url "https://example.com/your-page" `
  --button-text "确定" `
  --poll-seconds 5
```

## 参数

| 参数 | 说明 | 默认值 |
| --- | --- | --- |
| `--url` | 要打开并监视的页面 | 代码中预置的 Unipus 课程页面 |
| `--button-text` | 要点击的按钮文字；备用选择器可能匹配包含该文字的元素 | `确定` |
| `--poll-seconds` | 两次检查的间隔秒数，最小为 `1` | `5` |
| `--profile-dir` | 本地持久化 Chromium 配置目录 | `.browser-profile` |
| `--log-dir` | `popup_clicker.log` 所在目录 | `logs` |
| `--headless` | 无窗口运行；此模式下无法手动登录 | 关闭 |

## 本地数据与隐私

运行状态默认只保存在你的电脑上，以下目录均已被 `.gitignore` 排除：

- `.browser-profile/`：持久化浏览器配置，可能包含 Cookie 等敏感会话数据，请勿分享。
- `logs/`：记录启动、目标网址、点击与停止等事件。
- `.venv/`、`.pytest_cache/`、`__pycache__/`：本地依赖与缓存。

## 测试

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

如需安全地手动验证，可使用仓库内完全本地的[合成通知页面](docs/assets/demo/notification-fixture.html)（无登录、无外部资源、无网络请求）：

```powershell
# 窗口 1：启动本地静态服务
.\.venv\Scripts\python.exe -m http.server 8765 --directory docs/assets/demo

# 窗口 2：让工具监视该页面
.\.venv\Scripts\python.exe popup_clicker.py `
  --url "http://127.0.0.1:8765/notification-fixture.html" `
  --poll-seconds 1 `
  --profile-dir ".browser-profile/demo" `
  --log-dir "logs/demo"
```

工具点击“确定”后，页面会显示 `Confirmed locally`。

## 常见问题

- **缺少 Chromium**：运行 `.\.venv\Scripts\python.exe -m playwright install chromium`。
- **按钮没有被点击**：确认按钮文字与 `--button-text` 一致，且按钮确实可见。
- **可能点错按钮**：停止工具，换用更明确的按钮文字，并核对页面后再启动。
- **需要登录**：不要使用 `--headless`，在打开的浏览器中手动登录。
- **`poll_seconds must be at least 1 second`**：把 `--poll-seconds` 设为 `1` 或更大。

## 文件说明

```text
popup_clicker.py          # 主脚本
requirements.txt          # Python 依赖（playwright、pytest）
setup_windows.bat         # Windows 一键安装依赖、浏览器并运行测试
run_windows.bat           # Windows 一键启动（默认参数）
tests/                    # 单元测试
docs/assets/              # README 封面与本地合成测试页面
```
