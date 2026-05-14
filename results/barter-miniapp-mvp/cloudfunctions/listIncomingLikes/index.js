const cloud = require("wx-server-sdk");

cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV });

function getPairKey(a, b) {
  return [String(a), String(b)].sort().join("#");
}

exports.main = async (event) => {
  const wxContext = cloud.getWXContext();
  const openid = wxContext.OPENID;
  if (!openid) {
    return { success: false, message: "未登录" };
  }

  const targetItemId = String(event.targetItemId || "").trim();
  if (!targetItemId) {
    return { success: false, message: "缺少 targetItemId" };
  }

  const db = cloud.database();
  const _ = db.command;
  const items = db.collection("items");
  const swipes = db.collection("swipes");
  const users = db.collection("users");
  const matches = db.collection("matches");

  const targetRes = await items.doc(targetItemId).get().catch(() => null);
  if (!targetRes || !targetRes.data) {
    return { success: false, message: "目标物品不存在" };
  }
  if (targetRes.data.ownerOpenId !== openid) {
    return { success: false, message: "无权限查看该物品喜欢记录" };
  }

  const swipeRes = await swipes
    .where({
      toItemId: targetItemId,
      action: "like"
    })
    .orderBy("createdAt", "desc")
    .limit(100)
    .get();
  const rawList = swipeRes.data || [];
  if (rawList.length === 0) {
    return { success: true, list: [] };
  }

  const fromItemIds = [...new Set(rawList.map((it) => it.fromItemId))];
  const fromItemsRes = await items
    .where({
      _id: _.in(fromItemIds),
      status: _.neq("deleted")
    })
    .get();
  const fromItems = fromItemsRes.data || [];
  const itemMap = {};
  fromItems.forEach((item) => {
    itemMap[item._id] = item;
  });

  const ownerIds = [...new Set(fromItems.map((it) => it.ownerOpenId))];
  let userMap = {};
  if (ownerIds.length > 0) {
    const userRes = await users.where({ _id: _.in(ownerIds) }).get();
    userMap = (userRes.data || []).reduce((acc, user) => {
      acc[user._id] = user;
      return acc;
    }, {});
  }

  const pairKeys = [...new Set(rawList.map((it) => getPairKey(it.fromItemId, targetItemId)))];
  let matchMap = {};
  if (pairKeys.length > 0) {
    const matchRes = await matches.where({ pairKey: _.in(pairKeys) }).get();
    matchMap = (matchRes.data || []).reduce((acc, match) => {
      acc[match.pairKey] = match;
      return acc;
    }, {});
  }

  const list = rawList
    .map((record) => {
      const fromItem = itemMap[record.fromItemId];
      if (!fromItem || fromItem.ownerOpenId === openid) {
        return null;
      }
      const pairKey = getPairKey(record.fromItemId, targetItemId);
      const fromUser = userMap[fromItem.ownerOpenId] || {
        nickName: "微信用户",
        avatarUrl: "",
        creditScore: 100,
        creditLevel: "A"
      };
      return {
        fromItemId: record.fromItemId,
        toItemId: targetItemId,
        createdAt: record.createdAt,
        fromItem,
        fromUser,
        matched: Boolean(matchMap[pairKey] && matchMap[pairKey].status === "matched")
      };
    })
    .filter(Boolean);

  return { success: true, list };
};
