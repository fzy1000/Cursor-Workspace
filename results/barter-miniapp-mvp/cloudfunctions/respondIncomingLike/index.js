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

  const targetItemId = String(event.targetItemId || "").trim();
  const fromItemId = String(event.fromItemId || "").trim();
  const action = String(event.action || "like").trim();
  if (!targetItemId || !fromItemId) {
    return { success: false, message: "缺少物品参数" };
  }
  if (targetItemId === fromItemId) {
    return { success: false, message: "不能操作同一物品" };
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

  const targetRes = await getDocSafe(items, targetItemId);
  const fromRes = await getDocSafe(items, fromItemId);
  if (!targetRes || !targetRes.data || !fromRes || !fromRes.data) {
    return { success: false, message: "物品不存在" };
  }
  const targetItem = targetRes.data;
  const fromItem = fromRes.data;
  if (targetItem.ownerOpenId !== openid) {
    return { success: false, message: "无权限处理该请求" };
  }
  if (fromItem.ownerOpenId === openid) {
    return { success: false, message: "不能处理自己发起的请求" };
  }
  if (targetItem.status !== "active" || fromItem.status !== "active") {
    return { success: false, message: "仅可匹配上架中的物品" };
  }

  const basePrice = Number(targetItem.price);
  const candidatePrice = Number(fromItem.price);
  const diffRatio = Math.abs(candidatePrice - basePrice) / basePrice;
  if (!basePrice || diffRatio > 0.1) {
    return { success: false, message: "候选物品价格差超过 10%" };
  }

  const existingSwipeRes = await swipes
    .where({
      fromItemId: targetItemId,
      toItemId: fromItemId
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
        fromItemId: targetItemId,
        toItemId: fromItemId,
        action,
        createdAt: now
      }
    });
  }

  if (action !== "like") {
    return { success: true, matched: false };
  }

  const oppositeRes = await swipes
    .where({
      fromItemId,
      toItemId: targetItemId,
      action: "like"
    })
    .limit(1)
    .get();
  if (!oppositeRes.data || oppositeRes.data.length === 0) {
    return { success: true, matched: false };
  }

  const pairKey = getPairKey(targetItemId, fromItemId);
  const matchRes = await matches.where({ pairKey }).limit(1).get();
  let needCreditUpdate = false;
  if (!matchRes.data || matchRes.data.length === 0) {
    await matches.add({
      data: {
        pairKey,
        itemAId: targetItemId,
        itemBId: fromItemId,
        userAOpenId: targetItem.ownerOpenId,
        userBOpenId: fromItem.ownerOpenId,
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
    items.doc(targetItemId).update({ data: { status: "matched", updatedAt: now } }).catch(() => null),
    items.doc(fromItemId).update({ data: { status: "matched", updatedAt: now } }).catch(() => null)
  ]);
  if (needCreditUpdate) {
    await Promise.all([
      users.doc(targetItem.ownerOpenId).update({ data: { matchedCount: _.inc(1), updatedAt: now } }).catch(() => null),
      users.doc(fromItem.ownerOpenId).update({ data: { matchedCount: _.inc(1), updatedAt: now } }).catch(() => null)
    ]);
  }

  return { success: true, matched: true };
};
