const { call } = require("../../../services/api");

Page({
  data: {
    itemId: "",
    candidates: [],
    currentIndex: 0,
    empty: false
  },
  onLoad(options) {
    this.setData({ itemId: options.itemId || "" });
  },
  onShow() {
    this.loadCandidates();
  },
  async loadCandidates() {
    try {
      const result = await call("getMatchCandidates", { baseItemId: this.data.itemId });
      const candidates = result.candidates || [];
      this.setData({
        candidates,
        currentIndex: 0,
        empty: candidates.length === 0
      });
    } catch (error) {
      wx.showToast({ title: error.message || "加载失败", icon: "none" });
    }
  },
  get currentCandidate() {
    return this.data.candidates[this.data.currentIndex] || null;
  },
  onDislike() {
    this.handleSwipe("dislike");
  },
  onLike() {
    this.handleSwipe("like");
  },
  async handleSwipe(action) {
    const candidate = this.currentCandidate;
    if (!candidate) {
      return;
    }
    try {
      const result = await call("recordSwipe", {
        fromItemId: this.data.itemId,
        toItemId: candidate._id,
        action
      });
      if (result.matched) {
        wx.showModal({
          title: "匹配成功",
          content: "你们互相喜欢，已达成匹配",
          showCancel: false
        });
      }
      const nextIndex = this.data.currentIndex + 1;
      const empty = nextIndex >= this.data.candidates.length;
      this.setData({
        currentIndex: nextIndex,
        empty
      });
    } catch (error) {
      wx.showToast({ title: error.message, icon: "none" });
    }
  }
});
