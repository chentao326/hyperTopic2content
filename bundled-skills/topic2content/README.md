# Topic2Content — 话题→内容全管线

一个 Hermes Agent 技能，输入一个话题（产品、公司、概念、技术），自动跑通舆情扫描→横纵分析→公众号文章→视频演示→精修网页的完整内容生产管道，产出一站式内容五件套。

## 它能做什么

- 话题输入，自动输出整套内容
- 横纵分析深度报告（1-3万字 + HTML + PDF）
- 公众号风格长文（4000-8000字，口语化叙事，自动自检）
- 网页视频演示（React项目 + 自动翻页 + 音频合成）
- 精修网页文章（单文件HTML + PDF，断网可开）
- 自动发布（飞书知识库 + 知乎）

## 前置条件

- **Hermes Agent**（必需，本技能是 Hermes Skill）
- 其他依赖 skill（运行时自动加载）：
  - `hv-analysis` — 横纵分析法深度研究
  - `khazix-writer` — 卡兹克风格公众号文章
  - `web-video-presentation` — 网页视频演示
  - `beautiful-article` — 精修网页文章
  - `last30days-cn` — 中文平台舆情扫描
- Node.js >= 22（视频演示用）
- Python >= 3.9 + openai-whisper（字幕用）
- FFmpeg（音频处理用）
- TTS API key（推荐 mimo 或 edge-tts 免费替代）

## 安装方法

### 方式一：Hermes Skill 自动安装

```bash
# 如果 skill 在 GitHub 上，通过 Hermes 安装
hermes skill install <repo-url>

# 或者手动下载 zip 后
unzip topic2content.zip -d ~/.hermes/skills/
```

### 方式二：手动复制

```bash
# 把 topic2content 文件夹复制到 Hermes 的 skills 目录
cp -r topic2content ~/.hermes/skills/
```

### 方式三：其他 Agent（Codex / Claude Desktop）

也兼容 Codex CLI 和 Claude Desktop 的 skills 格式：

```bash
# Codex
cp -r topic2content ~/.codex/skills/
# Claude Desktop
cp -r topic2content ~/.claude/skills/
```

装好之后在 Agent 中直接跟它说「研究一下 XX」或「帮我分析 XX」即可触发。

## 使用方式

| 你说 | 它做 |
|------|------|
| 「研究一下XX」 | 横纵分析报告 + 公众号文章（默认） |
| 「出全套」 | 舆情扫描 → 报告 → 文章 → 视频演示 |
| 「把这份报告做成视频」 | 只跑视频演示阶段 |
| 「精修成网页文章」 | 只跑精修网页阶段 |
| 「出全套 + 网页精修」 | 全部五个阶段 |

支持快捷指定目标，可以组合使用。

## 管道流程

```
用户输入话题
  │
  ├─ Phase 0: 模式识别（判断用户要什么）
  ├─ Phase 1: 舆情扫描（30天热点，可选）
  ├─ Phase 2: 横纵分析报告（必跑，1-3万字深度报告）
  ├─ Phase 3: 公众号文章（默认跑，4000-8000字）
  ├─ Phase 4: 视频演示（可选，React网页演示+配音）
  ├─ Phase 5: 精修网页（可选，单文件HTML+PDF）
  └─ Phase 6: 三平台发布（可选，飞书+知乎）
```

每个阶段产出独立的文件，产物之间不互相覆盖，可以单独提取使用。

## 产出命名规范

所有产出按统一格式组织：

```
<日期>_<话题>_<类型>_v<版本>/
├── <日期>_<话题>_横纵分析报告_v<版本>.md
├── <日期>_<话题>_公众号文章_v<版本>.md
└── <日期>_<话题>_视频演示_v<版本>/
    ├── script.md
    ├── outline.md
    └── presentation/
```

## 技术要求

- 视频演示需要 Node.js 18+（推荐 22），装好依赖后可以离线开发
- 音频合成推荐使用 edge-tts（免费，零配置）或 mimo TTS（中文质量好）
- whisper 字幕需要 small 模型（461MB）

## 文件结构

```
topic2content/
├── SKILL.md                  # 技能主文件（Hermes Agent 加载用）
├── README.md                 # 本文件
└── references/
    ├── checklist.md          # 各阶段质检清单
    └── pitfalls.md           # 已知坑和修复方法
```

## 许可

MIT
