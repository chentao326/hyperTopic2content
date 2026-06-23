# DESIGN.md 自动推断规则

Phase 4 Step D 使用。从 B1 网页 CSS 提取视觉 token 或从 Phase 2 报告类型推断基础视觉。

## 层面 2 = 是（从 B1 网页 CSS 提取）

### 提取逻辑

读 B1 网页演示的 CSS 文件（`presentation/src/App.css` / `index.css` / `tailwind.config.js`），提取：

1. 主色（accent）：`--color-primary` / `--accent` / `theme.colors.primary` → DESIGN.md accent
2. 背景色：`--color-bg` / `background-color` on body → DESIGN.md background
3. 辅色（muted）：`--color-muted` / `--color-secondary` → DESIGN.md secondary
4. 字体：`font-family` on body / headings → DESIGN.md typography
5. 圆角：`border-radius` 默认值 → DESIGN.md corners
6. 阴影：`box-shadow` 用法 → DESIGN.md depth level

### 提取示例

假设 B1 的 CSS 有：
```css
:root {
  --color-primary: #4ec9b0;
  --color-bg: #0a0e1a;
  --color-muted: #6b7a90;
  --font-body: 'Inter', sans-serif;
}
body { border-radius: 8px; }
```

生成 DESIGN.md:
```yaml
accent: "#4ec9b0"
background: "#0a0e1a"
secondary: "#6b7a90"
font: "Inter"
corners: 8px
depth: subtle
```

### 容错

- CSS 变量找不到 → 从报告类型推断（见下面的基础规则）
- 字体是系统字体 → 换 Inter（HyperFrames 内置）
- 颜色值是 RGB/rgb/hsl → 转 hex

## 层面 2 = 否（从 Phase 2 报告类型推断）

### 基础规则表

| Phase 2 报告类型 | 背景色 | 强调色 | 辅色 | 字体 | 圆角 | 深度 |
|----------------|-------|-------|-----|-----|-----|-----|
| 产业战略 / 公司研究 | #0a0e1a 深蓝黑 | #4ec9b0 青绿 | #6b7a90 灰蓝 | Inter 700 | 8px | subtle |
| 技术解析 | #0d1117 深色 | #58a6ff 蓝 | #8b949e 灰 | Inter 600 | 4px | flat |
| 产品评测 | #f8f9fa 浅白 | #e53935 红 | #757575 灰 | Inter 700 | 12px | medium |
| 人物故事 | #2d1f0e 深褐 | #f5a623 暖黄 | #8d6e63 棕 | Inter 500 | 16px | medium |
| 金融 / 数据密集 | #0f111a 暗色 | #f0b90b 金黄 | #848e9c 灰 | Inter 700 + mono | 4px | subtle |
| 人文 / 文化 | #f5f0e8 奶白 | #c0583e 砖红 | #a89f91 米灰 | 衬线 | 4px | flat |

### 报告类型自动判断

从 Phase 2 报告的标题/关键词推断：
- 含 "战略" "布局" "路线" "竞争" → 产业战略
- 含 "技术" "架构" "原理" "算法" → 技术解析
- 含 "评测" "对比" "体验" → 产品评测
- 含 "故事" "人物" "传记" → 人物故事
- 含 "财报" "数据" "收入" "股价" → 金融
- 含 "文化" "艺术" "电影" → 人文

## DESIGN.md 最小格式

```yaml
accent: "#HEX"
background: "#HEX"
secondary: "#HEX"
font: "Inter"
corners: "8px"
depth: "subtle"
```

HyperFrames 启动时会优先读这份文件。生成后落盘到 B2 项目根目录 `DESIGN.md`。Phase 4 Step D 的 ⏸ 处确认。
