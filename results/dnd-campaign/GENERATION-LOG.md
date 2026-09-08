# 冒险生成日志（三宝书程序）

随机种子：`20260908`。复现：`python3 results/dnd-campaign/engine/generate_adventure.py`。

本文件只记录**掷骰与命中条目**及出处。未掷出的派系、年份、城市、模块情节一律不写入剧情。

## 程序依据

- 地点型冒险六步：`materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf` 第3章，PDF约 p72–p74
- 构筑地下城：同书第5章，PDF约 p100–p102
- 随机地图（限制扩张为起始区+4房）：同书附录A，PDF约 p271–p276
- 村庄大本营：同书「聚居地·村庄」，PDF约 p17
- 1–4级当地英雄：同书「游戏阶段」，PDF约 p35
- 神名：`materials/dnd-5e-三宝书/DND_5E_玩家手册CN.pdf` 附录B，PDF约 p294

## 掷骰结果

| 表 | 骰 | 点数 | 结果 | 出处 |
|----|----|------|------|------|
| 地下城目标 | d20 | 8 | 拯救一名俘虏 | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 第3章「地下城目标」，PDF约p72 |
| 冒险反派 | d20 | 7 | 任何行为趋向的不死生物 | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 第3章「冒险反派」，PDF约p73 |
| 冒险盟友 | d12 | 6 | 智者 | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 第3章「冒险盟友」，PDF约p74 |
| 冒险主顾 | d20 | 5 | 军官 | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 第3章「冒险主顾」，PDF约p74 |
| 冒险开场 | d12 | 4 | 冒险者们在一副尸体上发现了一张地图。该地图既设定了冒险所在，同时还是该冒险中反派想要之物 | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 第3章「冒险开场」，PDF约p74 |
| 冒险高潮 | d12 | 11 | 须选择追捕逃亡反派或拯救关心的 NPC/无辜者 | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 第3章「冒险高潮」，PDF约p74 |
| 地下城所在地 | d100 | 60 | 某山隘口中 | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 第5章「地下城所在地」，PDF约p100 |
| 地下城建造者 | d20 | 12 | 人类 | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 第5章「地下城建造者」，PDF约p101 |
| 建造者阵营 | d20 | 9 | 守序中立 | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 「角色阵营」，PDF约p101 |
| 建造者职业 | d20 | 1 | 野蛮人 | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 「角色职业」，PDF约p101 |
| 地下城用途 | d20 | 6 | 迷宫 | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 第5章「地下城用途」，PDF约p102 |
| 地下城历史 | d20 | 16 | 所在地被众神诅咒并受众神离弃 | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 第5章「地下城历史」，PDF约p102 |
| 村庄神坛（DMG：村庄有一两座神庙或神坛） | d6 | 1 | 裳禔亚 Chauntea（NG，农业） | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 「聚居地·村庄」PDF约p17；神名 PHB 附录B p294 |
| 起始区域（附录A） | d10 | 9 | 通道10尺；T型路口 | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 附录A「起始区域」，PDF约p271 |
| 房间1尺寸 | d20 | 7 | 长方形20x30 | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 附录A「房间」，PDF约p272 |
| 房间1门型 | d20 | 14 | 石质，栓住或上锁 | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 附录A「门类型」，PDF约p272 |
| 房间1原用途 | 见该用途表 | 14 | 储物室 | 附录A 地下城：迷宫 d20，PDF约p273 |
| 房间1现状 | d20 | 20 | 维持原状且光洁如新 | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 附录A「房间现状」，PDF约p276 |
| 房间1内容 | d100 | 26 | 怪物（宠物或结盟生物） | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 附录A「地下城房间内容」，PDF约p276 |
| 房间1怪物动机 | d20 | 8 | 地下城中找一个物品 | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 附录A「怪物动机」，PDF约p276 |
| 房间2尺寸 | d20 | 14 | 长方形40x50 | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 附录A「房间」，PDF约p272 |
| 房间2门型 | d20 | 14 | 石质，栓住或上锁 | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 附录A「门类型」，PDF约p272 |
| 房间2原用途 | 见该用途表 | 9 | 巢穴 | 附录A 地下城：迷宫 d20，PDF约p273 |
| 房间2现状 | d20 | 13 | 家具受损但仍然存在 | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 附录A「房间现状」，PDF约p276 |
| 房间2内容 | d100 | 11 | 怪物（主要生物）与宝藏 | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 附录A「地下城房间内容」，PDF约p276 |
| 房间2怪物动机 | d20 | 2 | 寻找一个避难所 | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 附录A「怪物动机」，PDF约p276 |
| 房间3尺寸 | d20 | 14 | 长方形40x50 | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 附录A「房间」，PDF约p272 |
| 房间3门型 | d20 | 3 | 木质 | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 附录A「门类型」，PDF约p272 |
| 房间3原用途 | 见该用途表 | 9 | 巢穴 | 附录A 地下城：迷宫 d20，PDF约p273 |
| 房间3现状 | d20 | 16 | 家具受损但仍然存在 | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 附录A「房间现状」，PDF约p276 |
| 房间3内容 | d100 | 23 | 怪物（宠物或结盟生物） | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 附录A「地下城房间内容」，PDF约p276 |
| 房间3怪物动机 | d20 | 17 | 躲避危险 | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 附录A「怪物动机」，PDF约p276 |
| 房间4尺寸 | d20 | 9 | 长方形20x30 | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 附录A「房间」，PDF约p272 |
| 房间4门型 | d20 | 2 | 木质 | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 附录A「门类型」，PDF约p272 |
| 房间4原用途 | 见该用途表 | 3 | 警卫室 | 附录A 地下城：迷宫 d20，PDF约p273 |
| 房间4现状 | d20 | 4 | 坑洞，地面部分倒塌 | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 附录A「房间现状」，PDF约p276 |
| 房间4内容 | d100 | 25 | 怪物（宠物或结盟生物） | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 附录A「地下城房间内容」，PDF约p276 |
| 房间4怪物动机 | d20 | 12 | 躲避敌人 | materials/dnd-5e-三宝书/DND_5E_城主指南CN.pdf 附录A「怪物动机」，PDF约p276 |

## 遭遇预算（1名1级角色）

简单25 / 中等50 / 困难75 / 致命100 XP阈值；当日校正XP 300。少于三名角色时倍数上调。

## 下一步（手册，不是自拟故事）

1. 《玩家手册》第1章一步步创建角色。
2. 创角完成后，用「冒险开场」条目把角色带进已生成的地点。
3. 房间内的具体怪物从《怪物图鉴》选**与反派条目和当地英雄典型对手相符**的资料卡，并用上表 XP 预算结算。
