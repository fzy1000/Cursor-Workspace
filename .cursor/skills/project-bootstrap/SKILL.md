---
name: project-bootstrap
description: Bootstrap and maintain a Cursor workspace with rules, MCP config, and practical defaults. Use when the user asks to initialize workspace standards, configure MCP, or set up project-level agent conventions.
---

# Project Bootstrap

## 目标

在项目内维护一套稳定的 Cursor 工作区基础设施，包括 rules、skills 和 MCP 配置。

## 执行步骤

1. 确认 `.cursor/rules/` 中存在至少一个 `alwaysApply: true` 的规则。
2. 确认 `.cursor/skills/` 中存在至少一个项目技能，并使用清晰的触发描述。
3. 检查 `.cursor/mcp.json` 配置是否可运行（命令、参数、环境变量齐全）。
4. 若用户要求“设为工作区”，优先提供 `.code-workspace` 文件并指导直接打开。

## MCP 配置建议

- 优先使用本地可执行命令，避免依赖不明确的全局路径。
- 敏感值放入环境变量，例如 `API_KEY`，不要硬编码。
- 对外部服务标注用途，便于后续维护。

## 验收清单

- [ ] `.cursor/rules/*.mdc` 存在且可读
- [ ] `.cursor/skills/*/SKILL.md` 存在且描述清晰
- [ ] `.cursor/mcp.json` JSON 格式正确
- [ ] `.code-workspace` 可在 Cursor 中直接打开
