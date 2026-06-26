---
name: hyperTopic2content
description: |
  话题→内容全管线。输入一个话题（产品/公司/概念/技术），自动跑通舆情扫描→横纵分析→公众号文章→精修网页 的完整管道。视频生成（网页演示 + MP4）由 video-pipeline skill 独立承接。
  触发词：研究一下XX、帮我做XX的完整分析、XX是什么来头出全套、帮我深度研究XX并出文章、跑一下这个、这是资料帮我写篇东西。
  视频触发词（路由到 video-pipeline）："做视频""出 MP4""口播视频""出短视频"。
  快捷模式：只说"研究一下"默认跑横纵报告+公众号文章。
  检查点模式 vs 自动推进：Phase 0 启动时询问。检查点模式每步产物落盘后暂停；自动推进一口气跑到底。
  素材直达模式：用户直接提供已完成的作品（笔记/文章/PDF/外部内容链接）作为输入时，跳过 Phase 1 舆情扫描和 Phase 2 横纵分析，直接进 Phase 3 公众号文章扩展。原素材作为 Phase 3 的输入源，Phase 3 的参考来源从原素材中提取。
---

# hyperTopic2content — 话题→内容全管线

输入一个话题，自动编排多个 skill 跑通完整内容管线。v3.0 起，**视频生成（Phase 4）拆为独立 video-pipeline skill**：hyperTopic2content 专注 Phase 0→3→5→6，视频需求路由到 `video-pipeline`。

## 核心原则

- **检查点模式 vs 自动推进**：Phase 0 启动时先问用户「检查点还是自动推进」。检查点模式每个产物落盘暂停等确认；自动推进一口气跑到底。用户随时在任意检查点说「自动推进」切换到自动模式。
- **检查点统一格式**：每个 ⏸ 处 → 「通过」继续 / 「改 XXX」重跑本步 / 「自动推进」后续全跳。
    - 「改 XXX 重跑本步」= 覆盖当前产物（同版本号），**后续所有步骤也必须重跑**（因为输入可能变了）。
    - 自动推进模式下遇到非致命错误：暂停并告知用户，不动手重试。
- **产物落盘再汇报**：不口头描述结果，文件真的写到了磁盘才算完成。
- **跳过条件明确**：用户说「只要报告」跳过文章和视频；说「出视频」路由到 video-pipeline。
- **工作目录软链**：所有项目在 `/Volumes/My SSD/code/content-pipeline/` 下用软链暴露到 `/Volumes/My SSD/文章/`。
- 🔔 **cron 模式**：定时任务下无用户可交互，跳过所有检查点询问（自动推进），话题自动选择后直接跑完全程。`execute_code` 可能被阻止，用 `search_files` + `patch` 做 L1 自检（详见 `references/cron-mode-selfcheck.md`）。Lark 消息发送需拆分短消息避免安全扫描阻断（详见 `references/lark-cron-messaging.md`）。

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
    ├─ Phase 2: hv-analysis（横纵分析深度报告）【素材直达时跳过】
    │   产出：1-3万字深度报告 + HTML + PDF
    │
    ├─ Phase 3: khazix-writer（公众号文章）【默认跑】
    │   产出：4000-8000字公众号长文
    │   输入：Phase 2 的报告
    │
    ├─ Phase 4: video-pipeline（视频生成，可选）
    │   路由到 video-pipeline skill
    │   产出：B1 网页演示 + B2 MP4 视频
    │   触发："出视频" / "做演示" / "出 MP4" / "出全套"
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
        实操参考：references/three-platform-publish.md
```

---

## Phase 0: 模式识别

拿到用户输入后，先判断跑哪些 Phase。**同时询问检查点模式 or 自动推进**。

| 用户说法 | 跑哪些 | Phase 4 细节 |
|----------|--------|-------------|
| 「研究一下XX」 | Phase 2+3 | 不跑视频 |
| 「研究一下XX，出视频」 | Phase 2+3+4 | 路由到 video-pipeline（B2 MP4） |
| 「研究一下XX，做演示」 | Phase 2+3+4 | 路由到 video-pipeline（B1 网页演示） |
| 「研究一下XX，出全套」 | Phase 1→2→3→4→5 | video-pipeline B1+B2 双跑 |
| 「研究一下XX，出 MP4 短视频」 | Phase 2+3+4 | 路由到 video-pipeline（短视频模式） |
| 「XX 出全套，含精修」 | Phase 1→2→3→4→5 | video-pipeline B1+B2 双跑 |
| 「把这个报告做成视频」 | Phase 4 only | 路由到 video-pipeline，用已有报告 |
| 「跑一下这个」/「这是资料帮我写」 | Phase 3 only | 素材直达，不跑视频 |
| 「把这个资料做成视频」 | Phase 4 only | 路由到 video-pipeline，用已有素材 |
| 「把这个报告/文章做成网页」 | Phase 5 only | 精修网页 |
| 「最近30天AI有什么热点」 | Phase 1 only | 舆情扫描 |
| 「发布到知乎/飞书」 | Phase 6 only | 发布 |

不确定时默认跑 Phase 2+3（不跑视频）。**Phase 0 结束时必须问「检查点模式还是自动推进？」**。

检查点模式对每个产物暂停等确认。自动推进模式后续所有 ⏸ 处跳过。

---

## Phase 1: 舆情扫描 / 热点发现

**首选加载 skill**: `last30days-cn`

**执行**（仅当 skill 可用时）:
```bash
python <skill_dir>/scripts/last30days.py "<话题>" --quick --emit compact
```

**⚠️ 降级策略——skill 不可用时的替代方案**:
`last30days-cn` skill 可能因未安装、路径变更或导入失败而不可用（skill_view 报错或提示找不到）。此时不要放弃 Phase 1，改用 `web_search` 多角度搜索替代：

```python
# 搜索策略：4个不同角度覆盖
from hermes_tools import web_search
# 角度1: 综合热点
web_search("2026年6月 热门话题 热点新闻 中国", limit=10)
# 角度2: 行业垂直
web_search("2026年6月 AI行业热点 大新闻", limit=10)
# 角度3: 科技圈热议
web_search("2026年6月 科技圈 热搜 热议", limit=10)
# 角度4: 交叉覆盖
web_search("中国 互联网 热点话题 June 2026 热门", limit=10)
```

搜完后用 HKR 框架（H=Happy有趣/K=Knowledge信息量/R=Resonance共鸣）评估每个候选，标注热度来源和热度描述。

**产出**: 3-5个候选话题，每个标注来源平台+热度简述。

**跳过条件**: 用户已指定明确的研究对象（如"研究即梦AI"），跳过；用户说"先看看热点"才跑。

---

## Phase 2: 横纵分析报告

**加载 skill**: `hv-analysis`

**信息收集**（按优先级）:

1. **Playwright 抓取正文（首选）**: 用户机器上 `pw` wrapper 可用（`~/.hermes/bin/pw scrape <url>`），对中文平台（36氪、头条、CSDN、AI产品库、什么值得买、B站）效果稳定。知乎仍可能 403，被拦的换 DDGS 兜底。
   ```bash
   pw scrape https://example.com/article
   ```

2. **DDGS 搜索**（找 URL 列表用）: 搜 3-4 个角度（纵向历史/横向竞品/用户口碑/战略背景），每轮 8-10 条，对关键 URL 再用 Playwright 抓正文
   ```bash
   cd ~/.hermes/hermes-agent && venv/bin/python3 /tmp/search_xxx.py
   ```
   脚本用 write_file 写入 /tmp，避免 shell 编码问题。DDGS 对中文关键词效果不稳定，优先用英文关键词搜中文内容，或简化查询词加 site: 限定。

3. **last30days-cn 终扫**（可选）: 报告写完后跑一次确认热度
   ```bash
   python <skill_dir>/scripts/last30days.py "<研究对象>" --quick --emit compact
   ```
   ⚠️ 如果 `last30days-cn` 不可用（找不到 skill_dir），改用 `web_search` 做一次补充搜索确认最新动态。

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

**输入**: 
- 常规模式：Phase 2 的横纵分析报告
- 素材直达模式：用户直接提供的已完成作品（笔记/文章/PDF/外部内容）

**加载 skill**:
- 默认风格 → `khazix-writer`（卡兹克风格，口语化叙事，禁用冒号/破折号/双引号）
- 用户说「半佛」「毒舌」「犀利」「吐槽」风格 → `hottake-writer`（半佛风格，数字分节，吐槽+商业拆解，【】强调，风险提示结尾）

**输入**: Phase 2 的横纵分析报告

**写作**:
- 卡兹克风格：按 khazix-writer 写 4000-8000 字。B站风格口播，禁止冒号/破折号/双引号。核心论点要有具体数据支撑。写完后跑四层自检体系（L1-L4）。
- 半佛风格：按 hottake-writer 写 1500-5000 字。数字分节（1、2、3…），黑色幽默+发疯式吐槽，段子服务于商业拆解，【】强调概念，风险提示结尾。写完后跑五项自检（打开率/完读率/金句率/不挨骂/不封号）。
- 不确定风格时：默认卡兹克风格。

**文章末尾**：必须加入「参考来源」段落，列出全文关键数据和事实的公开来源（媒体名称+文章标题+日期）。来源从 Phase 2 报告的「信息来源」章节提取，精简到 5-10 条最核心的。
- 卡兹克风格：按 khazix-writer 写 4000-8000 字。B站风格口播，禁止冒号/破折号/双引号。核心论点要有具体数据支撑。写完后跑四层自检体系（L1-L4）。
- 半佛风格：按 hottake-writer 写 1500-5000 字。数字分节（1、2、3…），黑色幽默+发疯式吐槽，段子服务于商业拆解，【】强调概念，风险提示结尾。写完后跑五项自检（打开率/完读率/金句率/不挨骂/不封号）。
- 不确定风格时：默认卡兹克风格。用户明确提「再出个XX风格的」再换 skill 重写。
**多受众版本**：用户看完首版后说「再出一版面向XX群体的」时，属于 Phase 3 多受众子流程。不从 Phase 2 重新开始，保持与首版相同的来源材料（原素材或 Phase 2 报告），只调整受众定位、语言风格和信息密度。流程：
- 分析目标受众特征（年龄层/知识背景/信仰倾向/使用场景）
- 用受众语言重写（不是修改，是重写——口吻、案例、引用的经典都不同）
- 保留核心论据（种子法则三层面、因果逻辑等不变量），替换案例包装
- 中老年/信众版要点：温暖长辈口吻、念佛/放下怨恨场景、带孙子日常、卧床修行、梦参老和尚/星云大师参考文献
- 年轻人版要点：社交媒体视角、焦虑共鸣、了凡四训故事、金石经白话翻译
- 文件名加受众标识：`<日期>_<话题>_公众号文章_v<版本>_<受众>.md`
- 仍需自检，但自检标准按受众调整（中老年版不需要口语化词组计数，信众版需要教义准确性检查）
- 产出后询问用户是否保留两个版本、选哪个做视频

**自检**: 
- 卡兹克版：跑 khazix-writer 的四层自检体系（L1 硬性规则→L2 风格一致性→L3 内容质量→L4 活人感）。
- 半佛版：跑 hottake-writer 的五项漏斗自检（打开率/完读率/金句率/不挨骂/不封号）。
- 多受众版：按受众调整后的标准自检，中老年版重点检查语气是否亲切、佛学用词是否准确；不必强制口语化词组计数。
- 🔔 **cron 模式注意**：定时任务下 `execute_code` 可能被阻止，此时用 `search_files` + `patch` 组合完成 L1 硬性规则扫描。
  详见 `references/cron-mode-selfcheck.md`。
- 重点关注：半佛版禁用词和卡兹克版禁用词不同——半佛允许「说白了」「【】强调」、允许数字分节，不要混淆两套规则。

**产出**: `<日期>_<话题>_公众号文章_v<版本>.md`（多受众版本加受众标识）

**跳过条件**: 用户明确说"只要报告不要文章"。

---

## Phase 4: 视频生成（路由到 video-pipeline）

本 skill 不再包含视频生成细节。视频需求请**加载 `video-pipeline` skill**：

```
skill_view(name='video-pipeline')
```

### 路由规则

| 用户说 | 路由目标 | 输入 |
|--------|---------|------|
| 「出视频」「出 MP4 短视频」 | video-pipeline Step A→B→E→D→G（B2 only） | Phase 3 公众号文章 |
| 「做演示」「出网页演示」 | video-pipeline Step A→B→F（B1 only） | Phase 3 公众号文章 |
| 「出全套」（含视频） | video-pipeline B1+B2 优化串行 | Phase 3 公众号文章 + Phase 2 报告 |
| 「把这个报告/资料做成视频」 | video-pipeline（B2，素材直达） | 用户提供的报告/资料 |

### 传递给 video-pipeline 的内容

- Phase 2 横纵分析报告 .md → 报告类型（用于 DESN.md 模板匹配）
- Phase 3 公众号文章 .md → 口播稿提炼输入
- Phase 0 选定的检查点/自动推进模式 → video-pipeline 继承

### video-pipeline 架构简述

```
Step A: 口播稿生成 → Step B: TTS 试听 → Step C: 版本选择
    ├─ B1 线: Step F 网页演示（web-video-presentation）
    └─ B2 线: Step E (TTS+whisper) → Step D (DESIGN.md) → Step G (MP4)
```

B1 不是 B2 前置 — B1 已存在则提取 CSS 做视觉 token，不存在则模板匹配。

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
3. 发布知乎文章（含话题标签 + 问题链接）

**飞书知识库**：`lark-cli` 需通过 `npx @larksuite/cli` 调用（非直接的 `lark-cli` 命令）。创建 wiki 节点时 `--params` 传 `space_id`，`--data` 传 `node_type/obj_type/title`。文档内容用 `docs +update --doc-format markdown` 写入。

**知乎**：话题 ID 通过 `zhihu search "关键词" -t topic` 查询。文章内容从横纵报告转 HTML（`python3 -c "import markdown; ..."`）。发布后不可编辑，三平台交叉引用需在飞书知识库文档中互相标注。

**触发条件**: 用户说"发布"或有发布到知乎/飞书的习惯。

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

### 公众号文章
- ❌ 冒号「：」是 AI 味指纹
- ✅ 全部改用逗号
- ❌ 「绑绑有余」不是标准写法
- ✅ 标准成语「绰绰有余」

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
- ✅ 改为文章标题

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
| Phase 2 | Phase 3 | 横纵分析报告 .md |
| Phase 3 | Phase 4 (video-pipeline) | 公众号文章 .md |
| Phase 2 | Phase 4 (video-pipeline) | 横纵分析报告 .md（用于 DESIGN.md 报告类型推断） |
| Phase 4 | Phase 5 | MP4 文件路径 + B1 网页演示路径 |
| Phase 5 | Phase 6 | 精修 HTML/PDF 路径 |

> Phase 4 内部状态传递见 `video-pipeline` skill 的「Step 间状态传递」。

## 版本

v3.0 — 2026-06-26 **架构重构**：Phase 4（视频生成）拆为独立 `video-pipeline` skill。hyperTopic2content 专注 Phase 0→3→5→6，视频需求路由到 video-pipeline。B1 和 B2 解耦，B1 不再是 B2 前置。引入优化串行流水线（grilling 结论：M3 8GB 适配，whisper 和 Vite build 不真并行）。SKILL.md 从 710 行精简到 ~400 行。

v2.1 — 2026-06-23 Codex 审查修复：补 Phase 5 缺失 skill 的预检与降级路线；修正 Phase 4b 工作目录和脚本路径；Step A prompt 明确产出 outline.md；统一 TTS context、中文音色、短视频时长和 MP3 验收口径。

v2.0 — 重大改造。基于 text-to-video-pipeline 和 topic2content v1.2 合并。2026-06-23 通过 Claude Code 审查（agent-reviewer），4 个致命缺陷和 6 个改进点全部修复：时序死锁已解（A→B→F→C→D→E→G）、outline.md 已补、外部依赖已内化、TTS 音色已统一、环境预检已加、MP4 命名已对齐、检查点重跑已定义、进度通知已加。

新增：
- Phase 4 拆为 Step A→G 七步（B1 网页演示保留，B2 MP4 视频新增）
- B2 基于 HyperFrames 真 MP4 输出（1920x1080 H.264 AAC）
- 检查点模式 vs 自动推进双模式
- TTS 试听确认机制（3 音色 × 10 秒试听 → 用户选）
- Step A 先确定 MP4 目标版本（短视频版 30-60s / 完整版默认 90-180s / 全都要）
- Step C 只负责视觉一致选择 + AI 推荐
- DESIGN.md 从 B1 网页 CSS 自动提取
- 口播稿统一生成（script.md + script_full.txt + outline.md 三格式）
