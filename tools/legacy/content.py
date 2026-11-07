"""All the words on the Cairn Launcher page and the RustCraftMC Team page, in Chinese and English.

Every claim here strictly adheres to the launcher repository facts:
- README.md / README.zh-CN.md
- docs/BENCHMARK.md (2026-10-29)
- TERMS.md and PRIVACY.md (version 1.0, effective 2026-11-06)
- Cargo.toml and actual release binaries measured on the build machine.

Strings may contain formatting HTML (<code>, <a>, <i class="dot">); they are inserted as-is.
"""

# ---------------------------------------------------------------------------------------------- Cairn Launcher

CAIRN = {
    "zh": {
        "lang_attr": "zh-CN",
        "title": "Cairn Launcher — 纯粹 · 优雅 · 灵动的现代 Minecraft 启动器",
        "desc": "Cairn Launcher 是用 Rust 构建的原生第三方 Minecraft 启动器，面向 Windows 10 及更高版本。界面由自研 GUI 引擎原生绘制：不是 Java，不是网页，不是 Electron。完全开源。",
        "skip": "跳到正文",
        "nav_label": "主导航",
        "nav": [
            ("native", "原生"),
            ("tour", "导览"),
            ("measured", "实测"),
            ("privacy", "隐私"),
            ("download", "下载"),
        ],
        "switch": "English",
        "switch_attr": "en",
        "dl_short": "下载",
        "cairn_label": "章节索引",
        "stones": ["启程", "原生", "导览", "实测", "隐私", "下载"],

        # Hero
        "h1a": '纯粹 <i class="dot">·</i> 优雅 <i class="dot">·</i> 灵动',
        "h1b": "现代 Minecraft 原生启动器",
        "lede": "以 Rust 系统级语言雕琢每一个环节。告别庞大冗余的中间抽象，自绘轻快灵动的原生界面。安装、模组、账号、下载与崩溃诊断，在一扇精致的窗口中从容展开。",
        "cta_dl": "获取 Windows 版",
        "cta_src": "探索 GitHub 源码",
        "hero_note": "适用于 Windows 10 及更高版本 · 开源透明 · 第三方非官方启动器",
        "hero_alt": "Cairn Launcher 主界面：优雅的问候与时钟、本周游玩时长折线、活动热力图、快捷启动卡片，映衬在 GPU 合成的动态毛玻璃与风景壁纸之上",

        # Not Java, not a web view, not Electron
        "nots": [("不是 ", "Java", "。"), ("不是 ", "网页", "。"), ("不是 ", "Electron", "。")],
        "native_lede": "Cairn 是一座从头构建的单文件原生程序。它拒绝将网页封装为臃肿桌面应用的套路，而是依托完全自研的 GUI 引擎 <code>cairn-ui</code> 亲手绘制每一个像素，并在 GPU 硬件加速下合成自然通透的毛玻璃景深。",
        "facts": [
            (
                "没有 JVM，也没有浏览器内核",
                "启动器自身进程完全摆脱了 Java 虚拟机与 Chromium/WebView 运行时的沉重包袱。经过全面优化的 Release 构建仅为单个单文件 exe，体积仅约 9.6 MiB，轻装疾行。",
                False,
            ),
            (
                "自研图形引擎，亲手绘制每一个像素",
                "界面由本仓库自研的 <code>cairn-ui</code> 纯原生渲染：依托 <code>tiny-skia</code> 呈现细腻抗锯齿矢量、<code>cosmic-text</code> 精确排版复杂字形、<code>taffy</code> 高效解析弹性布局、<code>winit</code> 统管原生窗口。具备 OpenGL 3.3 时由 GPU 硬件合成真实毛玻璃，无 GPU 环境平滑回退至纯软件渲染。",
                False,
            ),
            (
                "启动器自身纯粹，而游戏本体依然需要 Java",
                "我们为启动器卸下了运行时的负担，但 Minecraft 游戏本身仍需 Java。Cairn 会根据每个版本的规范智能推导兼容的 Java 环境，并在本地缺失时自动下载 Mojang 官方运行时，无需手动繁琐配置。",
                True,
            ),
            (
                "独立进程宿主，沙盒隔离的 JavaScript 插件",
                "扩展插件采用标准的 JavaScript 编写，并在由 QuickJS-NG 驱动的独立宿主子进程中运行。任何涉及网络、本地文件或外部程序的调用均需你在启用时显式授权；即使插件遇到异常崩溃，启动器主界面依然稳固如初。",
                False,
            ),
        ],
        "stack": [
            ("cairn-ui", "自研控件体系 · 状态模型 · 优雅主题与动效", 56),
            ("taffy", "Flexbox / Grid 现代化弹性布局引擎", 66),
            ("cosmic-text", "高质量多语言文本排版与字形塑形", 78),
            ("tiny-skia", "纯 CPU 高性能抗锯齿 2D 矢量渲染", 90),
            ("winit · OpenGL", "系统原生窗口管线与 GPU 毛玻璃合成（支持软件回退）", 100),
        ],
        "stack_cap": "石堆（Cairn）的哲学：每一块基石各司其职，不添一分多余的重量。",

        # Tour
        "tour_h": "全链路生态，凝于方寸之间",
        "tour_sub": "将繁琐的版本架构、多源网络、账号隔离与崩溃分析沉淀于底层，呈现自然内敛的现代操作面貌。",
        "seg_theme": "界面主题",
        "seg_lang": "显示语言",
        "dark": "深色",
        "light": "浅色",
        "steps": [
            (
                "home",
                "模块化自定义仪表盘",
                "即刻启动、常用快捷方式、数字时钟、游玩时长折线统计与动态热力图一览无余。支持通过优雅的 YAML 格式自由扩展或随心摆放小组件。",
            ),
            (
                "new-instance",
                "全版本与全加载器生态",
                "跨越从最初的 Alpha、经典正式版到最新每周快照的所有官方版本（支持全新年份制版本号），开箱支持 Fabric、Quilt、Forge、NeoForge 与 OptiFine 快速安装。",
            ),
            (
                "instances",
                "多维度实例隔离与导入",
                "既可直接沿用官方 .minecraft 目录，也可建立相互隔离的独立实例并共享全局资源池；具备五档全局隔离策略与细粒度覆盖，并能自动发现并一键迁入已有启动器的数据。",
            ),
            (
                "accounts",
                "多源身份认证与硬件加密",
                "无缝集成微软 OAuth 设备码登录、自建或统一 Yggdrasil 外置认证（如 LittleSkin）以及离线账户。在 Windows 平台采用系统级 DPAPI 硬件加密保护凭据安全。",
            ),
            (
                "library",
                "模组探索与整合包流转",
                "直连 Modrinth 与 CurseForge 海量生态，自动分析并补全必要前置依赖，支持版本更新检查；完整支持 .mrpack、CurseForge 与 MultiMC / Prism 整合包的导入与导出。",
            ),
            (
                "settings-download",
                "自适应多源下载引擎",
                "聚合 Mojang 官方源、BMCLAPI、MCIM 镜像及自定义源，具备动态测速择优与故障自动熔断换源机制；支持自适应并发限流、流式计算 SHA-1 校验与大文件分块断点续传。",
            ),
            (
                "crash",
                "本地化日志与崩溃深度诊断",
                "游戏非正常退出时，启动器在本地深度比对日志、Crash Report 与 JVM hs_err 错误，以清晰的自然语言拆解崩溃根因，并可导出自动剔除敏感令牌的脱敏诊断包。",
            ),
            (
                "extensions",
                "安全可控的扩展插件生态",
                "支持声明式 YAML 主页小组件与面板，以及在独立 QuickJS-NG 沙盒子进程中运行的 JavaScript 脚本。权限调用按需确认，并支持使用 <code>--no-plugins</code> 参数进行完全隔离启动。",
            ),
            (
                "settings-appearance",
                "视觉定制与多语言支持",
                "深浅双色主题、动态拾取自定义强调色、带毛玻璃景深的自选壁纸与系统级高 DPI 平滑缩放。界面原生支持简体中文、English 与日本語三语。",
            ),
        ],

        # Measured
        "bench_h": "实测性能指标",
        "bench": [
            (
                "60",
                "ms",
                "NeoForge 1.21.1 完整启动准备",
                "完成配置解析、版本继承链推导、校验约 4,000 个游戏文件、确定兼容 Java 运行时、解压 natives 库并构建完整启动命令。10 次测量取中位数（经第二轮优化由 106 ms 降至 60 ms）。",
            ),
            (
                "32",
                "ms",
                "300 个模组超大整合包热扫描",
                "真实解压并解析 300 个模组 JAR 文件的元数据与依赖拓扑。注：首次无缓存冷盘完整读取并计算 SHA-1 耗时约 412 ms。",
            ),
            (
                "≈14",
                "MiB",
                "启动准备全流程峰值内存",
                "命令行核心进程在完成全量依赖与游戏文件准备时的真实工作集峰值，内存开销轻盈无感。",
            ),
            (
                "9.6",
                "MiB",
                "独立单文件可执行程序体积",
                "Release 构建下 <code>CairnLauncher.exe</code> 完整单文件体积为 10,046,464 字节；底层核心 CLI <code>cairn.exe</code> 仅约 5.2 MiB（5,473,792 字节）。",
            ),
        ],
        "bench_how_h": "基准测试硬件与测试环境",
        "bench_how": "测试设备：Intel Core i7-14700F（20 核 28 线程）、32 GB 内存、NVMe 固态硬盘、Windows 11 企业工作站版（Build 26200）。每项测试均由独立新进程执行，统计耗时包含进程创建全开销。测试于系统文件缓存预热状态下执行。",

        # Privacy
        "priv_h": "本地主权：你的数据始终留在你的设备上",
        "priv_sub": "严格遵循《隐私政策》（版本 1.0，2026-11-06 生效）并对齐 0.1.0 版源代码，恪守对本地主权的绝对尊重。",
        "priv": [
            (
                "零遥测、零统计、零广告、零静默上传",
                "启动器绝不包含任何用户行为统计、打点上报、崩溃远程上传或商业推广代码，开发者不收集亦不持有你的任何个人数据。",
            ),
            (
                "便携归一，数据就地存放",
                "所有账号凭据、配置项与实例默认聚合在可执行程序同级的 <code>.cairn</code> 目录（支持通过 <code>CAIRN_HOME</code> 灵活重定向）。物理删除该目录即可无痕清除。",
            ),
            (
                "直连官方受信任端点，拒绝中间转发",
                "账号登录、版本索引与资源下载均直连 Microsoft、Mojang、Modrinth、CurseForge 或你手动配置的镜像源，绝不经过开发者的任何中转代理服务器。",
            ),
            (
                "敏感凭据硬件级加密，配置明文透明",
                "在 Windows 环境下，敏感凭据由 Windows DPAPI 原生硬件级加密保存在 <code>accounts.dat</code>；其余普通配置以结构清晰的 JSON 明文呈现，透明易于备份。",
            ),
            (
                "绝无静默自动更新，掌控权交还用户",
                "启动器不会在后台进行静默联网检测或强制更新。一切新版本发布均透明公开于官方网站与 GitHub Release，由用户自主决定更新节奏。",
            ),
        ],
        "callout_h": "关于账号与游戏授权的合规声明",
        "callout": "离线账号仅为启动器本地配置的玩家名档案，绝不构成亦不能替代 Minecraft 游戏的正版软件授权。根据《用户协议》第 3 章规定：居住在中国大陆境外的用户，必须首先通过 Microsoft 官方流程登录拥有 Minecraft Java 版的正版账户，方可使用离线账号；居住在中国大陆境内的用户，强烈建议在持有正版授权的前提下使用。",
        "read_privacy": "阅读隐私政策",
        "read_terms": "阅读用户协议",

        # Download
        "get_h": "获取单文件版本，或由源码亲手构建",
        "get_lede": "目前面向 Windows 10 及更高版本系统提供原生支持。启动器采用免安装便携设计，解压即用，所有数据完全内敛于旁侧的 <code>.cairn</code> 文件夹中。",
        "get_dl": "前往 GitHub Releases 下载",
        "get_repo": "浏览 GitHub 源代码仓库",
        "get_facts": [
            "完全开源，代码透明托管于 GitHub；图形界面库 <code>cairn-ui</code> 遵循 MIT / Apache-2.0 双许可。",
            "无静默自动更新：请关注官方网站或 GitHub Release 频道获取后续更新版本。",
            "从源码构建要求：Windows 10 或更高版本系统，以及 Rust 1.91+（2024 Edition）。",
        ],
        "code_title": "从源代码快速编译",
        "code": [
            ("cargo run -p cairn-app", "启动桌面应用程序"),
            ("cargo build --release -p cairn-app", r"编译 target\release\CairnLauncher.exe"),
            ("cargo build --release -p cairn-cli", r"编译 target\release\cairn.exe"),
        ],
        "copy": "复制命令",
        "copied": "已复制到剪贴板",
    },

    "en": {
        "lang_attr": "en",
        "title": "Cairn Launcher — Pure, elegant, and modern Minecraft launcher",
        "desc": "Cairn Launcher is a native, third-party Minecraft launcher built with Rust for Windows 10 and newer. Rendered with our bespoke GUI library: not Java, not a web view, not Electron. Fully open source.",
        "skip": "Skip to content",
        "nav_label": "Main navigation",
        "nav": [
            ("native", "Native"),
            ("tour", "Tour"),
            ("measured", "Measured"),
            ("privacy", "Privacy"),
            ("download", "Download"),
        ],
        "switch": "中文",
        "switch_attr": "zh-CN",
        "dl_short": "Download",
        "cairn_label": "Chapters",
        "stones": ["Start", "Native", "Tour", "Measured", "Privacy", "Download"],

        # Hero
        "h1a": "Pure, elegant,",
        "h1b": "and modern Minecraft launcher",
        "lede": "Natively engineered with Rust. Stripping away runtime bloat and superfluous abstractions, Cairn pairs a responsive, self-rendered GUI with effortless management of instances, mods, accounts, and crash analytics.",
        "cta_dl": "Download for Windows",
        "cta_src": "Explore on GitHub",
        "hero_note": "Windows 10 or newer · Open source · Unofficial third-party launcher",
        "hero_alt": "Cairn Launcher interface: time greetings, weekly playtime stats, activity heatmap, and quick launch cards against a wallpaper with GPU-composited glass blur",

        # Not Java, not a web view, not Electron
        "nots": [("Not ", "Java", "."), ("Not a ", "web view", "."), ("Not ", "Electron", ".")],
        "native_lede": "Cairn is a single-binary native application built from scratch. Rather than wrapping web pages inside heavy desktop shells, it paints every pixel directly through our bespoke GUI framework <code>cairn-ui</code>, compositing depth and frosted glass on the GPU.",
        "facts": [
            (
                "No JVM, no embedded browser engine",
                "The launcher process carries zero Java virtual machine or Chromium/WebView overhead. The fully optimized release build is a single standalone executable of approximately 9.6 MiB.",
                False,
            ),
            (
                "A bespoke GUI stack that paints every pixel",
                "Engineered from the ground up: <code>tiny-skia</code> powers anti-aliased 2D vector drawing, <code>cosmic-text</code> handles complex typography, <code>taffy</code> calculates flexible layouts, and <code>winit</code> manages windows. With OpenGL 3.3, frosted glass is composited in real time on the GPU, gracefully falling back to pure software rendering when unavailable.",
                False,
            ),
            (
                "The launcher is native; the game still needs Java",
                "We eliminated JVM overhead from the launcher itself, but Minecraft remains a Java application. Cairn automatically determines the required Java version for any game version and downloads official Mojang runtimes if none is found locally.",
                True,
            ),
            (
                "Sandboxed JavaScript extensions in a distinct host",
                "Extensions are written in JavaScript and executed inside an isolated QuickJS-NG sub-process. Network, filesystem, or command-line permissions require explicit confirmation upon enablement; if a plugin crashes, the launcher stays rock-solid.",
                False,
            ),
        ],
        "stack": [
            ("cairn-ui", "Bespoke widgets · Reactive state · Fluid themes & motion", 56),
            ("taffy", "High-performance Flexbox and Grid layout engine", 66),
            ("cosmic-text", "Cross-platform multilingual text shaping & layout", 78),
            ("tiny-skia", "Pure CPU anti-aliased 2D vector renderer", 90),
            ("winit · OpenGL", "Native windowing & GPU glass compositing (software fallback)", 100),
        ],
        "stack_cap": "The philosophy of a cairn: each stone placed with purpose, without an ounce of excess.",

        # Tour
        "tour_h": "A cohesive ecosystem in one serene window",
        "tour_sub": "Taming version dependencies, multi-mirror downloads, account security, and crash diagnostics with quiet engineering precision.",
        "seg_theme": "Theme",
        "seg_lang": "Language",
        "dark": "Dark",
        "light": "Light",
        "steps": [
            (
                "home",
                "Modular, customizable dashboard",
                "Quick launch, shortcuts, digital clock, playtime curves, and dynamic activity heatmaps at a glance. Easily customize or craft custom widgets via clean YAML definitions.",
            ),
            (
                "new-instance",
                "Every official release and loader",
                "From historical alphas to the latest weekly snapshots (including the new calendar-based versions). One-click installation for Fabric, Quilt, Forge, NeoForge, and OptiFine.",
            ),
            (
                "instances",
                "Flexible isolation and instant import",
                "Organize game instances alongside the default .minecraft directory or in isolated sandboxes sharing a global asset pool. Includes five isolation presets and automatic one-click import from existing launchers.",
            ),
            (
                "accounts",
                "Multi-source authentication & hardware encryption",
                "Seamless Microsoft OAuth device-code sign-in, custom Yggdrasil external authentication (e.g., LittleSkin), and offline profiles. Tokens are secured via Windows DPAPI hardware-backed encryption.",
            ),
            (
                "library",
                "Curated modding & seamless packs",
                "Browse Modrinth and CurseForge with automated dependency resolution and update alerts. Full support for importing and exporting .mrpack, CurseForge, and MultiMC / Prism modpacks.",
            ),
            (
                "settings-download",
                "Adaptive multi-source download engine",
                "Combines Mojang, BMCLAPI, MCIM, and custom mirrors with real-time latency probing and automatic failover. Features dynamic concurrency throttling, streaming SHA-1 verification, and chunked resumable downloads.",
            ),
            (
                "crash",
                "Localized crash diagnostics",
                "When the game exits abnormally, Cairn analyzes game logs, crash reports, and JVM hs_err files locally to explain the root cause in plain language, exporting sanitized bundles with sensitive tokens masked.",
            ),
            (
                "extensions",
                "Secure, sandboxed extension platform",
                "Declarative YAML widgets and panels alongside JavaScript plugins running inside an isolated QuickJS-NG sandbox. Confirmed on demand, with a global <code>--no-plugins</code> safe mode.",
            ),
            (
                "settings-appearance",
                "Refined visuals & multilingual fidelity",
                "Light and dark themes, customizable accent hues, wallpaper with frosted depth, and smooth HiDPI scaling. Built-in support for Simplified Chinese, English, and Japanese.",
            ),
        ],

        # Measured
        "bench_h": "Verifiable Performance",
        "bench": [
            (
                "60",
                "ms",
                "Complete launch prep for NeoForge 1.21.1",
                "Parsing configurations, resolving version inheritance, verifying ~4,000 game files, selecting compatible Java, extracting natives, and building launch arguments. Median of 10 runs (reduced from 106 ms after stage-two optimization).",
            ),
            (
                "32",
                "ms",
                "Warm scan of a 300-mod pack",
                "Opening, unpacking, and parsing metadata and dependency graphs across 300 JAR files. Note: cold-disk first verification with complete SHA-1 hashing takes 412 ms.",
            ),
            (
                "≈14",
                "MiB",
                "Peak working set during launch prep",
                "Peak memory footprint of the command-line engine while orchestrating dependencies and files—featherweight and unobtrusive.",
            ),
            (
                "9.6",
                "MiB",
                "Standalone release executable size",
                "A fully featured <code>CairnLauncher.exe</code> release binary measures 10,046,464 bytes (~9.6 MiB); the command-line tool <code>cairn.exe</code> is ~5.2 MiB (5,473,792 bytes).",
            ),
        ],
        "bench_how_h": "Benchmark hardware and methodology",
        "bench_how": "Test rig: Intel Core i7-14700F (20 cores, 28 threads), 32 GB RAM, NVMe SSD, Windows 11 Pro for Workstations (Build 26200). Each benchmark is executed in a dedicated fresh process with process creation overhead included, under warm OS file cache conditions.",

        # Privacy
        "priv_h": "Local sovereignty: your data stays on your machine",
        "priv_sub": "Strictly aligned with our Privacy Policy (version 1.0, effective 2026-11-06) and 0.1.0 source code, adhering to total data ownership.",
        "priv": [
            (
                "Zero telemetry, analytics, ads, or silent tracking",
                "The launcher contains no tracking beacons, usage telemetry, remote crash uploaders, or ad networks. The developers do not collect or hold your personal data.",
            ),
            (
                "Clean portable storage by design",
                "All accounts, configurations, and instances reside by default in the adjacent <code>.cairn</code> folder (configurable via <code>CAIRN_HOME</code>). Deleting this folder leaves zero residue.",
            ),
            (
                "Direct connection to trusted endpoints only",
                "Logins, version manifests, and asset downloads connect straight to Microsoft, Mojang, Modrinth, CurseForge, or your configured mirrors, without any developer-operated middleman proxy.",
            ),
            (
                "Hardware-grade token encryption",
                "On Windows, sensitive tokens in <code>accounts.dat</code> are protected by Windows DPAPI hardware-backed encryption. All other settings remain human-readable JSON for straightforward inspection and backup.",
            ),
            (
                "No silent automatic updates",
                "The launcher never silently downloads or forces software updates in the background. Releases are published transparently on our website and GitHub, keeping update decisions entirely in your hands.",
            ),
        ],
        "callout_h": "Legal notice on accounts and game licenses",
        "callout": "An offline account is merely a local player name profile and neither constitutes nor replaces a genuine Minecraft game license. Under Chapter 3 of the Terms of Service: users residing outside mainland China must first authenticate through Microsoft's official flow with an account owning Minecraft Java Edition before creating offline profiles; users residing in mainland China are strongly urged to hold a valid license.",
        "read_privacy": "Read the Privacy Policy",
        "read_terms": "Read the Terms of Service",

        # Download
        "get_h": "Download portable release or build from source",
        "get_lede": "Natively supporting Windows 10 and newer. Cairn is strictly portable—no installer wizard required, and all application state remains cleanly encapsulated within the <code>.cairn</code> folder.",
        "get_dl": "Get Release on GitHub",
        "get_repo": "Browse GitHub Repository",
        "get_facts": [
            "Fully open source; source code hosted on GitHub. The GUI framework <code>cairn-ui</code> is dual-licensed under MIT or Apache-2.0.",
            "No silent background updates: subscribe to our website or GitHub Releases for new versions.",
            "Requirements for building from source: Windows 10 or newer, and Rust 1.91+ (2024 Edition).",
        ],
        "code_title": "Build from source",
        "code": [
            ("cargo run -p cairn-app", "Run the desktop launcher"),
            ("cargo build --release -p cairn-app", r"Build target\release\CairnLauncher.exe"),
            ("cargo build --release -p cairn-cli", r"Build target\release\cairn.exe"),
        ],
        "copy": "Copy command",
        "copied": "Copied to clipboard",
    },
}

# ---------------------------------------------------------------------------------------------- RustCraftMC Team

ORG = {
    "zh": {
        "lang_attr": "zh-CN",
        "title": "RustCraftMC Team — 致力于现代、原生与纯粹的 Minecraft 开源项目",
        "desc": "RustCraftMC Team 是一个专注于以现代系统级语言与原生架构重塑 Minecraft 工具链和基础设施的开源团队。代表项目：Cairn Launcher、RustCraft。",
        "skip": "跳到正文",
        "nav_label": "组织主导航",
        "nav": [("projects", "精选项目"), ("github", "GitHub 组织")],
        "switch": "English",
        "switch_attr": "en",
        "h1": "RustCraftMC <b>Team</b>",
        "lede": "以严谨的系统级工程实践与现代语言工具链，为 Minecraft 生态构建轻量、敏捷、可信赖的开源基础设施与工具。",
        "projects_h": "精选项目",
        "cairn_tag": "纯粹 · 优雅 · 灵动的现代 Minecraft 启动器",
        "cairn_body": "用 Rust 原生构建的单文件启动器。彻底摆脱 Chromium 容器与 JVM 运行时包袱，搭载自研 cairn-ui 图形库与硬件级 GPU 毛玻璃合成，兼具极速响应与呼吸般的现代质感。",
        "cairn_site": "访问启动器官网",
        "cairn_repo": "GitHub 仓库",
        "cairn_alt": "Cairn Launcher 启动器主界面展示",
        "rustcraft_tag": "RustCraft 探索项目",
        "rustcraft_body": "基于 Rust 语言重新探索与构建 Minecraft 生态核心体验的开拓性开源项目。欢迎前往官方站点了解更多架构细节与开发进展。",
        "rustcraft_hint": "访问 RustCraft 官网 ↗",
        "github_h": "开源与社区协作",
        "github_sub": "所有公开代码库均托管于 GitHub，遵循开放、透明的协作精神。欢迎查阅源码、参与讨论或提交贡献。",
        "github_hint": "github.com/RustCraftMC",
        "foot_links": [
            ("Cairn Launcher 官网", "cairnlauncher/"),
            ("用户协议", "cairnlauncher/terms/"),
            ("隐私政策", "cairnlauncher/privacy/"),
        ],
        "foot_gh": "GitHub 组织",
        "trademark": "Minecraft 是 Mojang Studios 和 Microsoft 的商标。RustCraftMC Team 是独立的开源团队，与 Mojang Studios 或 Microsoft 无关联。",
        "nf_title": "404",
        "nf_subtitle": "页面未找到",
        "nf_text": "抱歉，您访问的路径不存在。该页面可能已被移动、更名，或输入的链接有误。",
        "nf_home": "返回组织首页",
        "nf_cairn": "前往 Cairn Launcher 官网",
    },
    "en": {
        "lang_attr": "en",
        "title": "RustCraftMC Team — Modern, Native & Open-Source Minecraft Tools",
        "desc": "RustCraftMC Team is dedicated to crafting native, lightweight, and modern tools for the Minecraft ecosystem using systems programming. Featured projects: Cairn Launcher and RustCraft.",
        "skip": "Skip to content",
        "nav_label": "Main navigation",
        "nav": [("projects", "Projects"), ("github", "GitHub")],
        "switch": "中文",
        "switch_attr": "zh-CN",
        "h1": "RustCraftMC <b>Team</b>",
        "lede": "Engineering uncompromising, native tools and modern infrastructure for the Minecraft ecosystem with systems precision.",
        "projects_h": "Featured Projects",
        "cairn_tag": "Pure, elegant, and modern Minecraft launcher",
        "cairn_body": "A single-binary native launcher built with Rust. Free from Chromium shells and JVM overhead, driven by our bespoke cairn-ui graphics stack with hardware-accelerated frosted glass compositing.",
        "cairn_site": "Visit Launcher Site",
        "cairn_repo": "GitHub Repository",
        "cairn_alt": "Cairn Launcher application dashboard screenshot",
        "rustcraft_tag": "RustCraft Project",
        "rustcraft_body": "An exploratory reimagining of Minecraft core systems in Rust. Visit the dedicated website to explore the architecture and development roadmap.",
        "rustcraft_hint": "Visit RustCraft Website ↗",
        "github_h": "Open Source & Collaboration",
        "github_sub": "All our public repositories are hosted transparently on GitHub. Explore our source code, report issues, or contribute.",
        "github_hint": "github.com/RustCraftMC",
        "foot_links": [
            ("Cairn Launcher Home", "cairnlauncher/en/"),
            ("Terms of Service", "cairnlauncher/en/terms/"),
            ("Privacy Policy", "cairnlauncher/en/privacy/"),
        ],
        "foot_gh": "GitHub Organization",
        "trademark": "Minecraft is a trademark of Mojang Studios and Microsoft. RustCraftMC Team is an independent open-source team and is not affiliated with Mojang or Microsoft.",
        "nf_title": "404",
        "nf_subtitle": "Page Not Found",
        "nf_text": "The page you are looking for does not exist. It may have been moved, renamed, or the URL might be mistyped.",
        "nf_home": "Back to Team Home",
        "nf_cairn": "Visit Cairn Launcher",
    },
}
