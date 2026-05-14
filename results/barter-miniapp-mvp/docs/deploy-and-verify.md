# 部署与最小验证说明（MVP）

## 1. 部署准备
- 微信开发者工具导入目录：`results/barter-miniapp-mvp/miniprogram`
- 云开发环境：在 `miniprogram/app.js` 中将 `envId` 替换为实际环境 ID
- 云函数目录：`results/barter-miniapp-mvp/cloudfunctions`

## 2. 云数据库初始化
1. 创建集合：`users`、`items`、`swipes`、`matches`
2. 按 `docs/cloudbase-indexes.md` 创建索引
3. 在云开发控制台数据库权限中应用 `docs/cloudbase-security-rules.jsonc`（按环境规则微调）

## 3. 云函数部署顺序
依次上传并部署以下函数：
1. `login`
2. `createItem`
3. `listMyItems`
4. `getItemDetail`
5. `getMatchCandidates`
6. `recordSwipe`
7. `listIncomingLikes`
8. `respondIncomingLike`
9. `getProfile`
10. `updateProfile`

## 4. 最小可运行验证（本地已执行）
- JS 语法校验：
  - 执行：`node --check`（脚本遍历 `results/barter-miniapp-mvp` 下全部 `.js`）
  - 结果：`checked_js_files=21`，`syntax_check=passed`
- 云函数完整性校验：
  - 检查 10 个必需云函数均存在 `index.js + package.json`
  - 结果：`missing=none`

## 5. 小程序端手工验收清单
1. 登录：首次进入未登录状态可跳转登录页并登录成功
2. 发布：至少 1 张图、描述、标签、价格可发布成功；非法数据会被拦截
3. 匹配：仅出现价格差 10% 内候选；左滑/右滑可落库
4. 喜欢我的：可看到来自他人物品的喜欢记录
5. 双向匹配：在“喜欢我的”点“我也喜欢”后显示匹配成功
6. 我的页：可加载信用分/等级、最近发布，简介可编辑并保存

## 6. 灰度建议
- 建议先在测试环境开放给 20-50 位种子用户
- 开启云函数调用日志，重点关注：
  - `recordSwipe` 去重与价格校验失败率
  - `respondIncomingLike` 匹配成功率
  - `updateProfile` 参数校验失败率

## 7. 正式发布（须在你本机完成，无法由远程代操作）

以下步骤需使用**你的**微信开发者账号、管理员扫码与网络环境；我无法代替你登录微信公众平台或点击「上传」。

1. 安装并打开 **微信开发者工具**，选择「导入项目」。
2. 项目目录选择：`results/barter-miniapp-mvp/miniprogram`（仓库内完整路径见上文 `deploy-and-verify` 第 1 节）。
3. 在 `project.config.json` 中填写你的 **AppID**（若留空，可在导入向导里填写）。
4. 确认 `miniprogram/app.js` 中 `envId` 已改为你的 **云开发环境 ID**。
5. 在云开发面板中确认：数据库集合、索引、权限已按第 2～3 节配置；10 个云函数均已「上传并部署」。
6. 开发者工具菜单：**上传** → 填写版本号与项目备注 → 上传成功。
7. 浏览器打开 [微信公众平台](https://mp.weixin.qq.com/) → **管理** → **版本管理**：
   - 可先设为 **体验版**，添加体验成员做最后一轮验收；
   - 再 **提交审核**（按类目准备资质与隐私说明）；
   - 审核通过后 **发布**。

说明：自动化 CI 上传（如 `miniprogram-ci`）需你在本机配置私钥与 AppID 等敏感信息，建议使用环境变量，勿写入仓库；需要时可另开任务单独加脚本模板。
