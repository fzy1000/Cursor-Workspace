---
name: materials-analysis-outputs
description: Runs quantitative or documentary analysis strictly from materials in materials/, applies formulas in docs/consensus.md, and writes deliverables to results/ with full source citations. Use when the user asks for statistics, correlation, performance tables, charts, exported CSV, or analysis reports derived from uploaded project files.
---

# 材料分析与结果产出

## 何时使用

用户基于 **`materials/`** 中的表格或文档要求：统计、相关性、收益/回撤类计算、导出数据表、图表说明或 **`results/`** 中的分析报告时启用本技能。

## 执行顺序

1. **锁定输入**：确认使用的文件路径（默认 `materials/`）、工作表名、列名或段落位置；不得用未在仓库内的文件充当来源。  
2. **对齐口径**：打开 **`docs/consensus.md`**（或任务指定的共识文件）；公式、指标定义、阈值表述**仅使用其中已写明的条款**。若共识缺项且任务依赖计算，先说明缺口并请用户补充，**不自拟项目共识**。  
3. **计算与校验**：逐步可还原到原始单元格或字段；中间表可写入 **`results/`** 便于复核。  
4. **产出位置**：报告、图表（SVG/PNG 等）、导出 CSV/Excel、复现用中间表 — **默认写入 `results/`**；勿覆盖 `materials/` 原件除非用户明确要求。  
5. **交付物内容**：正文须含**数据溯源**（路径 + 表/字段/日期范围）；结论区分「材料内可证」与「方法局限/未检验项」。  
6. **风格**（若用户要插入 PPT/配图）：版式与配色参见 **`style/INSTRUCTION.md`**，**数字仍只来自材料与共识**。

## 禁止

- 编造或推断未出现在材料中的数值、样本区间或产品属性。  
- 在未经用户当次允许时引入网络数据补全材料。  
- 把 `results/` 里旧文件当作原始事实来源替代 `materials/`。

## 交叉引用

- 证据与免责总规程：[instruments/work-materials-instrument.md](../../../instruments/work-materials-instrument.md)  
- 结果目录说明：[results/README.md](../../../results/README.md)
