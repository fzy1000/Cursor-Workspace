# 《逸剑风云决》MOD 逐步实现教程（UnrealPakViewer 版）

> 本版 **不使用 FModel**，解包全程用 **UnrealPakViewer**。  
> 配套设计单：[yijian-mod-tianren-chuanwu-design.md](./yijian-mod-tianren-chuanwu-design.md)  
> 适用：Steam 版《逸剑风云决》· **Windows**

---

## 工具清单（无 FModel）

| 工具 | 用途 | 获取 |
|------|------|------|
| **UnrealPakViewer** | 打开 pak、浏览、**Extract 解包** | https://github.com/jashking/UnrealPakViewer/releases |
| **UAssetGUI** | 编辑 `.uasset` 数据表 | https://github.com/atenfyr/UAssetGUI/releases |
| **Mappings.usmap** | 多数情况 **可选**（UE4.26 解析失败时再导入） | 3DM / Nexus 搜逸剑 usmap |
| **UnrealPak / repak** | 重新打包 `.pak` | [UnrealPakTool](https://github.com/allcoolthingsatoneplace/UnrealPakTool) |
| **（可选）CT 表** | `addskill` 快速测技能 | 3DM 逸剑 CT 帖 |

### UnrealPakViewer 版本注意

逸剑社区经验（[Cing 教程](https://cingblog.top/archives/yi-jian-feng-yun-jue-wu-pin-id-ti-qu-jiao-cheng)）：**请用 1.3 版**；部分新版本对本游戏可能闪退。若闪退，换 1.3 或 Nightly 试。

工具路径建议：**纯英文路径、无空格**（如 `D:\Tools\UnrealPakViewer\`）。

---

## 总流程

```
UnrealPakViewer 解包 Tables
    → UAssetGUI 改 Skills / Items / Buffs / Inherit
    → UnrealPak 打 _P.pak
    → 进游戏新档测传承
```

**建议开发顺序**（每步打包测一次）：

1. 纵云梯 → 2. 风云太极经 → 3. 太极绵掌 → 4. 混元缠丝手 → 5. 真武太极坠 → 6. Inherit 50000 点

---

## 第 0 步：准备

### 0.1 游戏 pak 路径

Steam → 逸剑风云决 → 浏览本地文件：

```
...\Wandering Sword\Wandering_Sword\Content\Paks\Wandering_Sword-WindowsNoEditor.pak
```

### 0.2 备份

- 复制整个 `Paks` 文件夹  
- 备份 Steam 存档  
- **用新存档测试 MOD**

### 0.3 关掉冲突 MOD

其它改了 `Skills.uasset` / `Inherit.uasset` 的 pak 先移出 `Paks`，只留你的测试 pak。

---

## 第 1 步：用 UnrealPakViewer 打开 pak

1. 运行 **UnrealPakViewer.exe**  
2. 把 **`Wandering_Sword-WindowsNoEditor.pak`** 拖进窗口（或菜单 **File → Open**）  
3. 等待左侧 **树形视图（Tree View）** 加载完成  
4. 若提示 **AES 密钥**：逸剑 Steam 版通常 **不需要**；若强制要密钥，到 3DM / Nexus 搜「逸剑 AES」或换 1.3 版 Viewer  

### 1.1 切换到列表视图搜文件（推荐）

- 工具栏或视图切换 → **List View / 文件列表**  
- 顶部 **搜索框** 输入：`Skills.uasset`、`Items.uasset`、`Buffs.uasset`、`Inherit`  
- 记下完整路径，一般为：

```
Wandering_Sword/Content/JH/Tables/Skills.uasset
Wandering_Sword/Content/JH/Tables/Items.uasset
Wandering_Sword/Content/JH/Tables/Buffs.uasset
Wandering_Sword/Content/JH/Tables/Inherit.uasset   （名称可能是 Inherit / Legacy，以你列表为准）
```

### 1.2 树形视图手动展开（备选）

```
Wandering_Sword
  └── Content
        └── JH
              └── Tables
                    ├── Skills.uasset
                    ├── Skills.uexp
                    ├── Items.uasset
                    ├── Items.uexp
                    ├── Buffs.uasset
                    ├── Buffs.uexp
                    ├── Inherit.uasset
                    └── Inherit.uexp
```

---

## 第 2 步：Extract 解包（核心）

### 2.1 解包整个 Tables 文件夹（最省事）

1. 在 **树形视图** 中选中 **`Tables` 文件夹**  
2. **右键 → Extract**（解压）  
3. 选择输出目录，例如：`D:\TianRenMod_Work\extracted\`  
4. 解包后应得到带完整层级的目录，例如：

```
extracted\Wandering_Sword\Content\JH\Tables\
    Skills.uasset + Skills.uexp
    Items.uasset + Items.uexp
    Buffs.uasset + Buffs.uexp
    Inherit.uasset + Inherit.uexp
    …（其它表可不管）
```

### 2.2 或只解包需要的 4 个表

对每个文件 **分别** 右键 → **Extract**（不要只解 `.uasset`）：

| 必须成对提取 |
|--------------|
| `Skills.uasset` + **`Skills.uexp`** |
| `Items.uasset` + **`Items.uexp`** |
| `Buffs.uasset` + **`Buffs.uexp`** |
| `Inherit.uasset` + **`Inherit.uexp`** |

> **没有 `.uexp` 时 UAssetGUI 会报错**（ArgumentOutOfRangeException 等）。若 Extract 后只有 uasset，在 Viewer **列表里同时选中两个文件** 再 Extract，或解整个 Tables 文件夹。

### 2.3 建立编辑工作区

```
D:\TianRenMod_Work\
├── original\                    ← 从 extracted 整份复制，永不修改
│   └── Wandering_Sword\Content\JH\Tables\
└── edit\                          ← 再复制一份到这里改
    └── Wandering_Sword\Content\JH\Tables\
```

以后 **只在 `edit\...\Tables\` 里改**。

---

## 第 3 步：配置 UAssetGUI（与 FModel 无关）

1. 打开 **UAssetGUI**  
2. 右上角 **Engine Version → VER_UE4_26（4.26）**  
   - 逸剑是 **UE4**，不是 UE5；[3DM 立绘 MOD 教程](https://bbs.3dmgame.com/thread-6457097-1-1.html) 写明：**游戏引擎 4.26**，版本选错封包后可能 **游戏崩溃**（「低版本资源用高版本选项」尤其危险）  
   - **不要选 5.3**（那是别的 UE5 游戏教程）  
   - 4.26 打不开时，再试 **4.27**（部分旧帖写 4.27，仍以 4.26 为准）  
3. **Mappings.usmap（可选）**  
   - UE4.26 很多情况下 **不加载 usmap 也能打开 Tables**  
   - 若提示解析失败 / Failed to parse，再到 3DM / Nexus 搜 `Wandering Sword usmap` 导入，**引擎版本仍选 4.26**  
4. 把 **`edit\...\Tables\Items.uasset`** 拖进 UAssetGUI  
5. 能展开 **Exports → Table** 且能看到中文物品名 → 版本正确  

### 3.1 用 UnrealPakViewer 辅助查名字（可选）

在 Viewer 中 **选中某个 `.uasset` → 右键 → Export To Json**，用记事本搜「云相太极」「天魔手」。  
但最终 **改数据仍用 UAssetGUI**。

### 3.2 用 UAssetGUI 导出 JSON 建 ID 表（推荐）

对每个表：**File → Save As (JSON)**：

- `Items.json`  
- `Skills.json`  
- `Buffs.json`  
- `Inherit.json`  

在 JSON 里搜索并记录 **原版 ID**：

| 搜索关键字 | 用途 |
|------------|------|
| 云相太极 | 克隆心法 |
| 云涛晓雾凌波舞 | 克隆轻功 |
| 天魔手 | 克隆拳武器 |
| 绵掌、武当长拳 | 克隆三式拳 |
| 天山传承、玉龙 | 克隆 Inherit 行 |

MOD 新 ID 建议段：**990001～990099**（全局不要和原版重复）。

---

## 第 4 步：纵云梯（第一个可玩 MOD）

1. UAssetGUI 打开 `edit\...\Skills.uasset`  
2. 找到 **云涛晓雾凌波舞** 行 → 复制整行 → 新 ID **`990002`**，改名 **纵云梯**  
3. **第一版不要改** 动画 / Blueprint / Buff 引用（全部保持和原版一样）  
4. 打开 `Items.uasset`，复制一本轻功秘籍 → ID **`990012`**，学会技能指向 **`990002`**  
5. **File → Save** 保存两个 uasset（会同步改 uexp）  
6. 跳到 **第 9 步打包**，进游戏测  

可选：CT 表 `addskill 990002 10` 验证 Skills 行是否有效。

---

## 第 5 步：风云太极经

1. **Skills**：复制 **云相太极** → ID **`990001`**，改名称描述  
2. **v0.1**：等级效果先不改，能学能装即可  
3. **Items**：复制云相秘籍 → **`990011`**  
4. **v0.2**：从 **流云太极** 抄 L5～6 到本技能；L10 在 **Buffs** 加「每层太极 +15% 武当伤」（见设计单）  

---

## 第 6 步：太极绵掌三式

1. 复制 **绵掌** 三次 → **`990003 / 990004 / 990005`**  
2. 从 **武当长拳** 复制二式、三式的范围、距离、CD 到 004、005  
3. 「每层太极 5% 再击」：参照 **天魔手 / 绝弦无音** 的 Proc；不会做先 **固定 10%**  
4. **Items**：一本或三本秘籍 → **`990013`** 等  

---

## 第 7 步：混元缠丝手 + 真武太极坠

| 物品 | 操作 |
|------|------|
| **混元缠丝手** `990021` | Items 复制 **天魔手**，改随机 debuff 为「太极印」6 种 |
| **真武太极坠** `990022` | Items 复制高阶饰品，加开战 +1 太极等被动 |

---

## 第 8 步：Inherit 传承 50000 点

1. UAssetGUI 打开 `edit\...\Inherit.uasset`  
2. 复制 **天山传承（剑）** 或 **玉龙传承** 一整行  
3. 修改：  
   - 显示名 → **天人遗武·风云太极**  
   - **Cost → 50000**（测试时可改 **0**）  
   - 物品/秘籍列表 → `990011, 990012, 990013, 990021, 990022`  
4. Save  

---

## 第 9 步：打包 _P.pak（UnrealPak）

### 9.1 组装 MOD 目录

**只放你改过的 uasset + uexp**，路径必须和游戏一致：

```
D:\TianRenMod_P\
└── Wandering_Sword\
    └── Content\
        └── JH\
            └── Tables\
                ├── Skills.uasset
                ├── Skills.uexp
                ├── Items.uasset
                ├── Items.uexp
                ├── Buffs.uasset      （若改过 Buffs）
                ├── Buffs.uexp
                ├── Inherit.uasset    （最后再加）
                └── Inherit.uexp
```

可从 `edit\Wandering_Sword\Content\JH\Tables\` **只复制改过的文件** 到上面结构。

### 9.2 打包

1. 将 **`TianRenMod_P` 文件夹**（注意是外层文件夹名）拖到 **`UnrealPak-with-Compression.bat`**  
2. 生成 pak，**重命名**为例如 **`TianRenChuanWu_P.pak`**（**必须 `_P` 后缀**）  
3. 复制到：

```
...\Wandering Sword\Wandering_Sword\Content\Paks\TianRenChuanWu_P.pak
```

### 9.3 用 repak 的替代命令（若不用 bat）

```text
repak pack -v --compression Gzip D:\TianRenMod_P
```

输出文件同样需命名为 `xxx_P.pak`。

---

## 第 10 步：游戏内测试

| 步骤 | 操作 |
|------|------|
| 1 | 启动游戏，能进主菜单 |
| 2 | **新游戏** → 继承界面有 **天人遗武** |
| 3 | 选传承（50000 点或测试用 0 点） |
| 4 | 背包有秘籍、混元缠丝手、真武太极坠 |
| 5 | 学秘籍、装栏位、打一架 |

卸 MOD 前：卸下 MOD 装备并忘记 MOD 武功，避免坏档。

---

## UnrealPakViewer 常见问题

| 现象 | 处理 |
|------|------|
| 打开 pak 闪退 | 换 **1.3 版** Viewer；路径改英文无空格 |
| Extract 只有 uasset 没有 uexp | 解 **整个 Tables 文件夹**；或列表里 uasset/uexp 一起选 |
| 搜不到 Inherit | 搜 `inherit`、`Legacy`、`传承`；或在 List View 搜 `.uasset` 筛 Tables |
| 右键没有 Export To Json | 仅部分版本有；改用 UAssetGUI 导出 JSON |
| UAssetGUI 打不开表 | 引擎版本改 **4.26**；确认 uexp 同目录；仍失败再导入 usmap |
| 改完 pak 进游戏崩溃 | 多半是 UAssetGUI **版本选成 5.x** 或封包路径错，改回 **4.26** 重改 |
| 游戏更新后 MOD 失效 | 用 Viewer **重新 Extract**，对比表结构，重做 MOD |

---

## MOD ID 对照表（填解包后的原版 ID）

| MOD ID | 类型 | 名称 | 克隆自（在 JSON 里搜） |
|--------|------|------|------------------------|
| 990001 | Skill | 风云太极经 | 云相太极 |
| 990002 | Skill | 纵云梯 | 云涛晓雾凌波舞 |
| 990003～005 | Skill | 太极绵掌三式 | 绵掌 + 武当长拳 |
| 990011～013 | Item | 秘籍 | 对应原版秘籍 |
| 990021 | Item | 混元缠丝手 | 天魔手 |
| 990022 | Item | 真武太极坠 | 高阶饰品 |
| 990090 | Inherit | 天人遗武 | 天山/玉龙传承 |

---

## 参考链接

- [Cing：UnrealPakViewer + UAssetGUI 提取物品 ID](https://cingblog.top/archives/yi-jian-feng-yun-jue-wu-pin-id-ti-qu-jiao-cheng)  
- [UnrealPakViewer GitHub](https://github.com/jashking/UnrealPakViewer)  
- [3DM：传承 8 合一（Inherit 范例）](https://bbs.3dmgame.com/thread-6545626-1-1.html)  

---

*解包工具：UnrealPakViewer · 编辑：UAssetGUI · 无需 FModel*
