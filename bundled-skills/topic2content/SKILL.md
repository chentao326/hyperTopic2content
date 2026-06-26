---
name: topic2content
description: |
  话题→内容全管线。输入一个话题（产品/公司/概念/技术），自动跑通舆情扫描→横纵分析→公众号文章→视频演示→精修网页文章 的完整管道，产出一站式内容五件套（横纵报告 + 公众号长文 + 视频演示 + 精修网页 + 精修 PDF）。
  触发词：研究一下XX、帮我做XX的完整分析、XX是什么来头出全套、帮我深度研究XX并出文章和视频、帮我精修成网页文章。
  快捷模式：只说"研究一下"默认跑横纵报告+公众号文章+视频演示。
  完整模式：说"出全套"或"含视频"时跑全部五个阶段；说"还要精修网页"再加 beautiful-article 阶段。
---

# Topic2Content — 话题→内容全管线

输入一个话题，自动编排多个 skill 跑通完整内容管线，产出五件套。

## 核心原则

- **全程自动推进**：Phase 之间不暂停等确认（用户已明确授权），一口气跑到底。
- **每个 Phase 完成后先过自检再进下一阶段**：按子 skill 的质检清单逐项核查，不达标就修。
- **产物落盘再汇报**：不口头描述结果，文件真的写到了磁盘才算完成。
- **跳过条件明确**：用户说「只要报告」就跳过文章和视频；说「出全套」就跑全部。
- **工作目录软链到文章根目录**：所有项目都在 `/Volumes/My SSD/code/content-pipeline/` 下用软链暴露到 `/Volumes/My SSD/文章/`，便于 Finder 浏览和定稿归档。
- **定稿前不删改**：每个阶段产物落盘后保留，不互相覆盖；后续阶段读取最新版本即可。
- **必停 Checkpoint 在每个 skill 内部**：不自作主张跳过 sub-skill 的 Checkpoint（beautiful-article 强制 3 个 Checkpoint、video-presentation 强制 1 个 Checkpoint）。

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

拿到用户输入后，先判断跑哪些 Phase：

| 用户说法 | 跑哪些 |
|----------|--------|
| 「研究一下XX」 | Phase 2 + 3（默认：报告 + 文章） |
| 「出全套」「完整研究」「含视频」 | Phase 1→2→3→4（全跑到视频） |
| 「研究一下，不要文章」 | Phase 2 only |
| 「把这个报告做成视频」 | Phase 4 only（用已有报告） |
| 「把这个报告/文章做成精修网页」 | Phase 5 only（用已有产物） |
| 「出全套 + 网页精修」 | Phase 1→2→3→4→5（5 阶段） |
| 「最近30天AI有什么热点」 | Phase 1 only |
| 「发布到知乎/飞书」 | Phase 6 only |

不确定时默认跑 Phase 2 + 3 + 4（含视频演示）。

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

## Phase 4: 视频演示

**加载 skill**: `web-video-presentation`

**输入**: Phase 3 的文章 + Phase 2 的报告

**流程**: 按 web-video-presentation 的 Phase 1→2→3 走

**环境检查**（开始前必做）:
```bash
# 1. 检查 NODE_ENV
[ "$NODE_ENV" = "production" ] && echo "WARNING: NODE_ENV=production, need development"
# 2. 检查 playwright
python3 -c "from playwright.async_api import async_playwright; print('OK')" 2>/dev/null || pip install playwright --break-system-packages
```

**产出**: 
- `script.md`（口播稿）
- `outline.md`（开发计划）
- `<日期>_<话题>_视频演示_v<版本>/`（文件夹，含 React 代码 + standalone HTML + 音频）
- `public/audio/<chapter>/<N>.wav` (24kHz PCM16 mono)

**TTS 音频合成**（关键 — 见下"音频合成决策"）:
- **推荐**: Mimo TTS (mimo-v2.5-tts, 中文 voice="冰糖"/"茉莉"/"苏打"/"白桦", API key 存 `~/.mimo_credentials` 权限 600)
- 备选 1: Qwen3-TTS via DashScope（中文质量顶级，免费额度，详见下方决策表）
- 备选 2: edge-tts（微软免费，无需 key，`pip install edge-tts`）
- 备选 3: MiniMax mmx-cli（需要 mmx 装 + `mmx auth login --api-key`，配置第三方 base_url 需 `mmx config set base_url`）
- 备选 4: OpenAI TTS（需要 OPENAI_API_KEY + OPENAI_BASE_URL）

mimo 预置音色按语言分组（中文≠英文，不能用错）：
| 中文音色 | 性别 | 英文音色 | 性别 |
|---------|------|---------|------|
| 冰糖 | 女 | Mia | 女 |
| 茉莉 | 女 | Chloe | 女 |
| 苏打 | 男 | Milo | 男 |
| 白桦 | 男 | Dean | 男 |

**⚠️ 预计耗时较长**：完整跑完约 20-40 分钟（19 节 React 组件 + 5 subagent 并行 + 93 段音频合成 + build），告知用户。

---

## Phase 5: 精修网页（可选）

**加载 skill**: `beautiful-article`

**输入**: Phase 2 的报告（也可基于 Phase 3 的公众号文章）

**流程**: 按 beautiful-article 的 Phase 0→8 走，**严格按它的 Checkpoint 1/2/3 流程**（必停 + 必问 5 件事）。

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

Phase 4 视频演示需要 93 段 TTS 音频（每章 5-30 段）。**环境约束：当前 Mac 无 GPU（cuda: False），本地推理 1.7B 模型不现实 — 必须走 API 方案**。

### 首选：Qwen3-TTS via DashScope API（推荐）

**为什么**:
- 阿里云 Qwen 团队开源（Apache 2.0），中文质量评测超过 MiniMax 和 ElevenLabs
- API 调用，不需要本地 GPU（DashScope 阿里云百炼平台）
- 新用户有免费额度
- 支持预置音色（Cherry/Lucy/Vivian 等 10+ 中文音色）
- 支持指令控制语气情绪（`instructions="语速快，活泼热情"`）
- 也支持音色克隆和音色设计（高级场景）
- OpenAI 兼容流式接口，合成 93 段约 1-2 分钟

**获取 API Key**:
去阿里云百炼平台注册：https://help.aliyun.com/zh/model-studio/get-api-key

**环境变量**:
```bash
export DASHSCOPE_API_KEY=***
pip install dashscope soundfile
```

**Python 调用**:
```python
import os
import dashscope
from dashscope.audio.qwen_tts_realtime import *

dashscope.api_key = os.environ['DASHSCOPE_API_KEY']

class MyCallback(QwenTtsRealtimeCallback):
    def __init__(self):
        super().__init__()
        self.file = open('output.pcm', 'wb')
    def on_event(self, response):
        if response['type'] == 'response.audio.delta':
            import base64
            self.file.write(base64.b64decode(response['delta']))
    def on_close(self, code, msg):
        self.file.close()

callback = MyCallback()
tts = QwenTtsRealtime(
    model='qwen3-tts-flash-realtime',
    callback=callback,
    url='wss://dashscope.aliyuncs.com/api-ws/v1/realtime'
)
tts.connect()
tts.update_session(
    voice='Cherry',  # 推荐中文女声：Cherry（温暖）/Lucy（自然）/Vivian（明亮）
    response_format='pcm_24000hz_mono_16bit',
    mode='server_commit'
)
tts.append_text('今天天气真不错。')
tts.finish()
callback.wait_for_finished()
```

合成后 ffmpeg 转 wav：
```bash
ffmpeg -f s16le -ar 24000 -ac 1 -i output.pcm output.wav
```

**预置音色推荐（中文视频配音）**:
| 音色 | 风格 | 推荐场景 |
|------|------|----------|
| Cherry | 温暖甜美女声 | 通用知识类视频 |
| Lucy | 自然亲切女声 | 讲故事、科普 |
| Vivian | 明亮略带锐气女声 | 产品介绍、动态节奏快 |
| Serena | 温柔知性女声 | 深度分析、正式内容 |
| Uncle_Fu | 低沉醇厚男声 | 严肃报告、深度解说 |
| Dylan | 京腔少年男声 | 接地气、轻松话题 |

**指令控制（可选）**:
```python
tts.update_session(
    voice='Cherry',
    response_format='pcm_24000hz_mono_16bit',
    instructions='语速较快，语气活泼热情，适合做产品介绍。',
    mode='server_commit'
)
```

**注意**:
- DashScope API 是 WebSocket 实时接口，每次连接合成一段文字
- 如果合成长文本，可以用 `append_text` 流式发送，最后 `finish()`
- 免费额度通常够跑一个完整视频（93 段）

### 备选 1：Mimo TTS（`mimo-v2.5-tts`）

需要 MIMO_API_KEY（从 https://api.xiaomimimo.com 获取）。中文质量稳定，支持情绪标签和唱歌。

**调用方式（OpenAI 兼容）**:
```python
from openai import OpenAI
client = OpenAI(
    api_key="<MIMO_API_KEY>",
    base_url="https://api.xiaomimimo.com/v1"
)
completion = client.chat.completions.create(
    model="mimo-v2.5-tts",
    messages=[
        {"role": "user", "content": ""},  # ⚠️ 必须空字符串!
        {"role": "assistant", "content": text},
    ],
    audio={"format": "wav", "voice": "冰糖"},
)
```

**⚠️ 三大坑（已踩）**:
1. **API 必须含 assistant role**：纯 `user` 会报 400
2. **user content 不能放文本**：会一起念。**必须 `content: ""`（空字符串）**
3. **voice 名是 "冰糖"/"Chloe"** 不是 "mimo_default"

### 备选 2：edge-tts（完全免费，零 API key）

```bash
edge-tts --voice zh-CN-XiaoxiaoNeural --text "你好" --write-media out.mp3
```

适合快速原型。中文女声 `zh-CN-XiaoxiaoNeural` 默认。**不能商用**。

### 备选 3：MiniMax mmx-cli

需要 MiniMax API key + 配置 base_url。中文质量好但部署稍麻烦。

### 备选 4：OpenAI TTS

中文用 alloy/onyx/nova 等，不如前面专门的中文模型自然。

### 存哪里

- 视频演示项目：`presentation/public/audio/<chapter>/<N>.wav`（24kHz PCM16 mono）
- 浏览器 audio src：`audio/<chapter>/<N>.wav`（Vite 自动从 public/ 复制到 build/）
- 修改 `App.tsx` 的 audio src 后缀从 `.mp3` → `.wav`（HTML5 audio 优先用 wav 因为 PCM16 是原生格式）

---

## 工作目录与软链（重要！）

所有项目都在 `/Volumes/My SSD/code/content-pipeline/` 下用**软链**暴露到 `/Volumes/My SSD/文章/`：

```bash
# 1. 在 /Volumes/My SSD/文章/ 下建软链
ln -s "/Volumes/My SSD/code/content-pipeline/20260618_xxx_横纵分析_v1" "/Volumes/My SSD/文章/20260618_xxx_横纵分析_v1"
ln -s "/Volumes/My SSD/code/content-pipeline/20260618_xxx_视频演示_v1" "/Volumes/My SSD/文章/20260618_xxx_视频演示_v1"

# 2. beautiful-article 工作区直接建在 /Volumes/My SSD/文章/ 下
mkdir -p "/Volumes/My SSD/文章/2026-06-18-xxx-beautiful"
cd "/Volumes/My SSD/文章/2026-06-18-xxx-beautiful"
bash <skill_dir>/scripts/scaffold.sh . --theme=freddie
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

| From | To | 传递内容 |
|------|----|---------|
| Phase 2 | Phase 3 | 横纵分析报告 .md 文件路径 |
| Phase 2+3 | Phase 4 | 公众号文章 .md + 横纵报告 .md 双路径 |
| Phase 4 | Phase 5 | 视频演示项目路径（Article.tsx hero 标题 / Lead 文本 / 5 个 Raw 块是精修的素材） |
| Phase 2+3 | Phase 5 | 横纵报告 / 公众号文章 都可作为精修底料 |
| Phase 3 | Phase 6 | 公众号文章 .md 文件路径 |
| Phase 4 | Phase 6 | 视频演示 standalone HTML |
| Phase 5 | Phase 6 | 精修 HTML/PDF |

---

## 版本

v1.2 — 重大更新。基于 2026-06-18 黄仁勋 5 层蛋糕项目的完整 5 阶段工作流沉淀。

新增：
- Phase 5 beautiful-article 精修网页（Checkpoint 1/2/3 + 三大避坑 + 主题推荐）
- Mimo TTS 详细使用文档（4 坑 + Python 模板）
- 工作目录软链机制
- 视频演示 · audio 章节（mmx-cli / Mimo / TTS 决策）
- beautiful-article · reacticle d.ts 三大 props 错误
- 完整文件 / 软链 / 整理规则

基于 2026-06-16 会话的完整工作流（v1.0）和 2026-06-18 黄仁勋 5 层蛋糕项目（v1.1）的沉淀。
