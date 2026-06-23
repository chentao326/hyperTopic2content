# 各 Phase 完成检查清单

## Phase 2 (hv-analysis)

- [ ] DDGS 搜索 ≥ 3 个角度，每个 ≥ 8 条
- [ ] Playwright 抓取 ≥ 2 篇正文
- [ ] 纵向分析 ≥ 6000 字（含叙事故事线）
- [ ] 横向分析 ≥ 3000 字（≥ 3 个竞品深入对比）
- [ ] 用户口碑有真实来源引用（好话+坏话都要有）
- [ ] 横纵交汇产出新判断（不是前面内容的缩写）
- [ ] 三个未来剧本都有逻辑支撑
- [ ] 所有关键事实标注信息来源
- [ ] PDF 生成成功（无报错，排版正常）
- [ ] 搜不到的信息诚实标注了「暂缺」

## Phase 3 (khazix-writer)

- [ ] L1 硬性规则：禁用词 / 禁用标点（冒号→逗号）/ 结构套话 / 空泛工具名 全部清零
- [ ] L2 风格一致性：开头钩子 / 长短句交替 / 口语化 / 标点禁令二次确认
- [ ] L3 内容质量：观点有支撑 / 知识输出自然 / 有文化升维 / 有对立面同理心
- [ ] L4 活人感：温度感 / 独特性 / 姿态 / 心流
- [ ] 错别字扫描（如「绰绰有余」等成语）
- [ ] 核心论点无重复（同一句话不宜在文中出现两次以上）

## Phase 4 (web-video-presentation)

### 环境
- [ ] NODE_ENV ≠ production（已设为 development）
- [ ] npm install 成功（检查 node_modules/ 和 vite 可执行）
- [ ] dev server 启动成功（curl localhost:5173 返回 200）

### 脚本与组件
- [ ] script.md 口播稿符合 B 站风格 8 条原则
- [ ] outline.md 含信息池 + 素材清单 + step 估时
- [ ] 7-8 章 React 代码就绪（每章 narrations.ts + Component.tsx + Component.css）
- [ ] chapters.ts 注册了所有章节
- [ ] STORAGE_KEY 已 bump
- [ ] TypeScript 编译通过（npx tsc --noEmit）
- [ ] 简化版 HTML 可单独打开

### 音频
- [ ] narrations 格式为 string[]（不是 { text, durationMs }[]）
- [ ] TTS provider 已选（Mimo 优先 / edge-tts 备选）
- [ ] 音频 API key 安全存放（`~/.mimo_credentials` chmod 600，**不在命令行**）
- [ ] 音频文件存在 public/audio/<chapter>/<N>.wav（24kHz PCM16 mono）
- [ ] App.tsx audio src 后缀为 `.wav`（不是 `.mp3`）
- [ ] 手动模式下按 M 键切 audio 模式，验证 audio 播放

### 视频演示项目优化（关键经验）

- [ ] 居中 / 字号比例：每章 5 个 Block Entry 都垂直水平居中（不要偏上半）
- [ ] 中文字号 ≥ 数字 hero：避免"数字太大、中文太小"反客为主
- [ ] 每段加 detail 段：增加信息密度，context 写明
- [ ] 字号比例：中文 200 weight 大字 120-180px，数字 hero 100-160px，中文说明 36-48px
- [ ] 用 tsf 校验 0 错误
- [ ] 0 page error / 0 console error

## Phase 5 (beautiful-article)

### Plan (Phase 2)
- [ ] 决定文章类型（longform / full-report / essay / briefing 等）
- [ ] 决定主题（tufte / press / freddie / knuth / vignelli / shannon）
- [ ] 决定版式宽度（narrow / regular / wide / full）
- [ ] 决定配图模式（none / user-assets / placeholders / ai-generated）
- [ ] 决定封面（开 / 关，主视觉选 33 年时间线 / 五层堆叠 / 5 段对照 等）

### Checkpoint 1（必停）
- [ ] 5 项独立确认完成（每项独立 question）
- [ ] 信息保留比例明确（按文章类型选，longform=100% / full-report=80% / briefing=50%）

### First Spread (Phase 4)
- [ ] 封面（Cover.tsx）3:4 比例 + 主题风格 + 图文并茂
- [ ] Hero（标题 + 副标 + meta 3 项）
- [ ] Lead（导语 1-2 段）
- [ ] Summary（full-report 必备，TL;DR 4-5 行）
- [ ] Section 01（第一个 section，代表性视觉块）
- [ ] 所有 --ra-* token，无 hardcode
- [ ] tsc 0 错误 / 0 console error / 0 page error

### Checkpoint 2（必停）
- [ ] 验收通过
- [ ] 选定开发模式（A 单 Agent 顺序 / B 多 Agent 并行）

### Full Build (Phase 5)
- [ ] 18 个 section 文件全部存在（每节 1 个文件）
- [ ] 5 个 Raw 块文件（独立 raw-blocks/ 目录）
- [ ] Article.tsx 接入所有 18 个 section
- [ ] tsc 0 错误
- [ ] dev server 0 console error / 0 page error
- [ ] TOC 23 项点击跳转工作

### Final Review (Phase 6)
- [ ] Editorial：信息保留率 / 章节顺序 / 范围边界
- [ ] Visual：5 Raw 块可见 / 主题一致 / 0 红色系（如要求）
- [ ] Technical：tsc / build / 离线可开 / 0 远程图

### Checkpoint 3（必停）
- [ ] 验收通过
- [ ] 决定交付（HTML / HTML+PDF / 还要修）

### 交付
- [ ] npm run build 成功
- [ ] npm run html 复制 dist/index.html → article/article.html
- [ ] bash <skill_dir>/scripts/html-to-pdf.sh 生成 article/article.pdf
- [ ] cp 到 /Volumes/My SSD/文章/文章产出/<日期>_<话题>.{html,pdf}
- [ ] document.title 改为文章标题（不能是 "Beautiful Article"）
- [ ] 移除 index.html 的 Google Fonts link（让 freddie 主题 fallback 到 system serif）

## Phase 5 避坑

- [ ] `reacticle` `Summary` 用 `points: string[]` **不是 `children`**
- [ ] `Quote` 用 `who` / `source` **不是 `attribution` / `emphasis`**
- [ ] `Aside` 的 `tone` 只有 `note` / `principle` / `capability` / `warning` 合法
- [ ] `index.html` 引用 Google Fonts → 断网降级，**移除**让 freddie 主题 fallback
- [ ] article.html `document.title` 改文章标题
- [ ] `user` content 必须空字符串（否则一起念）
- [ ] Mimo voice 中文内容用 `冰糖` / `苏打` / `茉莉` / `白桦`，不是 `mimo_default` 或英文音色
- [ ] 风格 tag `(快读)` 加快节奏（audio.speed 不支持）

## Phase 6 (发布)

- [ ] 内容已摄入 Obsidian vault
- [ ] 飞书知识库已发布
- [ ] 知乎已发布

## Phase 4b (B2 MP4 视频，新增)

### Step A: 口播稿
- [ ] script.md 产出并同步到 script_full.txt
- [ ] outline.md 产出，包含信息池 + 素材清单 + step 估时
- [ ] 短视频 script_full.txt 120-220 字；完整版 300-600 字（B 站风格，禁用词清零）
- [ ] 开头有钩子，结尾有收尾，中间有数据

### Step B: TTS 试听
- [ ] 3 段试听音频都已生成（bingtang/soda/yunjian）
- [ ] 每段 ~10 秒，无截断
- [ ] AI 推荐附上

### Step C: 层面选择
- [ ] 层面 2 是否 → 已选择
- [ ] 层面 3 版本 → 已选择

### Step D: DESIGN.md
- [ ] 视觉 token 提取（层面 2=是时）或基础规则推断（否时）
- [ ] DESIGN.md 格式符合 HyperFrames 规范

### Step E: 正式 TTS + 字幕
- [ ] mimo 或 edge-tts 正式合成全程音频
- [ ] audio.mp3 可被 ffprobe 识别（MP3 / 128k 左右 / 时长正确）；如保留 WAV，才检查 24kHz PCM16 mono
- [ ] whisper 转字幕 JSON 词数 >50（正常 100-200 词）

### Step G: MP4 输出
- [ ] HyperFrames lint 0 error
- [ ] inspect 0 layout issue
- [ ] MP4 文件存在且格式正确（H.264 1920x1080 AAC）
- [ ] MP4 时长 = 音频时长 ± 0.5s
- [ ] 短视频版或完整版命名符合规范
