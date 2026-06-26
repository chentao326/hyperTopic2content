# hyperTopic2content — 话题→内容全管线（含真 MP4 视频）

输入一个话题（产品、公司、概念、技术），自动跑通舆情扫描→横纵分析→公众号文章→视频生成（网页演示 + 真 MP4 视频）→精修网页文章的完整内容生产管道，产出内容六件套。相比 topic2content，新增了 HyperFrames 渲染的 MP4 视频输出。

## 它能做什么

- 话题输入，自动输出全套内容 + 视频
- 横纵分析深度报告（1-3万字 + HTML + PDF）
- 公众号风格长文（4000-8000字，支持卡兹克/半佛两种风格）
- **网页视频演示**（React 项目，自动翻页 + 分段配音，每步音画同步）
- **真 MP4 视频**（HyperFrames 渲染，1920x1080 H.264，短视频/完整版双模式）
- 精修网页文章（单文件 HTML + PDF，断网可开）
- 自动发布（飞书知识库 + 知乎）

## 前置条件

- **Hermes Agent**（必需）
- 依赖 skills：
  - `hv-analysis` — 横纵分析法
  - `khazix-writer` / `hottake-writer` — 公众号文章
  - `web-video-presentation` — 网页演示
  - `beautiful-article` — 精修网页
  - `last30days-cn` — 舆情扫描
- Node.js >= 22（网页演示 + HyperFrames）
- Python >= 3.9 + openai-whisper（字幕）
- FFmpeg
- HyperFrames CLI（`npx hyperframes@0.7.3`）
- TTS API（推荐 mimo TTS 或 edge-tts）
- whisper small 模型（461MB）

## 安装方法

### 方式一：Hermes Skill 安装

```bash
# 从 GitHub 安装
hermes skill install <repo-url>

# 或手动
unzip hypertopic2content.zip -d ~/.hermes/skills/
```

### 方式二：手动复制

```bash
cp -r hypertopic2content ~/.hermes/skills/
```

### 方式三：其他 Agent（Codex / Claude Desktop）

```bash
# Codex
cp -r hypertopic2content ~/.codex/skills/
# Claude Desktop
cp -r hypertopic2content ~/.claude/skills/
```

装好之后在 Agent 里说「研究一下 XX 出视频」或「XX 是什么来头出全套」即可触发。

## 使用方式

### 快捷指令

| 你说 | 它做 |
|------|------|
| 「研究一下XX」 | 横纵分析报告 + 公众号文章（默认，不跑视频） |
| 「研究一下XX，出视频」 | 报告 + 文章 + MP4 视频 |
| 「研究一下XX，出全套」 | 舆情 → 报告 → 文章 → 网页演示 → MP4 视频 → 精修网页 |
| 「XX 出 MP4 短视频」 | 报告 + 文章 + 短视频版 MP4 |
| 「把这份报告做成视频」 | 只用已有报告跑视频阶段 |
| 「精修成网页文章」 | 只跑精修网页阶段 |

### 双模式运行

启动时会问你：**检查点模式**还是**自动推进**？

- 检查点模式：每个阶段产物落盘后暂停，等你确认再继续
- 自动推进：一口气跑到底，每步播报进度但不停止

可以随时在检查点改成自动推进。

### MP4 视频三档可选

| 版本 | 时长 | 字数 | 适合场景 |
|------|------|------|----------|
| 短视频 | 30-60秒 | 120-220字 | B站/视频号引流 |
| 完整版 | 90-180秒 | 300-600字 | 深度展示 |
| 全都要 | 两组 | 各档分别 | 同时产出短+长两个版本 |

## 管道流程

```
用户输入话题
  │
  ├─ Phase 0: 模式识别 + 运行模式选择
  ├─ Phase 1: 舆情扫描（可选）
  ├─ Phase 2: 横纵分析报告（必跑）
  ├─ Phase 3: 公众号文章（默认跑，卡兹克/半佛风格）
  ├─ Phase 4: 视频生成（核心改造，可选）
  │   ├─ Step A: 口播稿统一生成（script.md + script_full.txt + outline.md）
  │   ├─ Step B: TTS 试听确认（3音色×10秒试听）
  │   ├─ Step C: 视觉一致选择
  │   ├─ Step D: DESIGN.md 生成
  │   ├─ Step E: B2 TTS + whisper + 字幕
  │   ├─ Step F: B1 网页演示（React 项目，可选）
  │   └─ Step G: B2 MP4 渲染（HyperFrames，短视频/完整版/全都要）
  ├─ Phase 5: 精修网页（可选）
  └─ Phase 6: 三平台发布（可选）
```

## 核心设计原则

- **音画同步**：每步独立音频文件，播完自动切页，告别连续音频漂移问题
- **预览优先**：MP4 渲染前必须先浏览器预览审核视觉
- **产物独立**：每步产出都是独立文件，可单独提取使用
- **进度播报**：长步骤完成后通知产物路径和关键指标
- **模块化**：B1 网页演示和 B2 MP4 可各自单跑或并联

## 文件结构

```
hypertopic2content/
├── SKILL.md                    # 技能主文件
├── README.md                   # 本文件
├── scripts/
│   └── whisper_to_transcript.py  # whisper JSON → HyperFrames 字幕
└── references/
    ├── phase4b-pipeline.md     # B2 MP4 视频 7 步详细流程
    ├── pitfalls.md             # 已知坑和修复方法
    ├── script-extraction-prompt.md  # 口播稿生成模板
    ├── three-platform-publish.md    # 三平台发布流程
    ├── B2-视觉质量要求.md          # MP4 视觉风格要求
    ├── B2-newsroom-workflow.md      # 新闻室主题工作流
    ├── checklist.md                 # 质检清单
    └── design-inference-rules.md    # 视觉规则推断表
```

## 技术要求

- 网页演示需要 Node.js 22+ 和 npm
- HyperFrames 渲染需要 `npx hyperframes@0.7.3`（建议先 `npm install hyperframes` 提前缓存）
- 音频合成推荐 mimo TTS（中文音色：冰糖/茉莉/苏打/白桦）
- 免费替代：edge-tts（`pip install edge-tts`，零配置）
- whisper 字幕需要 small 模型（自动下载约 461MB）
- 渲染预计耗时：短视频 60-90秒，完整版 5-10分钟

## 许可

MIT
