#!/usr/bin/env python3
"""从 character.json + world-state.json + pregens.json 生成 STATUS.md。"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "state"
STATUS = ROOT / "STATUS.md"

SKILL_CN = {
    "acrobatics": "杂技（敏捷）",
    "animal_handling": "驯兽（感知）",
    "arcana": "奥秘（智力）",
    "athletics": "运动（力量）",
    "deception": "欺瞒（魅力）",
    "history": "历史（智力）",
    "insight": "洞悉（感知）",
    "intimidation": "威吓（魅力）",
    "investigation": "调查（智力）",
    "medicine": "医药（感知）",
    "nature": "自然（智力）",
    "perception": "察觉（感知）",
    "performance": "表演（魅力）",
    "persuasion": "说服（魅力）",
    "religion": "宗教（智力）",
    "sleight_of_hand": "巧手（敏捷）",
    "stealth": "隐匿（敏捷）",
    "survival": "求生（感知）",
}

ABI = [("str", "力量 STR"), ("dex", "敏捷 DEX"), ("con", "体质 CON"), ("int", "智力 INT"), ("wis", "感知 WIS"), ("cha", "魅力 CHA")]


def mod(score: int) -> int:
    return (score - 10) // 2


def fmt_mod(score: int) -> str:
    m = mod(score)
    return f"{score}（{'+' if m >= 0 else ''}{m}）"


def skill_bonus(ab_key: str, proficient, abilities: dict, pb: int) -> str:
    ab_for = {
        "acrobatics": "dex",
        "animal_handling": "wis",
        "arcana": "int",
        "athletics": "str",
        "deception": "cha",
        "history": "int",
        "insight": "wis",
        "intimidation": "cha",
        "investigation": "int",
        "medicine": "wis",
        "nature": "int",
        "perception": "wis",
        "performance": "cha",
        "persuasion": "cha",
        "religion": "int",
        "sleight_of_hand": "dex",
        "stealth": "dex",
        "survival": "wis",
    }[ab_key]
    m = mod(abilities[ab_for])
    if proficient == "expertise":
        m += pb * 2
        tag = "专精"
    elif proficient:
        m += pb
        tag = "熟练"
    else:
        tag = "未熟练"
    sign = "+" if m >= 0 else ""
    return f"{sign}{m}（{tag}）"


def load(name: str):
    return json.loads((STATE / name).read_text(encoding="utf-8"))


def render_unselected(world: dict) -> str:
    cal = world["calendar"]
    loc = world["location"]
    return f"""# 角色状态

[回到战役说明](README.md)

> 点开本文件即可查看当前属性、状态、装备、背包、技能、专长、战技与魔法。  
> **数据源**：`state/character.json` + `state/world-state.json`（由 `engine/update_status.py` 生成，请勿手改本文当作记忆）。

## 战役时钟

- **年份**：{cal['year_dr']} DR · {cal['year_name']}
- **日期**：{cal['month_cn']}（{cal['month']}）{cal['day']} 日 · {cal['time_of_day']}
- **地点**：{loc['place']}（{loc['region']}）
- **回合**：第 {world['turn']} 轮 · 场次 {world['session']}

## 身份

尚未选定角色。请在对话中回复 **A / B / C / D**（或提出自定义概念，DM 按《玩家手册》第 1 章步骤落地）。

| 代号 | 角色 | 种族 / 职业 / 背景 |
|------|------|-------------------|
| A | 卡伦·安卡瑟 | 人类（泰瑟尔）战士 · 民间英雄 |
| B | 伊拉恩·月溪 | 月精灵法师 · 学者 |
| C | 布琳达·石炉 | 丘陵矮人牧师（海姆·生命） · 侍僧 |
| D | 佩林·荆袋 | 轻足半身人游荡者 · 罪犯 |

## 属性 / 状态 / 装备 / 背包 / 技能 / 专长 / 战技 / 魔法

创角完成后自动填写。1 级时专长与战技多为空：专长常见于人类变体或第 4 级；战斗大师战技见于战士第 3 级（《玩家手册》第 3、6 章）。

## 派系声望

{faction_table(world)}

## 已知事态

{world.get("notes_public") or "无"}
"""


def faction_table(world: dict) -> str:
    lines = ["| 派系 | 声望 |", "|------|------|"]
    for k, v in world["factions"].items():
        lines.append(f"| {k} | {v} |")
    return "\n".join(lines)


def render_pc(pc: dict, world: dict, raw: dict) -> str:
    cal = world["calendar"]
    loc = world["location"]
    pb = 2
    ab = pc["abilities"]
    skills = pc.get("skills") or {}
    skill_lines = []
    for key, cn in SKILL_CN.items():
        skill_lines.append(f"| {cn} | {skill_bonus(key, skills.get(key, False), ab, pb)} |")
    feat_lines = "（无）" if not pc.get("feats") else "\n".join(f"- {x}" for x in pc["feats"])
    man = pc.get("maneuvers") or []
    man_txt = "（无）\n\n" + pc.get("maneuvers_note", "") if not man else "\n".join(f"- {x}" for x in man)
    feat_txt = feat_lines if isinstance(feat_lines, str) else feat_lines
    features = "\n".join(f"- **{f['name']}**：{f['text']}" for f in pc.get("features") or [])
    worn = "、".join(pc["equipment"]["worn"])
    inv = "、".join(pc.get("inventory") or [])
    money = pc["money"]
    weapons = "\n".join(
        f"| {w['name']} | {w['atk']} | {w['dmg']} | {w.get('notes','')} |"
        for w in pc["equipment"]["weapons"]
    )
    cond = "、".join(raw.get("conditions") or []) or "无"
    sc = pc.get("spellcasting")
    if not sc:
        magic = "非法术职业，或尚未获得法术。\n"
    else:
        slots = sc.get("slots") or {}
        slot_txt = "、".join(f"{k}环 {v['current']}/{v['max']}" for k, v in slots.items())
        cans = "、".join(sc.get("cantrips") or [])
        prep = "、".join(sc.get("prepared") or [])
        book = "、".join(sc.get("spellbook") or [])
        magic = f"""- **关键属性**：{sc['ability'].upper()}　**法术豁免 DC**：{sc['save_dc']}　**法术攻击**：+{sc['attack']}
- **法术位**：{slot_txt or '无'}
- **戏法**：{cans or '无'}
- **已准备**：{prep or '无'}
- **法术书/领域恒定**：{book or '、'.join(sc.get('domain_always_prepared') or []) or '无'}
"""
    save_line = "、".join(
        f"{label[-3:]} {'熟练 +' + str(mod(ab[k])+pb) if pc['saves'][k] else '+' + str(mod(ab[k])) if mod(ab[k])>=0 else str(mod(ab[k]))}"
        for k, label in ABI
    )
    # fix save formatting more cleanly
    save_bits = []
    for k, label in ABI:
        m = mod(ab[k]) + (pb if pc["saves"][k] else 0)
        flag = "熟练" if pc["saves"][k] else "未熟练"
        save_bits.append(f"{label.split()[0]} {'+' if m>=0 else ''}{m}（{flag}）")
    pers = pc.get("personality") or {}
    return f"""# 角色状态 · {pc['name']}

[回到战役说明](README.md)

> 点开本文件即可查看当前属性、状态、装备、背包、技能、专长、战技与魔法。  
> **数据源**：`state/character.json`（由 `engine/update_status.py` 生成）。规则口径见《玩家手册》第 1、7、8、9、10 章。

## 战役时钟

- **年份**：{cal['year_dr']} DR · {cal['year_name']}
- **日期**：{cal['month_cn']}（{cal['month']}）{cal['day']} 日 · {cal['time_of_day']}
- **地点**：{loc['place']}（{loc['region']}）
- **回合**：第 {world['turn']} 轮 · 场次 {world['session']}
- **经验**：{raw.get('xp', pc.get('xp', 0))} XP · **等级**：{raw.get('level', 1)} · **激励**：{'有' if world.get('inspiration') or raw.get('inspiration') else '无'}

## 身份

| 项 | 内容 |
|----|------|
| 姓名 | {pc['name']}（{pc.get('name_en','')}） |
| 种族 | {pc['race']} |
| 职业 | {pc['class']}{' · ' + pc['subclass'] if pc.get('subclass') else ''} |
| 背景 | {pc['background']} |
| 阵营 | {pc['alignment']} |
| 神祇 | {pc.get('deity') or '未指定'} |
| 体型 / 速度 | {pc.get('size')} / {pc.get('speed')} 尺 |

## 属性

| 力量 | 敏捷 | 体质 | 智力 | 感知 | 魅力 |
|------|------|------|------|------|------|
| {fmt_mod(ab['str'])} | {fmt_mod(ab['dex'])} | {fmt_mod(ab['con'])} | {fmt_mod(ab['int'])} | {fmt_mod(ab['wis'])} | {fmt_mod(ab['cha'])} |

**豁免**：{'；'.join(save_bits)}  
**熟练加值**：+{pb}

## 战斗与状态

- **AC**：{pc['ac']}（{pc.get('ac_note','')}）
- **HP**：{raw.get('hp_current', pc['hp_current'])} / {pc['hp_max']}　**生命骰**：{pc['hit_dice']}
- **状态**：{cond}　**力竭**：{raw.get('exhaustion', 0)} 级
- **死亡豁免**：成功 {raw.get('death_saves',{}).get('success',0)} / 失败 {raw.get('death_saves',{}).get('fail',0)}

### 武器与攻击

| 名称 | 攻击 | 伤害 | 备注 |
|------|------|------|------|
{weapons}

## 职业特性

{features}

## 装备（着装）

{worn}

## 背包

{inv}

**钱币**：{money.get('pp',0)} pp / {money.get('gp',0)} gp（深水城俗称龙币） / {money.get('ep',0)} ep / {money.get('sp',0)} sp / {money.get('cp',0)} cp

## 技能

| 技能 | 加值 |
|------|------|
{chr(10).join(skill_lines)}

**工具**：{ '、'.join(pc.get('tools') or []) or '无' }  
**语言**：{ '、'.join(pc.get('languages') or []) }  
**感官**：{ '、'.join(pc.get('senses') or []) or '常规视觉' }

## 专长

{feat_txt}

## 战技

{man_txt}

## 魔法

{magic}

## 理念与缺陷

- **特质**：{pers.get('trait','')}
- **理想**：{pers.get('ideal','')}
- **羁绊**：{pers.get('bond','')}
- **缺陷**：{pers.get('flaw','')}

## 派系声望

{faction_table(world)}

## 角色已知事态

{world.get('notes_public') or '无'}
"""


def main() -> None:
    world = load("world-state.json")
    raw = load("character.json")
    pre = load("pregens.json")
    if not raw.get("selected"):
        text = render_unselected(world)
    else:
        pc = raw.get("sheet")
        if not pc:
            pid = raw.get("id")
            pc = pre["pregens"][pid]
        text = render_pc(pc, world, raw)
    STATUS.write_text(text, encoding="utf-8")
    print(f"Wrote {STATUS}")


if __name__ == "__main__":
    main()
