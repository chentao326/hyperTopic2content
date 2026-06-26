# B2 MP4 视觉方案：web-video-presentation + HyperFrames

2026-06-23 SK海力士项目验证通过。6分38秒视频，8章节卡片+词级字幕，H.264 1920x1080 30fps，15.8MB。

## 适用场景

报告 >8000 字、视频 >2 分钟的长视频。text-to-video-pipeline 的纯 HTML 方案适合短视频（<60s），长视频用本方案的章节卡片式更有信息密度。

## 工作流

### 1. 加载 web-video-presentation skill，选主题

```bash
bash <skill_dir>/scripts/scaffold.sh --list-themes
```

推荐主题：
- newsroom（报社风格，奶油纸底+报头红，适合商业/财经分析）
- monochrome-print（黑白印刷，适合学术/深度研究）
- warm-keynote（暖色Keynote，适合 SaaS/产品分析）

### 2. 写单文件 index.html

不用 scaffold.sh 创建 React 项目（路径含空格会失败）。直接写一个 self-contained HTML：

核心结构：
- `<div id="root" data-composition-id="root" data-width="1920" data-height="1080" data-duration="N" data-start="0">`
- N 个 `<div class="scene">` 章节卡片，CSS opacity:0 默认隐藏
- `<audio src="audio.mp3" data-start="0" data-duration="N">` 声明式音频
- GSAP timeline 控制场景切换 + 字幕同步
- `fetch("transcript.json")` 加载词级字幕

### 3. 布局原则（关键！）

1920x1080 画布大，容易堆在左下角。必须：
- `.scene { display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; }`
- 大数字 `.big-num { font-size: 140px; }` 撑画面
- 多数据项 `.drow { display: flex; gap: 80px; justify-content: center; }` 横向均匀
- VS 对比块用左右拼接色块
- 时间线用左日期+右文字行式布局

### 4. 浏览器预览自动缩放

```css
#root { transform-origin: top left; }
@media (max-width: 1920px), (max-height: 1080px) {
  #root { transform: scale(calc(min(100vw / 1920, 100vh / 1080))); }
}
```

### 5. GSAP timeline 注意

- 不要对所有场景统一 `.from("#s-XX .sub")`——不是每个场景都有 `.sub`，会报大量 GSAP warning
- 用 `tl.set(id, {opacity:1}, tIn)` + `tl.set(id, {opacity:0}, tOut)` 控制场景显隐
- 字幕从 transcript.json 加载，按词时间戳 `tl.to(span, {opacity:1}, t1)` 控制

### 6. HyperFrames lint → inspect → render

```bash
npx hyperframes@0.7.3 lint          # 0 error（字体只用 Georgia/Helvetica/Arial）
npx hyperframes@0.7.3 inspect --at 2,8,30,50,70 --no-contrast --timeout 120000
npx hyperframes@0.7.3 render --output final.mp4 --quality standard
```

渲染耗时：11940帧（6.5min视频）约 10 分钟。

## 产物

- `index.html` — 单文件 HTML 合成
- `audio.mp3` — TTS 配音（mimo 白桦/冰糖等）
- `transcript.json` — whisper 词级字幕
- `final.mp4` — H.264 1920x1080 30fps AAC MP4