let inited = false;

function initCloud(envId) {
  if (inited) {
    return;
  }
  if (!wx.cloud) {
    throw new Error("基础库不支持云开发，请升级微信版本。");
  }
  wx.cloud.init({
    env: envId,
    traceUser: true
  });
  inited = true;
}

module.exports = {
  initCloud
};
