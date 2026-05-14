const { call } = require("../../services/api");

Page({
  data: {
    loading: false,
    agreed: true
  },
  onChangeAgree(e) {
    this.setData({ agreed: e.detail.value.length > 0 });
  },
  async onLoginTap() {
    if (!this.data.agreed) {
      wx.showToast({ title: "请先勾选协议", icon: "none" });
      return;
    }
    this.setData({ loading: true });
    try {
      const profile = await wx.getUserProfile({
        desc: "用于创建你的以物换物账号"
      });
      const result = await call("login", {
        userInfo: profile.userInfo
      });
      const app = getApp();
      app.globalData.openid = result.openid;
      app.globalData.userInfo = result.user;
      wx.showToast({ title: "登录成功", icon: "success" });
      setTimeout(() => {
        wx.switchTab({
          url: "/pages/items/index"
        });
      }, 300);
    } catch (error) {
      wx.showToast({ title: error.message || "登录失败", icon: "none" });
    } finally {
      this.setData({ loading: false });
    }
  }
});
