const cloud = require("wx-server-sdk");

cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV });

exports.main = async (event) => {
  const wxContext = cloud.getWXContext();
  const openid = wxContext.OPENID;
  if (!openid) {
    return { success: false, message: "未登录" };
  }

  const bio = String(event.bio || "").trim();
  if (bio.length > 150) {
    return { success: false, message: "简介不能超过 150 字" };
  }

  const db = cloud.database();
  const users = db.collection("users");
  const now = Date.now();
  const userRes = await users.doc(openid).get().catch(() => null);
  if (!userRes || !userRes.data) {
    return { success: false, message: "用户不存在，请先登录" };
  }

  await users.doc(openid).update({
    data: {
      bio,
      updatedAt: now
    }
  });
  return { success: true };
};
