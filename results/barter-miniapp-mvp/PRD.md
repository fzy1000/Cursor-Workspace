# 以物换物小程序 MVP 产品规格

## 1. 产品目标
- 在微信生态内跑通 `发布物品 -> 价格范围匹配 -> 双向喜欢 -> 匹配成功` 主链路。
- 以 `openid` 作为用户主身份，不引入手机号注册。

## 2. 页面结构
- `登录页`：获取微信身份并初始化用户档案。
- `我的物品页`：展示我发布的物品，支持进入发布页和详情页。
- `发布物品页`：上传多图、填写描述/标签/价格并创建物品。
- `物品详情页`：查看物品详情，进入匹配页和“喜欢我的”页。
- `匹配页`：基于目标物品展示候选卡片，左滑不喜欢、右滑喜欢。
- `喜欢我的页`：查看谁想和我的哪个物品交换，并做回赞。
- `我的页面`：展示头像昵称、简介、信用等级与最近发布物品。

## 3. 业务规则

### 3.1 发布规则
- 图片至少 1 张，最多 9 张。
- 描述必填，长度 `1-200`。
- 标签可选，最多 10 个，单个标签最多 12 字。
- 价格必填，且 `price > 0`。

### 3.2 匹配规则
- 候选过滤公式：`abs(candidatePrice - basePrice) / basePrice <= 0.1`。
- 候选必须满足：
  - 物品状态为 `active`；
  - 不是当前用户的物品；
  - 未被当前用户针对该 baseItem 滑过（like/dislike）。
- 左滑：记录 `dislike`。
- 右滑：记录 `like`，并检查是否形成双向 like。

### 3.3 双向喜欢与成交
- A 物品对 B 物品右滑，写入单向 `like` 记录。
- 若 B 物品已对 A 物品存在 `like` 记录，则写入或更新 `matches.status = matched`。
- 同一对物品只允许一条有效匹配记录（使用标准化键去重）。

### 3.4 我的页面规则
- 简介 `bio` 可编辑，最长 150 字。
- 信用分 `creditScore` 初始 100，取值范围 `0-100`。
- 信用等级映射：
  - `A`: 90-100
  - `B`: 75-89
  - `C`: 60-74
  - `D`: 0-59
- 最近发布物品按 `createdAt desc` 返回，默认 5 条，可扩展为 10 条。

## 4. 数据模型

### 4.1 users
- `_id`: string(openid)
- `nickName`: string
- `avatarUrl`: string
- `bio`: string
- `creditScore`: number
- `creditLevel`: string(A/B/C/D)
- `matchedCount`: number
- `complaintCount`: number
- `createdAt`: number(timestamp)
- `updatedAt`: number(timestamp)

### 4.2 items
- `_id`: string
- `ownerOpenId`: string
- `images`: string[]
- `description`: string
- `tags`: string[]
- `price`: number
- `status`: string(active/matched/offline/deleted)
- `createdAt`: number
- `updatedAt`: number

### 4.3 swipes
- `_id`: string
- `fromOpenId`: string
- `fromItemId`: string
- `toItemId`: string
- `action`: string(like/dislike)
- `createdAt`: number

### 4.4 matches
- `_id`: string
- `pairKey`: string(排序后的 itemAId#itemBId)
- `itemAId`: string
- `itemBId`: string
- `userAOpenId`: string
- `userBOpenId`: string
- `status`: string(pending/matched/closed)
- `createdAt`: number
- `matchedAt`: number

## 5. 云函数接口
- `login`：获取 `openid` 并初始化用户。
- `createItem`：创建物品。
- `listMyItems`：查询我的物品。
- `getItemDetail`：获取单个物品详情。
- `getMatchCandidates`：按 10% 规则返回候选。
- `recordSwipe`：记录左/右滑；右滑时检查并更新匹配状态。
- `listIncomingLikes`：查询“谁想和我换”。
- `respondIncomingLike`：在“喜欢我的”中回赞并促成匹配。
- `getProfile`：读取我的资料和最近发布。
- `updateProfile`：更新简介等档案字段。

## 6. 状态流转
- `items.status`：
  - `active` -> `matched`（发生成功匹配，后续可配置自动下架）
  - `active` -> `offline`（手动下架）
  - `active/offline` -> `deleted`（软删除）
- `matches.status`：
  - `pending` -> `matched`（双向 like 达成）
  - `matched` -> `closed`（后续交易取消/结束）

## 7. MVP 验收用例
- 用户可完成微信登录并看到自己的用户信息。
- 用户可发布带图片、描述、标签、价格的物品。
- 匹配页只出现价格差异不超过 10% 的候选。
- 左滑不会进入“喜欢我的”，右滑会进入对方“喜欢我的”列表。
- 对方在“喜欢我的”中点击喜欢后，双方形成 `matched` 状态。
- 用户在“我的”页面可见简介、信用分/等级、最近发布物品。
