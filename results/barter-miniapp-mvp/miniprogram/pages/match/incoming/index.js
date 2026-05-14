const { call } = require("../../../services/api");

Page({
  data: {
    itemId: "",
    list: [],
    loading: false
  },
  onLoad(options) {
    this.setData({ itemId: options.itemId || "" });
  },
  onShow() {
    this.loadList();
  },
  async loadList() {
    this.setData({ loading: true });
    try {
      const result = await call("listIncomingLikes", { targetItemId: this.data.itemId });
      this.setData({ list: result.list || [] });
    } catch (error) {
      wx.showToast({ title: error.message || "加载失败", icon: "none" });
    } finally {
      this.setData({ loading: false });
    }
  },
  async onAccept(e) {
    const fromItemId = e.currentTarget.dataset.fromitemid;
    const current = (this.data.list || []).find((it) => it.fromItemId === fromItemId);
    if (current && current.matched) {
      wx.showToast({ title: "该请求已匹配", icon: "none" });
      return;
    }
    try {
      const res = await call("respondIncomingLike", {
        targetItemId: this.data.itemId,
        fromItemId,
        action: "like"
      });
      wx.showToast({
        title: res.matched ? "匹配成功" : "已处理",
        icon: "success"
      });
      this.loadList();
    } catch (error) {
      wx.showToast({ title: error.message, icon: "none" });
    }
  }
});
