const cloud = require("wx-server-sdk");

cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV });

exports.main = async (event) => {
  const itemId = event.itemId;
  if (!itemId) {
    return { success: false, message: "缺少 itemId" };
  }
  const db = cloud.database();
  const res = await db.collection("items").doc(itemId).get().catch(() => null);
  if (!res || !res.data) {
    return { success: false, message: "物品不存在" };
  }
  return { success: true, item: res.data };
};
