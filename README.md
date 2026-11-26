# 小博客

基于 Gridea 生成的静态博客，托管在 GitHub Pages。

- 仓库：`https://github.com/wcwtfhvk/wcwtfhvk.github.io`
- 自定义域名：`https://blog.404520.xyz`（见 `CNAME`）
- 实际推送分支：`master`

---

## ⚠️ 重要：CSS 样式失效问题（2026-11-26 已修复）

### 现象

打开博客只剩纯文本：字体是默认样式、链接带下划线、内容左对齐不居中，头像和配图也不显示。**CSS 文件本身没有任何问题**。

### 根因

Gridea 生成的 HTML 把资源地址写死成了 GitHub 默认域名：

```html
<link rel="stylesheet" href="https://wcwtfhvk.github.io/styles/main.css">
```

仓库绑定了自定义域名后，GitHub Pages 会把 `wcwtfhvk.github.io` 的请求 **301 跳转到 `http://blog.404520.xyz/...`（注意是 http）**。于是 HTTPS 页面去加载 HTTP 资源，被浏览器的**混合内容（Mixed Content）策略拦截**，CSS、图片全部加载失败。

验证方法：

```bash
curl -sI https://wcwtfhvk.github.io/styles/main.css
# 返回 301，Location: http://blog.404520.xyz/styles/main.css  ← 降级成 http
```

### 修复方式

把 HTML 里的绝对地址全部换成**根相对路径**，不依赖域名和协议：

```html
<link rel="stylesheet" href="/styles/main.css">
```

本次已处理：39 个 HTML 共 406 处替换，`atom.xml` 25 处改为 `https://blog.404520.xyz`（订阅源必须保留绝对地址）。提交：`a5ee501`。

### 下次复发怎么办（一键修复）

如果用 Gridea 重新生成并推送，绝对地址会被写回来，问题会**再次出现**。此时在仓库根目录运行：

```bat
fix-urls.bat
```

该脚本会自动完成全部替换，然后提交并推送：

```bash
python fix-urls.py
git add -A
git commit -m "Fix CSS: use root-relative URLs"
git push origin master
```

推送后等约 1 分钟 GitHub Pages 重新构建，刷新博客确认样式恢复。

### 从源头预防

重新用 Gridea 生成前，任选其一：

1. **改 Gridea 站点地址**：在 Gridea 的站点设置里，把站点地址从 `https://wcwtfhvk.github.io` 改成 `https://blog.404520.xyz`。这是最根本的做法。
2. **开启强制 HTTPS**：GitHub 仓库 → Settings → Pages → 勾选 **Enforce HTTPS**，让 301 跳转到 https 而非 http。
3. **生成后跑一次 `fix-urls.bat`**（即方案一，最省事，且换域名也不会复发）。

### 快速自查

样式再次不对时，先看页面源码头部：

```bash
curl -s https://blog.404520.xyz/ | grep 'main.css'
```

- `href="/styles/main.css"` → 正常
- `href="https://wcwtfhvk.github.io/styles/main.css"` → 中招了，跑 `fix-urls.bat`

再确认跳转是否降级：

```bash
curl -sI https://wcwtfhvk.github.io/styles/main.css | grep -i location
```

- 出现 `http://` → 就是这个问题
