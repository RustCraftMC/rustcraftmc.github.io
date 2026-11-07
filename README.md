# rustcraftmc.github.io

RustCraftMC Team 的组织首页和 Cairn Launcher 官网，放在同一个仓库里：

| 地址 | 内容 |
| --- | --- |
| `https://rustcraftmc.github.io/` | 组织首页（`index.html`，英文在 `en/`） |
| `https://rustcraftmc.github.io/cairnlauncher/` | Cairn Launcher 官网（中文默认，英文在 `cairnlauncher/en/`） |
| `/cairnlauncher/terms/`、`/cairnlauncher/privacy/` | 用户协议、隐私政策网页版（英文版在 `/cairnlauncher/en/` 下） |

纯静态页面，没有构建步骤，不加载任何第三方脚本、字体或统计，不设 Cookie。`.github/workflows/pages.yml` 把公开文件复制到 `_site` 后用官方的 Pages 工作流发布。

## 本地预览

```bash
python -m http.server 4173 --bind 127.0.0.1
```

然后打开 `http://127.0.0.1:4173/`。目录结构和线上一致，`/cairnlauncher/` 也能直接打开。

## 检查链接和资源

```bash
python tools/verify_site.py
```

## 会重新生成的部分

- **法务页面**：`python tools/build_legal.py [启动器仓库路径]`。从启动器仓库的 `TERMS.md`、`TERMS.en.md`、`PRIVACY.md`、`PRIVACY.en.md` 逐字生成四个网页，并校验文字没有被改动；协议更新后重跑即可，默认读取和本仓库并排的 `CairnLauncher` 文件夹。
- **界面截图**：启动器仓库里有 `#[ignore]` 的导出测试，`CAIRN_SITE_SHOTS_DIR=<目录> cargo test -p cairn-app export_site -- --ignored` 导出原始 PNG，再用 `python tools/optimize_shots.py <目录>` 转成 `cairnlauncher/assets/shots/` 下的 WebP。
- **分享图和图标**：`python tools/make_og.py`（需要 Windows 自带字体）。

`tools/legacy/` 是早期的页面生成器和样式源文件，对应旧版设计。现在的页面、样式和脚本直接在 `index.html`、`cairnlauncher/` 和 `assets/` 里维护，**不要运行 `tools/legacy/` 里的脚本**，它会用旧版覆盖现在的页面。
