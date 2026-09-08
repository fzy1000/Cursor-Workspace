#!/usr/bin/env python3
"""掷骰。先定 DC，再调用本模块。结果写入编年用的结构化记录。"""
from __future__ import annotations

import random
from dataclasses import dataclass, asdict


@dataclass
class DiceResult:
    notation: str
    rolls: list[int]
    modifier: int
    total: int
    dc: int | None
    success: bool | None
    note: str


def roll(notation: str, modifier: int = 0, dc: int | None = None, advantage: str | None = None, note: str = "") -> DiceResult:
    """notation 如 d20、2d6、1d10。advantage: None | 'adv' | 'dis'（仅对单颗 d20）。"""
    n, _, rest = notation.lower().partition("d")
    count = int(n) if n else 1
    sides = int(rest)
    if advantage in ("adv", "dis") and count == 1 and sides == 20:
        a, b = random.randint(1, 20), random.randint(1, 20)
        chosen = max(a, b) if advantage == "adv" else min(a, b)
        rolls = [a, b, chosen]
        total = chosen + modifier
    else:
        rolls = [random.randint(1, sides) for _ in range(count)]
        total = sum(rolls) + modifier
    success = None if dc is None else total >= dc
    return DiceResult(notation=notation, rolls=rolls, modifier=modifier, total=total, dc=dc, success=success, note=note)


def as_record(result: DiceResult) -> dict:
    return asdict(result)


if __name__ == "__main__":
    r = roll("d20", modifier=0, note="smoke test")
    print(r)
