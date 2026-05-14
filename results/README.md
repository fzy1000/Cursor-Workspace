# `results/` 分析结果目录

本目录用于存放**基于 `materials/` 等材料分析、制图、导出**而产生的交付物（表格、图表、报告、中间数据等）。

- **勿**将原始上传材料的大文件默认放在此目录；原件仍归 `materials/`。  
- 若某次任务需例外路径，以用户当次说明为准。  
- 分析结论须在正文内**标注数据出处**（文件路径、工作表、行列或字段）。

当前示例任务产出见 `analysis_report.md`、`ANALYSIS_RERUN.md`、`exploratory_stats.csv`、`compute_from_materials.py` 及同目录其他 CSV、SVG。  
使用 **pandas / seaborn** 的交互复现见仓库 `notebooks/materials_weekly_nav_analysis.ipynb`（需 `requirements-analysis.txt`）。
