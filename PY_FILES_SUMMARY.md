# 项目说明与 Python 脚本说明

## 项目功能
`openclaw_docs` 用于同步并维护 `https://docs.openclaw.ai/` 在线文档。
仓库中的 `docs/` 目录用于保存官网页面的本地镜像，目标是：
- 尽量保持最新；
- 可检查、可修复、可复跑；
- 为后续阅读、核对和分析提供稳定文档基础。

## Python 脚本说明

### `docs_scan.py`
**作用**
- 扫描 Markdown 文件或目录。
- 提取标题层级与 Markdown 超链接。
- 标记疑似空文档或疑似截断文档。

**用法**
- `python3 docs_scan.py <文件或目录>`
- `python3 docs_scan.py <文件或目录> --show-links`

---

### `sync_section.py`
**作用**
- 按单个 section 从 `llms.txt` 同步文档。
- 将抓取链接写入 `urls/<section>.txt`。
- 下载对应 `.md` 到 `docs/` 目录。
- 对疑似空/截断文档自动重试下载。

**用法**
- `python3 sync_section.py <section>`
- 示例：`python3 sync_section.py tools`

---

### `sync_selected_sections.py`
**作用**
- 按预设 sections 批量同步文档。
- 当前预设 sections：
  - `install`
  - `channels`
  - `tools`
  - `plugins`
  - `platforms`
  - `gateway`
  - `reference`
  - `help`
- 将链接写入 `urls/selected_sections.txt`。
- 下载并对疑似异常文档执行重试。

**用法**
- `python3 sync_selected_sections.py`

---

### `sync_all_docs.py`
**作用**
- 基于 `llms.txt` 的全站列表做完整性检查与修复。
- 检查缺失文档。
- 检查空文档或疑似截断文档。
- 自动下载或重下修复。
- 生成 `urls/all.txt`。

**用法**
- `python3 sync_all_docs.py --check-only`：仅检查
- `python3 sync_all_docs.py`：修复缺失或异常文档
- `python3 sync_all_docs.py --update-all`：强制重下全站文档

---

### `sync_common.py`
**作用**
- 作为同步脚本的共享模块。
- 统一处理：
  - 读取 `llms.txt`
  - URL 提取
  - 文档下载
  - 空文档/疑似截断检测
  - URL 列表写入
- 用于减少 `sync_all_docs.py`、`sync_section.py`、`sync_selected_sections.py` 的重复代码。

**用法**
- 不直接单独运行。
- 由其他同步脚本导入使用。

---

### `patch_openclaw_config.py`
**作用**
- 一次性修改本机 `~/.openclaw/openclaw.json` 的辅助脚本。
- 用于本机配置修补，不属于通用文档同步流程。

**用法**
- `python3 patch_openclaw_config.py`
- 运行前应先确认修改目标与影响范围。
