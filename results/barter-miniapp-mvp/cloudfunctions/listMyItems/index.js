const cloud = require("wx-server-sdk");

cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV });

exports.main = async (event) => {
  const wxContext = cloud.getWXContext();
  if (!wxContext.OPENID) {
    return { success: false, message: "未登录" };
  }
  const db = cloud.database();
  const limit = Math.min(Number(event.limit) || 20, 50);
  const res = await db
    .collection("items")
    .where({
      ownerOpenId: wxContext.OPENID,
      status: db.command.neq("deleted")
    })
    .orderBy("createdAt", "desc")
    .limit(limit)
    .get();
  return { success: true, items: res.data || [] };
};
