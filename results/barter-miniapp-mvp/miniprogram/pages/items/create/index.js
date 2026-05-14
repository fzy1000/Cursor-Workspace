const { call } = require("../../../services/api");

Page({
  data: {
    images: [],
    description: "",
    tagsInput: "",
    price: "",
    submitting: false
  },
  onDescriptionInput(e) {
    this.setData({ description: e.detail.value });
  },
  onTagsInput(e) {
    this.setData({ tagsInput: e.detail.value });
  },
  onPriceInput(e) {
    this.setData({ price: e.detail.value });
  },
  async onChooseImages() {
    const chooseRes = await wx.chooseMedia({
      count: 9 - this.data.images.length,
      mediaType: ["image"],
      sourceType: ["album", "camera"]
    });
    const selected = chooseRes.tempFiles || [];
    if (!selected.length) {
      return;
    }
    wx.showLoading({ title: "上传中" });
    try {
      const uploaded = [];
      for (const file of selected) {
        const ext = file.tempFilePath.split(".").pop();
        const cloudPath = `items/${Date.now()}-${Math.random().toString(36).slice(2)}.${ext}`;
        const uploadRes = await wx.cloud.uploadFile({
          cloudPath,
          filePath: file.tempFilePath
        });
        uploaded.push(uploadRes.fileID);
      }
      this.setData({
        images: this.data.images.concat(uploaded)
      });
    } catch (error) {
      wx.showToast({ title: error.message || "上传失败", icon: "none" });
    } finally {
      wx.hideLoading();
    }
  },
  onRemoveImage(e) {
    const index = Number(e.currentTarget.dataset.index);
    const images = this.data.images.slice();
    images.splice(index, 1);
    this.setData({ images });
  },
  validate() {
    const { images, description, tagsInput, price } = this.data;
    if (images.length < 1) {
      return "至少上传 1 张图片";
    }
    if (!description.trim()) {
      return "请填写物品描述";
    }
    if (description.trim().length > 200) {
      return "描述不能超过 200 字";
    }
    const num = Number(price);
    if (!num || num <= 0) {
      return "请输入正确价格";
    }
    const tags = tagsInput
      .split(/[,\uff0c\s]+/)
      .map((i) => i.trim())
      .filter(Boolean);
    if (tags.length > 10) {
      return "标签不能超过 10 个";
    }
    if (tags.some((tag) => tag.length > 12)) {
      return "单个标签不能超过 12 字";
    }
    return "";
  },
  async onSubmit() {
    const message = this.validate();
    if (message) {
      wx.showToast({ title: message, icon: "none" });
      return;
    }
    this.setData({ submitting: true });
    try {
      const tags = this.data.tagsInput
        .split(/[,\uff0c\s]+/)
        .map((i) => i.trim())
        .filter(Boolean);
      await call("createItem", {
        images: this.data.images,
        description: this.data.description.trim(),
        tags,
        price: Number(this.data.price)
      });
      wx.showToast({ title: "发布成功", icon: "success" });
      setTimeout(() => {
        wx.navigateBack();
      }, 300);
    } catch (error) {
      wx.showToast({ title: error.message || "发布失败", icon: "none" });
    } finally {
      this.setData({ submitting: false });
    }
  }
});
