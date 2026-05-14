function call(name, data = {}) {
  return wx.cloud.callFunction({
    name,
    data
  }).then((res) => {
    const result = res.result || {};
    if (result.success === false) {
      return Promise.reject(new Error(result.message || "请求失败"));
    }
    return result;
  });
}

module.exports = {
  call
};
