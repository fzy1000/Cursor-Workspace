const cloud = require("wx-server-sdk");

cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV });

function getPairKey(a, b) {
  return [String(a), String(b)].sort().join("#");
}

async function getDocSafe(collection, docId) {
  return collection.doc(docId).get().catch(() => null);
}

exports.main = async (event) => {
  const wxContext = cloud.getWXContext();
  const openid = wxContext.OPENID;
  if (!openid) {
    return { success: false, message: "未登录" };
  }

  const fromItemId = String(event.fromItemId || "").trim();
  const toItemId = String(event.toItemId || "").trim();
  const action = String(event.action || "").trim();
  if (!fromItemId || !toItemId) {
    return { success: false, message: "缺少物品参数" };
  }
  if (fromItemId === toItemId) {
    return { success: false, message: "不能对同一物品滑动" };
  }
  if (!["like", "dislike"].includes(action)) {
    return { success: false, message: "非法操作类型" };
  }

  const db = cloud.database();
  const _ = db.command;
  const items = db.collection("items");
  const swipes = db.collection("swipes");
  const matches = db.collection("matches");
  const users = db.collection("users");
  const now = Date.now();

  const fromItemRes = await getDocSafe(items, fromItemId);
  const toItemRes = await getDocSafe(items, toItemId);
  if (!fromItemRes || !fromItemRes.data || !toItemRes || !toItemRes.data) {
    return { success: false, message: "物品不存在" };
  }
  const fromItem = fromItemRes.data;
  const toItem = toItemRes.data;
  if (fromItem.ownerOpenId !== openid) {
    return { success: false, message: "无权限操作该物品" };
  }
  if (toItem.ownerOpenId === openid) {
    return { success: false, message: "不能选择自己的物品" };
  }
  if (fromItem.status !== "active" || toItem.status !== "active") {
    return { success: false, message: "仅可匹配上架中的物品" };
  }

  const basePrice = Number(fromItem.price);
  const candidatePrice = Number(toItem.price);
  const diffRatio = Math.abs(candidatePrice - basePrice) / basePrice;
  if (!basePrice || diffRatio > 0.1) {
    return { success: false, message: "候选物品价格差超过 10%" };
  }

  const existingSwipeRes = await swipes
    .where({
      fromItemId,
      toItemId
    })
    .limit(1)
    .get();
  if (existingSwipeRes.data && existingSwipeRes.data.length > 0) {
    await swipes.doc(existingSwipeRes.data[0]._id).update({
      data: {
        action,
        createdAt: now
      }
    });
  } else {
    await swipes.add({
      data: {
        fromOpenId: openid,
        fromItemId,
        toItemId,
        action,
        createdAt: now
      }
    });
  }

  if (action !== "like") {
    return { success: true, matched: false };
  }

  const reverseSwipeRes = await swipes
    .where({
      fromItemId: toItemId,
      toItemId: fromItemId,
      action: "like"
    })
    .limit(1)
    .get();

  if (!reverseSwipeRes.data || reverseSwipeRes.data.length === 0) {
    return { success: true, matched: false };
  }

  const pairKey = getPairKey(fromItemId, toItemId);
  const matchRes = await matches.where({ pairKey }).limit(1).get();
  let needCreditUpdate = false;
  if (!matchRes.data || matchRes.data.length === 0) {
    await matches.add({
      data: {
        pairKey,
        itemAId: fromItemId,
        itemBId: toItemId,
        userAOpenId: fromItem.ownerOpenId,
        userBOpenId: toItem.ownerOpenId,
        status: "matched",
        createdAt: now,
        matchedAt: now
      }
    });
    needCreditUpdate = true;
  } else if (matchRes.data[0].status !== "matched") {
    await matches.doc(matchRes.data[0]._id).update({
      data: {
        status: "matched",
        matchedAt: now
      }
    });
    needCreditUpdate = true;
  }

  await Promise.all([
    items.doc(fromItemId).update({ data: { status: "matched", updatedAt: now } }).catch(() => null),
    items.doc(toItemId).update({ data: { status: "matched", updatedAt: now } }).catch(() => null)
  ]);

  if (needCreditUpdate) {
    await Promise.all([
      users.doc(fromItem.ownerOpenId).update({ data: { matchedCount: _.inc(1), updatedAt: now } }).catch(() => null),
      users.doc(toItem.ownerOpenId).update({ data: { matchedCount: _.inc(1), updatedAt: now } }).catch(() => null)
    ]);
  }

  return { success: true, matched: true };
};
