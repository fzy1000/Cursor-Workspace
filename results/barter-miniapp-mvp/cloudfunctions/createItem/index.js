const cloud = require("wx-server-sdk");

cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV });

function validate(payload) {
  if (!Array.isArray(payload.images) || payload.images.length < 1 || payload.images.length > 9) {
    return "图片数量需在 1-9 张";
  }
  if (payload.images.some((id) => !String(id || "").trim())) {
    return "图片标识不能为空";
  }
  const description = String(payload.description || "").trim();
  if (!description || description.length > 200) {
    return "描述长度需在 1-200 字";
  }
  const tags = Array.isArray(payload.tags) ? payload.tags : [];
  if (tags.length > 10) {
    return "标签最多 10 个";
  }
  if (tags.some((tag) => String(tag || "").trim().length > 12)) {
    return "单个标签不能超过 12 字";
  }
  const price = Number(payload.price);
  if (!price || price <= 0) {
    return "价格必须大于 0";
  }
  return "";
}

exports.main = async (event) => {
  const wxContext = cloud.getWXContext();
  if (!wxContext.OPENID) {
    return { success: false, message: "未登录" };
  }
  const message = validate(event);
  if (message) {
    return { success: false, message };
  }
  const db = cloud.database();
  const now = Date.now();
  const data = {
    ownerOpenId: wxContext.OPENID,
    images: event.images,
    description: String(event.description).trim(),
    tags: (event.tags || []).map((i) => String(i).trim()).filter(Boolean).slice(0, 10),
    price: Number(event.price),
    status: "active",
    createdAt: now,
    updatedAt: now
  };
  const res = await db.collection("items").add({ data });
  return { success: true, itemId: res._id };
};
