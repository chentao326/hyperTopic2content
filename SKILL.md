---
name: hyperTopic2content
description: |
  话题→内容全管线（含真 MP4 视频输出）。输入一个话题（产品/公司/概念/技术），自动跑通舆情扫描→横纵分析→公众号文章→视频生成（网页演示 + MP4 视频）→精修网页文章 的完整管道。
  触发词：研究一下XX、帮我做XX的完整分析、XX是什么来头出全套、帮我深度研究XX并出文章和视频、做视频、出 MP4、出短视频。
  快捷模式：只说"研究一下"默认跑横纵报告+公众号文章（不跑视频）。
  视频模式：说"出视频"或"出全套"跑 Phase 4（网页演示 + MP4 视频）。
  检查点模式 vs 自动推进：Phase 0 启动时询问。检查点模式每步产物落盘后暂停；自动推进一口气跑到底。
---

# hyperTopic2content — 话题→内容全管线（含 MP4 视频）

输入一个话题，自动编排多个 skill 跑通完整内容管线。相比 topic2content，**Phase 4 新增 B2 MP4 视频输出**（HyperFrames 真 MP4），同时保留 B1 网页演示。B1/B2 可各自单跑或并联。

## 核心原则

- **检查点模式 vs 自动推进**：Phase 0 启动时先问用户「检查点还是自动推进」。检查点模式每个产物落盘暂停等确认；自动推进一口气跑到底。用户随时在任意检查点说「自动推进」切换到自动模式。
- **检查点统一格式**：每个 ⏸ 处 → 「通过」继续 / 「改 XXX」重跑本步 / 「自动推进」后续全跳。
    - 「改 XXX 重跑本步」= 覆盖当前产物（同版本号），**后续所有步骤也必须重跑**（因为输入可能变了）。
    - 自动推进模式下遇到非致命错误（如 whisper 下载失败、npm install 卡住）：暂停并告知用户，不动手重试。
- **进度通知**：长时间步骤（TTS 合成 > 10s、MP4 渲染 > 60s）完成后必须通知用户产物路径和关键指标。
- **产物落盘再汇报**：不口头描述结果，文件真的写到了磁盘才算完成。
- **跳过条件明确**：用户说「只要报告」跳过文章和视频；说「出视频」跑 Phase 4；说「出全套」跑全部。
- **工作目录软链**：同 topic2content，所有项目在 `/Volumes/My SSD/code/content-pipeline/` 下用软链暴露到 `/Volumes/My SSD/文章/`。
- **B1 和 B2 独立可跑**：B1（网页演示）和 B2（MP4 视频）可单独触发，也可并联。

---

## 管道流程

```
用户输入话题
    │
    ├─ Phase 0: 模式识别
    │   判断用户意图 → 选择跑哪些 Phase
    │
    ├─ Phase 1: last30days-cn（舆情扫描，可选）
    │   触发：用户未指定具体研究对象 OR 说"先看看热点"
    │   产出：30天热议摘要
    │
    ├─ Phase 2: hv-analysis（横纵分析深度报告）【必跑】
    │   产出：1-3万字深度报告 + HTML + PDF
    │
    ├─ Phase 3: khazix-writer（公众号文章）【默认跑】
    │   产出：4000-8000字公众号长文
    │   输入：Phase 2 的报告
    │
    ├─ Phase 4: web-video-presentation（视频演示，可选）
    │   产出：React项目 + 7 章 93 步网页演示 + 合成音频
    │   触发："出全套" / "含视频" / "做成视频"
    │   输入：Phase 3 的文章 + Phase 2 的报告
    │
    ├─ Phase 5: beautiful-article（精修网页，可选）
    │   产出：单文件 HTML 网页文章 + PDF（断网可开）
    │   触发："出全套" / "精修成网页" / "做成可分享的网页文章"
    │   输入：Phase 2 的报告（也可基于 Phase 3 文章）
    │
    └─ Phase 6: 三平台发布（可选）
        产出：Obsidian vault + 飞书知识库 + 知乎
        触发：用户说"发布"或有发布习惯
```

---

## Phase 0: 模式识别

拿到用户输入后，先判断跑哪些 Phase。**同时询问检查点模式 or 自动推进**。

| 用户说法 | 跑哪些 | Phase 4 细节 |
|----------|--------|-------------|
| 「研究一下XX」 | Phase 2+3 | 不跑视频 |
| 「研究一下XX，出视频」 | Phase 2+3+4b | 只 B2 MP4 |
| 「研究一下XX，做演示」 | Phase 2+3+4a | 只 B1 网页演示 |
| 「研究一下XX，出全套」 | Phase 1→2→3→4a+4b→5 | B1 + B2 都跑 |
| 「研究一下XX，出 MP4 短视频」 | Phase 2+3+4b | B2，短视频模式 |
| 「研究一下XX，出完整视频」 | Phase 2+3+4b | B2，完整版模式 |
| 「XX 出全套，含精修」 | Phase 1→2→3→4a+4b→5 | B1 + B2 并联 |
| 「把这个报告做成视频」 | Phase 4b only | 用已有报告 |
| 「把这个报告/文章做成网页」 | Phase 5 only | 精修网页 |
| 「最近30天AI有什么热点」 | Phase 1 only | 舆情扫描 |
| 「发布到知乎/飞书」 | Phase 6 only | 发布 |

不确定时默认跑 Phase 2+3（不跑视频）。**Phase 0 结束时必须问「检查点模式还是自动推进？」**。

检查点模式对每个产物暂停等确认。自动推进模式后续所有 ⏸ 处跳过。

---

## Phase 1: 舆情扫描

**加载 skill**: `last30days-cn`

**执行**:
```bash
python <skill_dir>/scripts/last30days.py "<话题>" --quick --emit compact
```

**产出**: 直接展示摘要，不单独落盘文件。

**跳过条件**: 用户已指定明确的研究对象（如"研究即梦AI"），跳过；用户说"先看看热点"才跑。

---

## Phase 2: 横纵分析报告

**加载 skill**: `hv-analysis`

**信息收集**（按优先级）:

1. **DDGS 搜索**（最可靠）: 搜 3-4 个角度（纵向历史/横向竞品/用户口碑/战略背景），每轮 8-10 条
   ```bash
   cd ~/.hermes/hermes-agent && venv/bin/python3 /tmp/search_xxx.py
   ```
   脚本用 write_file 写入 /tmp，避免 shell 编码问题。

2. **Playwright 抓取正文**: 对 DDGS 搜到的关键 URL 抓取完整正文
   ```python
   # 模板见 hv-analysis skill
   # 注意：知乎/CSDN 可能被拦，用 DDGS body 摘要兜底
   # 36氪、头条、AI产品库、什么值得买 通常能抓到
   ```

3. **last30days-cn 终扫**（可选）: 报告写完后跑一次确认热度
   ```bash
   python <skill_dir>/scripts/last30days.py "<研究对象>" --quick --emit compact
   ```

**报告写作**: 按 hv-analysis 的纵向→横向→交汇三部分写，1-3万字。

**PDF 生成**（macOS）:
```bash
DYLD_LIBRARY_PATH=/opt/homebrew/lib \
  /Users/chentao/.hermes-web-ui/desktop-runtime/hermes/0.16.0/mac-arm64/python/bin/python3 \
  <skill_dir>/scripts/md_to_pdf.py input.md output.pdf --title "标题" --author "横纵分析法"
```

**自检**: 跑 hv-analysis 的质检清单。

**产出**: `<日期>_<话题>_横纵分析报告_v<版本>.md` + `.html` + `.pdf`

---

## Phase 3: 公众号文章

**加载 skill**: `khazix-writer`

**输入**: Phase 2 的横纵分析报告

**写作**: 按卡兹克风格写 4000-8000 字。B站风格口播，禁止冒号/破折号/双引号。核心论点要有具体数据支撑。

**自检**: 跑 khazix-writer 的四层自检体系（L1 硬性规则→L2 风格一致性→L3 内容质量→L4 活人感）。重点关注：
- 冒号「：」改逗号
- 禁用词「说白了/本质上/换句话说/值得注意的是」全部清零
- 错别字扫描（如「绰绰有余」不能写成「绑绑有余」）

**产出**: `<日期>_<话题>_公众号文章_v<版本>.md`

**跳过条件**: 用户明确说"只要报告不要文章"。

---

## Phase 4: 视频生成（★核心改造）

Phase 4 拆为 Step A→G 七步，**执行顺序 A→B→F→C→D→E→G**（F 必须在 C 之前，确保 B1 CSS 已存在）。B1（网页演示）保留，B2（HyperFrames MP4）新增。

### ⚠️ 环境预检（Step B 前必做）

```bash
# 检查 Node.js / FFmpeg / Python / whisper / HyperFrames
node --version      # 需 >= 22
ffmpeg -version     # 任意即可
python3 --version   # 需 >= 3.9
which whisper       # 需在 PATH
ls ~/.cache/whisper/small.pt   # 461MB 需存在
npx hyperframes --version 2>/dev/null | head -1
# 全部检查后才能进 Step B
```

### Step A: 口播稿统一生成（产出三份）

从 Phase 3 公众号文章自动提炼口播稿，产出三份：

**格式 1: script.md**（B1 网页演示用，按章节拆分）
**格式 2: script_full.txt**（B2 TTS 用，完整拼接纯文本）
**格式 3: outline.md**（B1 网页演示用，章节开发规划。内容：信息池 + 素材清单 + 每步估时）

script_full.txt 规则：短视频 120-220 字，完整版 300-600 字，开头钩子 + 2-3 核心论点 + 结尾收尾。B 站风格（短句、口语、禁用冒号双引号破折号）。

LLM prompt 模板见 `references/script-extraction-prompt.md`。

**⏸ 检查点**: 三份文件落盘。用户回复「通过」/「改 XX」/「自动推进」。

### Step B: TTS 试听确认

⚠️ **配音前先试听，不是直接合成全程**。用 script_full.txt 前 2-3 句合成 3 段 ~10 秒试听：

| 试听 | 音色 | 提供方 | 风格 |
|-----|-----|-------|------|
| 1 | 冰糖（女声） | mimo-v2.5-tts | 专业稳重 |
| 2 | 苏打（男声） | mimo-v2.5-tts | 成熟干练 |
| 3 | zh-CN-YunjianNeural（男声） | edge-tts | 新闻播报（免费 fallback） |

**AI 推荐**：基于 Phase 2 报告类型（战略→冰糖；技术→苏打；故事→冰糖）。

产物：`tts-samples/sample_bingtang.mp3`, `sample_soda.mp3`, `sample_yunjian.mp3`

**⏸ 检查点**: 3 段试听 + AI 推荐。用户选音色。

### Phase 4a Step F: B1 网页演示

保留 topic2content/web-video-presentation 全部流程。输入 Step A 的 script.md + outline.md。同原 topic2content Phase 4 全部内容（环境检查、React 组件、93 段音频、build）。

**⏸ 检查点**: 网页演示项目落盘。

### Step C: 层面选择

B1 已完成，视频动手前选层面 2 和 3：

```
层面 2: 视觉一致
  是否从 B1 网页演示的 CSS 提取视觉 token 到 DESIGN.md？
  ○ 是（B1 已跑完，网页和视频用同一套设计语言）
  ○ 否（用 Phase 2 报告类型推断基础视觉）
  AI 推荐: B1 已完成 → "是"

层面 3: 章节复用
  MP4 视频场景结构：
  ○ 短视频版: 取 script.md 前 2-3 章、30-60 秒（适合 B 站/视频号引流）
  ○ 完整版: 全部章节按 scene 拆分、默认 90-180 秒（适合深度展示；用户明确要长视频时扩展到 5-15 分钟）
  ○ 全都要:  短视频 + 完整版都出
  AI 推荐: 报告>8000字→完整版 / <8000字→短视频版 / 发视频号→短视频
```

**⏸ 检查点**: 用户选择层面 2 和 3。可回「都用 AI 推荐」跳过。

### Step D: DESIGN.md 生成

若层面 2 选「是」：读 B1 网页的 CSS/App.tsx（路径：`presentation/src/App.css` 或 `src/index.css` 或 `tailwind.config.js`）→ 提取主色/辅色/字体/圆角 → 生成 DESIGN.md。若选「否」：用基础规则表。规则见 `references/design-inference-rules.md`。

**⏸ 检查点**: DESIGN.md 落盘。用户确认或调整。

### Step E: B2 TTS + whisper + 字幕

用 Step B 确认的音色，正式合成 script_full.txt 全程音频。详细 7 步流程见 `references/phase4b-pipeline.md`。简要：

  1. TTS 出 WAV → ffmpeg 转 MP3。⚠️ 预计耗时 10-30 秒，完成后通知用户
  2. whisper small --language zh --word_timestamps True → JSON。⚠️ 预计耗时 30-60 秒
  3. whisper_to_transcript.py 转 HyperFrames 格式 → transcript.json

**⏸ 检查点**: audio.mp3 + transcript.json 落盘。

### Phase 4b Step G: B2 MP4 输出

执行 text-to-video-pipeline Step 4-7。按 Step C 层面 3 选项处理：

- 短视频版：取 script.md 前 2-3 章的 scene，30-60s
- 完整版：全部章节按 scene 拆分，默认 90-180s；用户明确要长视频时扩展到 5-15min
- 全都要：分别跑两次渲染

HyperFrames HTML 合成读 Step D 的 DESIGN.md 作为视觉基础。参考模板：`references/example-index.html`。

⚠️ 渲染预计耗时：短视频 60-90s，完整版 3-5min。使用 background + notify_on_complete 通知用户。

**产物命名规范**（对齐产出版本管理）：
- 短视频：`<YYYYMMDD>_<话题>_MP4视频_<版本>_social.mp4`
- 完整版：`<YYYYMMDD>_<话题>_MP4视频_<版本>_full.mp4`

**⏸ 检查点**: MP4 文件落盘。

---

## Phase 5: 精修网页（可选）

**优先加载 skill**: `beautiful-article`（不存在时走现成网页文章 skill 降级路线）

**输入**: Phase 2 的报告（也可基于 Phase 3 的公众号文章）

**流程**:
1. 先检查 `beautiful-article` 是否存在：
   ```bash
   find ~/.hermes/skills ~/.codex/skills ~/.agents/skills -path '*/beautiful-article/SKILL.md' -print -quit
   ```
2. 若存在，按 beautiful-article 的 Phase 0→8 走，**严格按它的 Checkpoint 1/2/3 流程**（必停 + 必问 5 件事）。
3. 若不存在，不允许在中途直接失败；改用当前可用的网页文章现成能力（优先 `web-design-engineer` 或 `frontend-design` skill）生成断网可开的单文件 HTML，再用 Chrome headless 导出 PDF。该降级路线必须保留 Phase 5 的三次检查点和同样的交付命名。

**关键经验**（详见 beautiful-article SKILL.md）：
- **Checkpoint 1** 必问 5 件事：文章类型（含信息保留比例）/ 主题 / 版式宽度 / 配图模式 / 封面
- **First Spread**（封面 + Hero + Lead + 第一个 Section + 一个代表性视觉块）由主 Agent 兜底做（无需开 SubAgent，节省时间），Reviewer 自检后进 Checkpoint 2
- **Checkpoint 2** 必问 2 件事：验收结论 / 后续开发模式（A 单 Agent / B 多 Agent 并行）
- **Full Build** 推荐 **B 多 Agent 并行**（19 节分给 5 个 subagent 同步写）
- **Final Review** 主 Agent 兜底（不开 SubAgent 节省时间），自检后进 Checkpoint 3
- **Checkpoint 3** 必问 1 件事：交付决策（HTML / HTML+PDF / 还要修）

**主题推荐**（根据 Phase 2 报告类型）：
- 产业战略 / 公司研究 → **freddie**（暖白+明黄，无红色） 或 **press**（衬线出版物气质）
- 学术 / 论文风 → **knuth**
- 极致克制 / 数据密集 → **tufte**
- 中性系统文档 → **vignelli**

**配图**: 默认 `none`（0 外部图片，用 CSS+SVG Raw 块承担可视化），与视频演示项目一致

**5 个 Raw 块参考**（用于研究报告 / 产业分析）：
- 33 年时间线（8 节点 SVG）
- 5 层堆叠条（5 段不同灰度横条）
- 100-cell 网格（92/100 高亮）
- 能源层三选项对比
- 双时间线股价叠加

**避坑**:
- `reacticle` d.ts 中 `Summary` 接受 `points: string[]` **不是 `children`**
- `Quote` 接受 `who` / `source` **不是 `attribution` / `emphasis`**
- `Aside` 的 `tone` 只有合法值（`note` / `principle` / `capability` / `warning`），不能传 `"scope"`
- index.html 引用 Google Fonts → 断网时降级，**移除**让 freddie 主题 fallback 到 system serif
- article.html 改 `document.title` 为文章标题（默认 "Beautiful Article" 太通用）

**产出**: 
- `<工作区>/article/article.html`（2 MB 单文件 CSS+JS 内联，断网可开）
- `<工作区>/article/article.pdf`（2.5 MB A4 PDF, Chrome headless 渲染）
- 复制到 `文章产出/<日期>_<话题>.html` + `.pdf`

---

## Phase 6: 三平台发布（可选）

按固定流程：
1. 摄入 Obsidian vault (`/Users/chentao/Documents/Obsidian Vault/`)
2. 发布飞书知识库（space_id: 7427385554725142531）
3. 发布知乎文章

**触发条件**: 用户说"发布"或有发布到知乎/飞书的习惯。

---

## ⚠️ 音频合成决策

已整合到 Phase 4 Step B（TTS 试听确认）和 Step E（正式合成）。TTS 选项：mimo-v2.5-tts（推荐）/ Qwen3-TTS / edge-tts（免费 fallback）。详见 Phase 4 内对应步骤。

---

## 工作目录与软链（重要！）

所有项目都在 `/Volumes/My SSD/code/content-pipeline/` 下用**软链**暴露到 `/Volumes/My SSD/文章/`：

```bash
# 1. 在 /Volumes/My SSD/文章/ 下建软链
ln -s "/Volumes/My SSD/code/content-pipeline/20260618_xxx_横纵分析_v1" "/Volumes/My SSD/文章/20260618_xxx_横纵分析_v1"
ln -s "/Volumes/My SSD/code/content-pipeline/20260618_xxx_视频演示_v1" "/Volumes/My SSD/文章/20260618_xxx_视频演示_v1"

# 2. Phase 5 工作区直接建在 /Volumes/My SSD/文章/ 下
mkdir -p "/Volumes/My SSD/文章/2026-06-18-xxx-beautiful"
cd "/Volumes/My SSD/文章/2026-06-18-xxx-beautiful"
# beautiful-article 存在时才执行：
bash <beautiful_article_skill_dir>/scripts/scaffold.sh . --theme=freddie
# beautiful-article 不存在时，改用 web-design-engineer / frontend-design 生成单文件 HTML + PDF
```

**为什么软链**:
- 0 冗余（不复制 node_modules）
- 原项目修改自动同步
- Finder 双击软链看完整项目

**整理本文件夹的规则**:
- 用 native 名字软链（如 `20260618_xxx_视频演示_v1`）不要简化（如 `nvidia-5layer-cake`），避免循环软链
- 删除重复软链（同一项目只一个）
- 最终交付物（`文章产出/` 和 `视频产出/`）用 `cp -R` 真复制，不软链

---

## ⚠️ 已知坑（已验证，记录在此避免重复）

### 信息收集
- ❌ delegate_task 子Agent 无法联网搜索（没有 terminal/curl）
- ✅ 直接用 DDGS + Playwright 搜
- ❌ 知乎/CSDN 有反爬，curl 只能拿元数据
- ✅ Playwright headless Chromium 能绕过大部分，但知乎仍可能 403

### npm
- ❌ macOS 全局 `NODE_ENV=production` 导致 npm install 跳过 devDependencies
- ✅ 所有 npm 命令前加 `NODE_ENV=development`
- ❌ npm install -g mmx-cli 报 EACCES
- ✅ `npm config set prefix ~/.npm-global` + `export PATH=$HOME/.npm-global/bin:$PATH`

### WeasyPrint
- ❌ 系统 Python 3.9 的 weasyprint v66 不兼容 macOS
- ✅ 用 Hermes 运行时 Python 3.12 + `DYLD_LIBRARY_PATH=/opt/homebrew/lib`

### 公众号文章
- ❌ 冒号「：」是 AI 味指纹
- ✅ 全部改用逗号
- ❌ 「绑绑有余」不是标准写法
- ✅ 标准成语「绰绰有余」

### 视频演示 · audio
- ❌ 用 { text, durationMs } 格式
- ✅ 全部用 `string[]`（纯字符串数组）
- ❌ `mmx` 默认 base URL 是 MiniMax 官方
- ✅ 第三方 base URL 需 `mmx config set --key base_url --value <url>`
- ❌ `mmx auth login` 把 API key 暴露在命令行
- ✅ 用户自己 export 后跑

### TTS · Mimo
- ❌ `messages: [{role: "user", content: text}]`
- ✅ 必须 `messages: [{user, ""}, {assistant, text}]` — user content 会被念
- ❌ 把英文音色用于中文内容（如 `voice: "Chloe"` 配中文文本）
- ✅ 中文内容用 `voice: "冰糖"`（女）/`"茉莉"`（女）/`"苏打"`（男）/`"白桦"`（男）；英文内容才用 Chloe/Mia/Milo/Dean
- ❌ 混淆 mimo LLM 和 mimo TTS 的 key
- ✅ TTS key 存 `~/.mimo_credentials`（权限 600），与 Hermes .env 里的 mimo LLM key 是不同产品线
- ❌ Mimo 输出变长 (9.6s 念 50 字)
- ✅ 加 `(快读)` style tag 在 assistant content 前面，模型进入"快读模式"
- ❌ `audio.speed` 参数
- ✅ Mimo API 不支持 speed 参数（仅 style tag 控制节奏）
- ℹ️ `voice: "mimo_default"` 官方文档标注可用（按部署集群自动选冰糖或 Mia），但建议显式指定音色名更可靠

### 视频演示 · React 项目
- ❌ 播放模式 manual 模式不播 audio
- ✅ useAudioPlayer 设计：按 M 切到 audio 模式（播 audio 但手动翻）
- ❌ autoStarted 默认 false 不播
- ✅ 按 Space 触发

### beautiful-article · reacticle d.ts
- ❌ `<Summary><p>...</p></Summary>` (children)
- ✅ `<Summary points={["...", "..."]} />` (points: string[])
- ❌ `<Quote attribution="..." emphasis="...">`
- ✅ `<Quote who="..." source="..." />` (无 emphasis prop)
- ❌ `<Aside tone="scope" label="...">`
- ✅ `Aside` 的 tone 只有 `note` / `principle` / `capability` / `warning` 合法
- ❌ `index.html` 引用 Google Fonts (`<link href="https://fonts...">`)
- ✅ 移除链接（freddie 主题 fallback 到 system serif，断网可开）
- ❌ 默认 `<title>Beautiful Article</title>`
- ✅ 改为文章标题（如 `黄仁勋的「五层蛋糕」 · 英伟达 33 年的 AI 帝国路线图`）

### beautiful-article · 主题
- ❌ 用户要求避免红色选 press（氧化血红主色也是红色系）
- ✅ freddie（accent 是 `#241c15` 深棕近黑，**不是红色**）
- ❌ 调"亮色"→ 改 `--ra-color-accent`
- ✅ freddie 主题用 `--mc-yellow: #ffe01b`（明黄）作高亮，accent 是深棕

### 文件系统
- ❌ `/Volumes/My SSD/文章/` 路径含空格
- ✅ 所有命令必须双引号包围
- ❌ scaffold 启动工作区时 `source/` 已存在
- ✅ 移动 source 到 /tmp → 重 scaffold → 把 source 移回
- ❌ 软链目标名重名
- ✅ 软链时 mv 失败 → 删旧链 → 建新链

---

## 产出版本管理

每次产出的所有文件统一放在一个按规范命名的大文件夹中，便于检索和归档。

### 命名规范

**大文件夹**:
```
<YYYYMMDD>_<话题>_<类型>_v<版本>
```

**内部文件**:
```
<YYYYMMDD>_<话题>_<类型>_<产物种类>_v<版本>.<扩展名>
```

### 字段说明

| 字段 | 示例 | 规则 |
|------|------|------|
| YYYYMMDD | 20260616 | 创建日期，8位数字 |
| 话题 | jimeng-ai | 话题关键词，小写+连字符，英文/拼音 |
| 类型 | 横纵分析 | 中文，大文件夹用核心分析类型；文件用产物种类 |
| 产物种类 | 横纵分析报告 / 公众号文章 / 视频演示 / 音频 | 这个产物是什么 |
| 版本 | v1 / v2 | 从 v1 开始，修改后递增 |
| 扩展名 | .md / .pdf / .html / .wav | 按实际格式 |

### 示例

以「即梦AI」话题为例，创建日期 2026-06-16，版本 v1：

```
content-pipeline/
└── 20260616_jimeng-ai_横纵分析_v1/
    ├── 20260616_jimeng-ai_横纵分析报告_v1.md
    ├── 20260616_jimeng-ai_横纵分析报告_v1.html
    ├── 20260616_jimeng-ai_横纵分析报告_v1.pdf
    └── 20260616_jimeng-ai_公众号文章_v1.md
```

视频演示项目作为子文件夹：
```
20260616_jimeng-ai_视频演示_v1/
├── script.md
├── outline.md
├── article.md
├── presentation/
│   ├── public/audio/...
│   ├── package.json
│   └── ...
```

### 版本递增规则

- 初稿: v1
- 审核修改后: v2, v3 ...
- 每次存新版本时，旧版文件保留在同一个大文件夹内，不删除

### 工作目录

所有内容管线产出统一存放在:
```
/Volumes/My SSD/code/content-pipeline/
```

启动前先确认该目录存在，不存在则创建。移动硬盘未挂载时回退到:
```
/Users/chentao/code/content-pipeline/
```

### 软链到 /Volumes/My SSD/文章/

每个项目完成后建软链，便于 Finder 浏览 + 跨项目引用：
```bash
ln -s "/Volumes/My SSD/code/content-pipeline/<项目名>" "/Volumes/My SSD/文章/<项目名>"
```

用 native 名字（与原项目一致），不用简化名（避免循环软链）。**最终定稿后**，把 `presentation/dist/` 复制到 `视频产出/`，把 `article.md` 复制到 `文章产出/`（**真复制不软链**）。

---

## 快捷参考：Phase 间状态传递

执行顺序: A→B→F→C→D→E→G

| From | To | 传递内容 |
|------|----|---------|
| Phase 2 | Phase 3 | 横纵分析报告 .md |
| Phase 3 | Phase 4 Step A | 公众号文章 .md |
| Phase 4 Step A | Step F (B1) | script.md + outline.md |
| Phase 4 Step A | Step E (B2 TTS) | script_full.txt |
| Phase 4 Step B | Step E | 确认的音色名 |
| Step F (B1) | Step C | B1 网页演示项目路径 + CSS 文件 |
| Step C | Step D | 层面 2 选择（是否从 B1 CSS 提取） |
| Step C | Step G | 层面 3 选择（短视频/完整版/全都要） |
| Step D | Step G | DESIGN.md |
| Step E | Step G | audio.mp3 + transcript.json |
| Phase 4b | Phase 5 | MP4 文件路径 |
| Phase 5 | Phase 6 | 精修 HTML/PDF 路径 |

## 版本

v2.1 — 2026-06-23 Codex 审查修复：补 Phase 5 缺失 skill 的预检与降级路线；修正 Phase 4b 工作目录和脚本路径；Step A prompt 明确产出 outline.md；统一 TTS context、中文音色、短视频时长和 MP3 验收口径。

v2.0 — 重大改造。基于 text-to-video-pipeline 和 topic2content v1.2 合并。2026-06-23 通过 Claude Code 审查（agent-reviewer），4 个致命缺陷和 6 个改进点全部修复：时序死锁已解（A→B→F→C→D→E→G）、outline.md 已补、外部依赖已内化、TTS 音色已统一、环境预检已加、MP4 命名已对齐、检查点重跑已定义、进度通知已加。

新增：
- Phase 4 拆为 Step A→G 七步（B1 网页演示保留，B2 MP4 视频新增）
- B2 基于 HyperFrames 真 MP4 输出（1920x1080 H.264 AAC）
- 检查点模式 vs 自动推进双模式
- TTS 试听确认机制（3 音色 × 10 秒试听 → 用户选）
- 层面 2（视觉一致）+ 层面 3（章节复用）选择 + AI 推荐
- MP4 三选项（短视频版 30-60s / 完整版默认 90-180s / 全都要）
- DESIGN.md 从 B1 网页 CSS 自动提取
- 口播稿统一生成（script.md + script_full.txt + outline.md 三格式）
