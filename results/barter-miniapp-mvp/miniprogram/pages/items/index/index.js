const { call } = require("../../../services/api");

Page({
  data: {
    loading: false,
    items: []
  },
  onShow() {
    this.loadItems();
  },
  async loadItems() {
    this.setData({ loading: true });
    try {
      const result = await call("listMyItems", { limit: 20 });
      this.setData({ items: result.items || [] });
    } catch (error) {
      if (error.message.includes("未登录")) {
        wx.redirectTo({
          url: "/pages/login/index"
        });
        return;
      }
      wx.showToast({ title: error.message, icon: "none" });
    } finally {
      this.setData({ loading: false });
    }
  },
  onCreateTap() {
    wx.navigateTo({
      url: "/pages/items/create/index"
    });
  },
  onItemTap(e) {
    const itemId = e.currentTarget.dataset.id;
    wx.navigateTo({
      url: `/pages/items/detail/index?id=${itemId}`
    });
  }
});
