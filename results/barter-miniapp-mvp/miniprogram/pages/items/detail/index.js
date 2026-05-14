const { call } = require("../../../services/api");

Page({
  data: {
    id: "",
    item: null
  },
  onLoad(options) {
    this.setData({ id: options.id || "" });
  },
  onShow() {
    this.loadDetail();
  },
  async loadDetail() {
    if (!this.data.id) {
      return;
    }
    try {
      const result = await call("getItemDetail", { itemId: this.data.id });
      this.setData({ item: result.item });
    } catch (error) {
      wx.showToast({ title: error.message, icon: "none" });
    }
  },
  onGoSwipe() {
    wx.navigateTo({
      url: `/pages/match/swipe/index?itemId=${this.data.id}`
    });
  },
  onGoIncoming() {
    wx.navigateTo({
      url: `/pages/match/incoming/index?itemId=${this.data.id}`
    });
  }
});
