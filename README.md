# hyperTopic2content — 话题→内容全管线（v3.1）

输入一个话题（产品、公司、概念、技术），自动跑通舆情扫描→横纵分析→公众号文章→精修网页文章的完整内容生产管道。**视频生成（B1 网页演示 + B2 MP4）由 topic2content 和 video-pipeline 两个独立 skill 承接。**

## 它能做什么

- 话题输入，自动输出全套内容
- 横纵分析深度报告（1-3万字 + HTML + PDF）
- 公众号风格长文（4000-8000字，卡兹克/半佛双风格）
- 多受众版本文章（中老年/年轻人等不同语体）
- 精修网页文章（单文件 HTML + PDF，断网可开）
- 三平台自动发布（飞书知识库 + 知乎 + Obsidian）
- 定时 cron 自动跑（每日热点→公众号文章全自动）

## 三层分工（v3.1 架构）

```
hyperTopic2content（路由层）← 本仓库
    ├─"做演示" → topic2content（B1 React 网页演示专家）
    ├─"出视频"  → video-pipeline（B2 MP4 截图合成专家）
    └─"出全套"  → topic2content 先跑 B1 → video-pipeline 吃产物出 B2
```

## 前置依赖

hyperTopic2content 是一个路由层，需要以下子 skill 才能完整运行。安装方式见 [bundled-skills/](bundled-skills/)。

### 已打包在本仓库（bundled-skills/）

| Skill | Phase | 说明 |
|-------|-------|------|
| topic2content | Phase 4 B1 网页演示 | React 项目 + 分段音频合成 |
| hv-analysis | Phase 2 横纵分析 | 1-3万字深度报告 |
| khazix-writer | Phase 3 公众号（卡兹克风格） | 4000-8000字长文 |

### 外部获取

| Skill | Phase | 获取方式 |
|-------|-------|---------|
| video-pipeline | Phase 4 B2 MP4 | `git clone https://github.com/chentao326/video-pipeline.git ~/.hermes/skills/software-development/video-pipeline` |
| last30days-cn | Phase 1 舆情 | `npx skills@latest add last30days-cn -g` |
| hottake-writer | Phase 3 半佛风格 | `npx skills@latest add hottake-writer -g` |
| beautiful-article | Phase 5 精修网页 | `npx skills@latest add beautiful-article -g` |

### 一键安装

```bash
git clone https://github.com/chentao326/hyperTopic2content.git
cd hyperTopic2content
cp -r bundled-skills/* ~/.hermes/skills/
npx skills@latest add last30days-cn hottake-writer beautiful-article -g
git clone https://github.com/chentao326/video-pipeline.git ~/.hermes/skills/software-development/video-pipeline
```

## 使用方式

### 快捷指令

| 你说 | 它做 |
|------|------|
| 「研究一下XX」 | 横纵分析报告 + 公众号文章（默认） |
| 「研究一下XX，出视频」 | 报告 + 文章 → video-pipeline 出 MP4 |
| 「研究一下XX，做演示」 | 报告 + 文章 → topic2content 出网页演示 |
| 「研究一下XX，出全套」 | 舆情 → 报告 → 文章 → 网页演示 → MP4 → 精修网页 |
| 「XX 出 MP4 短视频」 | 报告 + 文章 + 短视频版 MP4 |
| 「把这份报告做成视频」 | video-pipeline 素材直达 |
| 「精修成网页文章」 | 只跑 beautiful-article |
| 「发布到知乎/飞书」 | 三平台发布 |

### 双模式运行

- 检查点模式：每阶段暂停等确认
- 自动推进：一口气跑到底
- cron 模式：定时任务下无用户交互，自动推进

## 管道流程

```
用户输入话题
  │
  ├─ Phase 0: 模式识别 + 运行模式选择
  ├─ Phase 1: 舆情扫描（可选，路由到 last30days-cn）
  ├─ Phase 2: 横纵分析报告（必跑，路由到 hv-analysis）
  ├─ Phase 3: 公众号文章（默认跑，路由到 khazix-writer）
  ├─ Phase 4: 视频生成（可选）
  │   ├─ B1 路由到 topic2content（React 网页演示）
  │   └─ B2 路由到 video-pipeline（截图合成 MP4）
  ├─ Phase 5: 精修网页（可选，路由到 beautiful-article）
  └─ Phase 6: 三平台发布（可选）
```

## 文件结构

```
hypertopic2content/
├── SKILL.md                         # 技能主文件
├── README.md                        # 本文件
└── references/
    ├── checklist.md                 # 质检清单
    ├── cron-mode-selfcheck.md       # cron 模式自检方案
    ├── lark-cron-messaging.md       # cron 模式下飞书消息拆分
    └── three-platform-publish.md    # 三平台发布流程
```

## 版本

- v3.1 — 2026-06-26 路由修正：B1→topic2content，B2→video-pipeline
- v3.0 — 2026-06-26 Phase 4 拆出，专注路由层

## 许可

MIT
