# PY_FILES_SUMMARY.md

本文件只记录仓库内 Python 脚本的用途与用法。
项目规则见 `skills.txt`，项目状态与交接信息见 `HANDOFF.md`。

## `project_env.py`
**作用**
- 统一补充 sibling `../myutils` 到导入路径。
- 让本项目脚本可以直接复用 `myutils` 的通用函数。

**用法**
- 不直接单独运行。
- 由 `docs_scan.py`、`sync_common.py` 等脚本导入使用。

---

## `docs_scan.py`
**作用**
- 扫描一个或多个 Markdown 文件/目录。
- 提取标题层级与 Markdown 链接。
- 标记疑似空文档或疑似截断文档。
- 内部复用 `myutils/markdown_utils.py`。

**用法**
- `python3 docs_scan.py <文件或目录>`
- `python3 docs_scan.py <文件或目录> --show-links`

---

## `sync_section.py`
**作用**
- 按单个 section 同步文档。
- 将对应链接写入 `urls/<section>.txt`。
- 下载到 `docs/`，并对疑似空/截断文档自动重试。

**用法**
- `python3 sync_section.py <section>`
- `python3 sync_section.py <section> --timeout 45`
- 示例：`python3 sync_section.py tools`

---

## `sync_selected_sections.py`
**作用**
- 按预设 sections 批量同步文档。
- 将链接写入 `urls/selected_sections.txt`。
- 下载到 `docs/`，并对疑似异常文档自动重试。

**当前预设 sections**
- `install`
- `channels`
- `tools`
- `plugins`
- `platforms`
- `gateway`
- `reference`
- `help`

**用法**
- `python3 sync_selected_sections.py`
- `python3 sync_selected_sections.py --timeout 45`

---

## `sync_all_docs.py`
**作用**
- 基于 `llms.txt` 做全站完整性检查与修复。
- 检查缺失文档。
- 检查空文档或疑似截断文档。
- 生成 `urls/all.txt`。
- 按本地镜像规则写入文档：官网根级 Markdown 归档到 `docs/others/`，其余文档保持原 section 路径。

**用法**
- `python3 sync_all_docs.py --check-only`：仅检查
- `python3 sync_all_docs.py`：修复缺失或异常文档
- `python3 sync_all_docs.py --update-all`：强制重下全站文档
- `python3 sync_all_docs.py --timeout 45`

---

## `sync_common.py`
**作用**
- 同步脚本的共享模块。
- 统一处理 `llms.txt` 读取、URL 提取、文档下载、空文档/截断检测、URL 列表写入等公共逻辑。
- 统一处理官网相对路径到本地镜像路径的映射规则：官网根级 Markdown 映射到 `docs/others/`，其余路径仍落在 `docs/` 原 section 下。
- 内部复用 `myutils/http_utils.py` 与 `myutils/markdown_utils.py`。

**用法**
- 不直接单独运行。
- 由 `sync_all_docs.py`、`sync_section.py`、`sync_selected_sections.py` 导入使用。
