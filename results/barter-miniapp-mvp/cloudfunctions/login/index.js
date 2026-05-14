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
    return { success: false, message: "未获取到登录身份" };
  }
  const db = cloud.database();
  const users = db.collection("users");
  const now = Date.now();
  const userInfo = event.userInfo || {};

  const current = await users.doc(openid).get().catch(() => null);
  if (!current || !current.data) {
    const doc = {
      _id: openid,
      nickName: userInfo.nickName || "微信用户",
      avatarUrl: userInfo.avatarUrl || "",
      bio: "",
      creditScore: 100,
      creditLevel: getCreditLevel(100),
      matchedCount: 0,
      complaintCount: 0,
      createdAt: now,
      updatedAt: now
    };
    await users.doc(openid).set({ data: doc });
    return { success: true, openid, user: doc };
  }

  const data = current.data;
  await users.doc(openid).update({
    data: {
      nickName: userInfo.nickName || data.nickName,
      avatarUrl: userInfo.avatarUrl || data.avatarUrl,
      creditLevel: getCreditLevel(data.creditScore || 100),
      updatedAt: now
    }
  });
  return {
    success: true,
    openid,
    user: {
      ...data,
      nickName: userInfo.nickName || data.nickName,
      avatarUrl: userInfo.avatarUrl || data.avatarUrl
    }
  };
};
