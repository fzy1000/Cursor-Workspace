# 数据库与安全设计（微信云开发）

## 1. 集合定义

### 1.1 `users`
```json
{
  "_id": "openid",
  "nickName": "微信昵称",
  "avatarUrl": "头像 URL",
  "bio": "个人简介",
  "creditScore": 100,
  "creditLevel": "A",
  "matchedCount": 0,
  "complaintCount": 0,
  "createdAt": 1715600000000,
  "updatedAt": 1715600000000
}
```

### 1.2 `items`
```json
{
  "_id": "自动生成",
  "ownerOpenId": "openid",
  "images": ["cloud://.../a.jpg"],
  "description": "九成新耳机",
  "tags": ["耳机", "数码"],
  "price": 299,
  "status": "active",
  "createdAt": 1715600000000,
  "updatedAt": 1715600000000
}
```

### 1.3 `swipes`
```json
{
  "_id": "自动生成",
  "fromOpenId": "openidA",
  "fromItemId": "itemA",
  "toItemId": "itemB",
  "action": "like",
  "createdAt": 1715600000000
}
```

### 1.4 `matches`
```json
{
  "_id": "自动生成",
  "pairKey": "itemA#itemB",
  "itemAId": "itemA",
  "itemBId": "itemB",
  "userAOpenId": "openidA",
  "userBOpenId": "openidB",
  "status": "matched",
  "createdAt": 1715600000000,
  "matchedAt": 1715600001234
}
```

## 2. 索引建议
- `users`
  - 单字段：`creditScore`
- `items`
  - 复合：`ownerOpenId + status + createdAt(desc)`
  - 单字段：`price`
- `swipes`
  - 复合唯一：`fromItemId + toItemId`
  - 单字段：`fromOpenId`
- `matches`
  - 复合唯一：`pairKey`
  - 复合：`userAOpenId + status`、`userBOpenId + status`

## 3. 权限原则
- 客户端仅做读操作，且避免直接读写敏感字段。
- 所有写操作经云函数完成，使用 `OPENID` 作为最终身份依据。
- 云函数内再次校验：
  - 物品拥有者校验；
  - 参数合法性校验；
  - 去重校验（swipe/match）。
- 可直接参考 `docs/cloudbase-security-rules.jsonc` 在云开发控制台配置数据库权限模板（再按实际环境微调）。

## 4. 字段校验
- `items.images.length` 范围：`1-9`
- `items.description` 长度：`1-200`
- `items.tags.length` 范围：`0-10`
- `items.price > 0`
- `users.bio` 长度：`0-150`
- `users.creditScore` 范围：`0-100`

## 5. 信用等级计算
- `90-100` => `A`
- `75-89` => `B`
- `60-74` => `C`
- `0-59` => `D`

由云函数统一计算并写回，客户端不直接提交 `creditLevel`。
