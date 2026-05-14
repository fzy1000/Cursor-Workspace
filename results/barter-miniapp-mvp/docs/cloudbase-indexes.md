# 云数据库索引创建清单

在微信云开发控制台按以下顺序创建：

## `users`
1. `creditScore`（普通索引）

## `items`
1. `ownerOpenId` + `status` + `createdAt`（复合索引，`createdAt` 降序）
2. `price`（普通索引）

## `swipes`
1. `fromItemId` + `toItemId`（唯一索引）
2. `fromOpenId`（普通索引）

## `matches`
1. `pairKey`（唯一索引）
2. `userAOpenId` + `status`（复合索引）
3. `userBOpenId` + `status`（复合索引）

## 说明
- `pairKey` 由云函数按字典序拼接：`[itemId1, itemId2].sort().join('#')`。
- 首版建议把所有写权限都收敛到云函数，避免前端直接写库。
