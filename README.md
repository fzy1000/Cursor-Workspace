# Cursor-Workspace

这是一个可直接用于 Cursor 的项目工作区模板，已包含：

- `.cursor/rules/`：项目级 instruction（规则）
- `.cursor/skills/`：项目级 skill（技能），含 `materials-analysis-outputs`（材料分析 → `results/` 产出）、`python-data-notebooks`（pandas / 可视化 / Jupyter 规范）
- `.cursor/mcp.json`：MCP 服务配置模板
- `Cursor-Workspace.code-workspace`：可直接打开的 Cursor 工作区文件
- `instruments/work-materials-instrument.md`：工作材料数据与引用规程（强制依据上传材料）
- `materials/`：上传的工作材料存放目录
- `results/`：分析、图表、导出报表等**产出物**默认存放目录
- `style/`：风格与版式参照；其中 [`style/INSTRUCTION.md`](style/INSTRUCTION.md) 为配图与 PPT 的汇总可执行指令
- `docs/consensus.md`：计算口径与公式共识（模板，需按项目填写）

## 快速开始

1. 在 Cursor 中打开该目录或 `.code-workspace` 文件。
2. 按需编辑 `.cursor/mcp.json` 的命令与环境变量。
3. 在聊天里直接让 Agent 使用本项目规则与技能执行任务。

数据分析（可选）：`pip install -r requirements-analysis.txt` 后打开 `notebooks/materials_weekly_nav_analysis.ipynb`；无依赖时用 `python3 results/compute_from_materials.py` 复现核心指标。

## Office 相关 MCP（Excel / PPTX）

已在 `.cursor/mcp.json` 中增加：

| 名称 | 作用 | 本机依赖 |
|------|------|----------|
| `excel` | 读写与编辑 `.xlsx`（无需安装 Microsoft Excel） | Node.js + `npx`，包名 `@negokaz/excel-mcp-server`；环境变量 `EXCEL_MCP_PAGING_CELLS_LIMIT=4000`（与 `.cursor/mcp.json` 一致） |
| `pptx` | 创建与编辑 `.pptx`（标准 MCP，基于 [shjanjua/pptx-mcp-server](https://github.com/shjanjua/pptx-mcp-server)） | Python 3.10+，并安装该包（PyPI 若不可用则从源码安装） |

**PPTX 安装示例**（建议在项目目录下使用虚拟环境，并把 `pptx` 的 `command` 改成该环境的 `python` 绝对路径）：

```bash
cd /Users/allen/Documents/Project/Cursor-Workspace
python3 -m venv .venv
.venv/bin/python -m pip install -U pip
.venv/bin/pip install git+https://github.com/shjanjua/pptx-mcp-server.git
```

然后将 `.cursor/mcp.json` 里 `pptx.command` 设为 `/Users/allen/Documents/Project/Cursor-Workspace/.venv/bin/python`（或你机器上对应路径）。

修改 MCP 配置后请**完全重启 Cursor** 再试。
