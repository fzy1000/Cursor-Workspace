const cloud = require("wx-server-sdk");

cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV });

exports.main = async (event) => {
  const wxContext = cloud.getWXContext();
  const openid = wxContext.OPENID;
  if (!openid) {
    return { success: false, message: "未登录" };
  }
  const baseItemId = event.baseItemId;
  if (!baseItemId) {
    return { success: false, message: "缺少 baseItemId" };
  }

  const db = cloud.database();
  const _ = db.command;
  const baseRes = await db.collection("items").doc(baseItemId).get().catch(() => null);
  if (!baseRes || !baseRes.data) {
    return { success: false, message: "基准物品不存在" };
  }
  const baseItem = baseRes.data;
  if (baseItem.ownerOpenId !== openid) {
    return { success: false, message: "无权限使用该物品匹配" };
  }

  const swipeRes = await db
    .collection("swipes")
    .where({
      fromItemId: baseItemId
    })
    .get();
  const swipedIds = (swipeRes.data || []).map((i) => i.toItemId);
  const minPrice = Number((baseItem.price * 0.9).toFixed(2));
  const maxPrice = Number((baseItem.price * 1.1).toFixed(2));

  const where = {
    ownerOpenId: _.neq(openid),
    status: "active",
    price: _.gte(minPrice).and(_.lte(maxPrice))
  };
  if (swipedIds.length > 0) {
    where._id = _.nin(swipedIds);
  }
  const res = await db
    .collection("items")
    .where(where)
    .orderBy("createdAt", "desc")
    .limit(50)
    .get();
  const candidates = (res.data || []).map((item) => {
    const diff = Math.abs(item.price - baseItem.price) / baseItem.price;
    return {
      ...item,
      diffPercent: (diff * 100).toFixed(2)
    };
  });
  return { success: true, candidates };
};
