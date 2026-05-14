# 材料再分析摘要（技能对齐说明）

**执行时间**：2026-04-09  
**遵循技能**：`materials-analysis-outputs`（材料溯源 + `results/` 产出）、`python-data-notebooks`（pandas/向量化/seaborn 规范体现在 `notebooks/materials_weekly_nav_analysis.ipynb`）。  
**共识口径**：`docs/consensus.md` §2.1–2.3（周收益率、Pearson、弱相关阈值 \(|r|<0.30\)）。

---

## 1. 数据源

| 项 | 内容 |
|----|------|
| 文件 | `materials/CTA&混合中性_周度净值序列.xlsx` |
| 工作表 | `Sheet` |
| 列 | `净值日期`、`对冲9号累计净值`、`CTA实盘净值` |

---

## 2. 数据质量（基于本次加载）

| 指标 | 值 |
|------|-----|
| 含日期与 B 列净值的行数 | 200 |
| B、C **同时非空**的周度行数 | 154 |
| 可计算的周收益率对数 \(n\) | 153 |
| 重叠区间（期末日） | 2023-03-24 — 2026-03-20 |

> 明细见 `results/exploratory_stats.csv`（由 `results/compute_from_materials.py` 生成，**仅标准库**，不依赖 pandas）。

---

## 3. 核心结论（与共识一致）

| 指标 | 值 |
|------|-----|
| Pearson \(r\)（对冲9号周收益 vs CTA 周收益） | **0.079718** |
| \(|r| < 0.30\) | **是** → **弱线性相关** |
| 对冲9号周收益均值 / 标准差 | 见 `exploratory_stats.csv` |
| CTA 周收益均值 / 标准差 | 见 `exploratory_stats.csv` |
| 同向周（两周收益均>0）次数 | 见 `exploratory_stats.csv` `weeks_both_positive` |
| 同向周（两周收益均<0）次数 | 见 `exploratory_stats.csv` `weeks_both_negative` |
| 异号周次数 | `weeks_mixed_sign` |

**解读**：在重叠样本内，两产品**周度收益线性相关性很弱**，与此前分析一致；分散化角度上，二者周收益缺乏稳定线性同涨同跌关系（仅限本频率与本算法）。

---

## 4. 复现方式

1. **当前环境（无 pandas）**  
   ```bash
   python3 results/compute_from_materials.py
   ```

2. **推荐环境（符合 `python-data-notebooks`）**  
   ```bash
   pip install -r requirements-analysis.txt
   jupyter notebook notebooks/materials_weekly_nav_analysis.ipynb
   ```  
   笔记本内使用 **pandas 向量化** `pct_change()`、**seaborn** 散点与 **matplotlib** 标签，结果应与本摘要数值一致。

---

## 5. 局限

- 结论仅适用于**表内周度净值**与相邻周收益；未做显著性检验。  
- 不构成投资建议。
