# 项目说明与 Python 脚本说明

## 项目功能（简要）
`openclaw_docs` 用于同步并维护 `https://docs.openclaw.ai/` 在线文档。
仓库中的 `.md` 文件可视为官网页面的本地镜像，目标是：
- 尽量保持最新；
- 可检查、可修复、可复跑；
- 为后续配置审查提供可靠文档基础。

## Python 脚本作用

### `docs_scan.py`
- 扫描 Markdown 文件/目录。
- 输出标题层级与超链接。
- 标记疑似空文档或疑似截断文档（`empty_or_truncated`）。
- 适合在精读前做快速结构体检。

### `sync_section.py`
- 按单个 section 同步文档（来源：`llms.txt`）。
- 将抓取链接写入 `urls/<section>.txt`。
- 下载对应 `.md` 到仓库目录。
- 对疑似空/截断文档自动重试下载。

### `sync_selected_sections.py`
- 按预设 sections 批量同步（install/channels/tools/plugins/platforms/gateway/reference/help）。
- 将链接写入 `urls/selected_sections.txt`。
- 下载并对疑似异常文档执行重试。

### `sync_all_docs.py`
- 全站级校验与修复脚本（基于 `llms.txt` 全量列表）。
- 功能：
  - 检查缺失文档；
  - 检查空文档/疑似截断文档；
  - 自动下载或重下修复；
  - 生成 `urls/all.txt`。
- 常用：
  - `python3 sync_all_docs.py --check-only`（仅检查）
  - `python3 sync_all_docs.py`（修复缺失/异常）

### `patch_openclaw_config.py`
- 一次性修改本机 `~/.openclaw/openclaw.json` 的辅助脚本。
- 用于本机配置修补，不属于通用文档同步流程。
