const { initCloud } = require("./utils/cloud");

App({
  globalData: {
    userInfo: null,
    openid: "",
    envId: "your-cloud-env-id"
  },
  onLaunch() {
    initCloud(this.globalData.envId);
  }
});
