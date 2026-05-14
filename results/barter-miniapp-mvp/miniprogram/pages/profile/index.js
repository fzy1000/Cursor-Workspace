const { call } = require("../../services/api");

Page({
  data: {
    profile: null,
    recentItems: [],
    editingBio: false,
    bioInput: ""
  },
  onShow() {
    this.loadProfile();
  },
  async loadProfile() {
    try {
      const result = await call("getProfile", { limit: 5 });
      this.setData({
        profile: result.profile,
        recentItems: result.recentItems || [],
        bioInput: (result.profile && result.profile.bio) || ""
      });
    } catch (error) {
      if (error.message.includes("未登录")) {
        wx.redirectTo({ url: "/pages/login/index" });
        return;
      }
      wx.showToast({ title: error.message || "加载失败", icon: "none" });
    }
  },
  onEditBio() {
    this.setData({ editingBio: true });
  },
  onBioInput(e) {
    this.setData({ bioInput: e.detail.value.slice(0, 150) });
  },
  async onSaveBio() {
    try {
      await call("updateProfile", { bio: this.data.bioInput });
      this.setData({ editingBio: false });
      wx.showToast({ title: "已保存", icon: "success" });
      this.loadProfile();
    } catch (error) {
      wx.showToast({ title: error.message || "保存失败", icon: "none" });
    }
  }
});
