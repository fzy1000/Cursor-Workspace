const cloud = require("wx-server-sdk");

cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV });

function getCreditLevel(score) {
  if (score >= 90) {
    return "A";
  }
  if (score >= 75) {
    return "B";
  }
  if (score >= 60) {
    return "C";
  }
  return "D";
}

exports.main = async (event) => {
  const wxContext = cloud.getWXContext();
  const openid = wxContext.OPENID;
  if (!openid) {
    return { success: false, message: "未登录" };
  }

  const db = cloud.database();
  const _ = db.command;
  const users = db.collection("users");
  const items = db.collection("items");
  const limit = Math.min(Math.max(Number(event.limit) || 5, 1), 10);

  const userRes = await users.doc(openid).get().catch(() => null);
  if (!userRes || !userRes.data) {
    return { success: false, message: "用户不存在，请先登录" };
  }
  const user = userRes.data;
  const profile = {
    ...user,
    creditLevel: getCreditLevel(Number(user.creditScore || 100))
  };
  if (profile.creditLevel !== user.creditLevel) {
    await users.doc(openid).update({
      data: {
        creditLevel: profile.creditLevel,
        updatedAt: Date.now()
      }
    });
  }

  const itemsRes = await items
    .where({
      ownerOpenId: openid,
      status: _.neq("deleted")
    })
    .orderBy("createdAt", "desc")
    .limit(limit)
    .get();

  return {
    success: true,
    profile,
    recentItems: itemsRes.data || []
  };
};
