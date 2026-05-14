---
name: python-data-notebooks
description: Guides pandas, numpy, matplotlib, seaborn, and Jupyter workflows with emphasis on reproducibility, vectorization, and PEP 8. Use when analyzing or visualizing data in Python scripts or .ipynb, building notebooks, or refactoring analysis code in this workspace.
---

# Python Data Analysis & Jupyter

## Principles

- Concise, technical answers; accurate, runnable Python.
- Prefer **vectorized** pandas/numpy operations over Python loops on whole columns.
- Prefer **functions** over classes unless modeling stateful pipelines.
- **PEP 8**; names reflect meaning (`weekly_returns`, not `df2`).
- Document **data sources**, assumptions, and methodology (markdown cells or module docstring).

## pandas

- Use **pandas** for manipulation; prefer **method chaining** where readable.
- Use **`loc` / `iloc`** for explicit selection; avoid chained indexing for assignment.
- Use **`groupby`** for aggregation; consider **`Categorical`** for low-cardinality strings.

## Visualization

- **matplotlib** for fine control; **seaborn** for statistical plots and sensible defaults.
- Every plot: **title, axis labels, legend** when multiple series; consider **color-blind-safe** palettes (e.g. seaborn `colorblind`).

## Jupyter

- Structure with **markdown section headers**; one logical step per code cell where practical.
- Execution order must **reproduce** from top to bottom; avoid hidden global state.
- Use **`%matplotlib inline`** (or IPython’s matplotlib integration) for inline figures in classic notebooks.

## Quality & errors

- Start with **exploration**: `info`, `describe`, missing counts, dtypes.
- Treat **missing data** explicitly (drop, impute, or flag—justify choice).
- **`try`/`except`** around I/O and brittle parsing; validate **ranges and dtypes** after load.

## Performance

- Vectorize; use appropriate dtypes; for **larger-than-memory** data consider **dask** (optional).
- Profile before micro-optimizing.

## Dependencies (typical stack)

`pandas`, `numpy`, `matplotlib`, `seaborn`, `jupyter`; add **`scikit-learn`** when doing ML.

## Conventions

1. Begin with exploration and summary statistics.  
2. Factor repeated plots into **small reusable functions**.  
3. Track notebooks and scripts with **git**; avoid committing huge raw data when possible.

## Workspace overlap

If analysis uses **`materials/`**, facts and figures must remain **traceable** to those files; write exports and reports to **`results/`** per project rules. See `materials-analysis-outputs` skill and `instruments/work-materials-instrument.md`.

## References

Official docs: [pandas](https://pandas.pydata.org/docs/), [matplotlib](https://matplotlib.org/stable/contents.html), [Jupyter](https://docs.jupyter.org/).
