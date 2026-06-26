# PIL + ffmpeg MP4 输出（Phase 4b 退化路径）

当 React 网页演示 + 自动录屏 / HyperFrames 渲染均不可行时，用此退化路径
生成口播视频。原理：为每段音频生成一帧图像（PIL 渲染文字），ffmpeg 逐段
合成后拼接。

## 适用场景

- React 项目的 `?auto=1` 录屏不流畅（浏览器卡顿 / 交互复杂）
- 没装 Playwright / Puppeteer 等 headless 浏览器工具
- HyperFrames capture 只能拿 1 帧（React SPA 需 JS 交互才能翻页）
- 快速出 MVP：口播稿已定，视觉只需基本的文字 + 配色

## 不适用场景

- 需要章节式视觉幻灯片（数据卡片 / 对比图 / 动画）—— 这些用 React 网页
  演示 + 录屏才是正确路径
- 需要字幕 —— 此路径只输出纯视频，如需字幕用 whisper 单独加

## 流程

```
1. audio-segments.json 已存在（Phase 3 产物）
2. Python PIL 为每段创建 1920×1080 帧图像（底色 + 居中文字）
3. ffmpeg 逐段合成：循环帧 + 对应 MP3 → 临时 .ts 文件
4. ffmpeg concat 拼接所有 .ts → 最终 MP4
```

## 依赖

```bash
pip install Pillow
ffmpeg (已安装)
```

## 核心代码

```python
from PIL import Image, ImageDraw, ImageFont

# 创建背景
bg = Image.new("RGB", (1920, 1080), (245, 237, 222))  # kraft-paper cream

# 文字渲染（自动换行）
font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 36)
draw = ImageDraw.Draw(img)
lines = [text[i:i+40] for i in range(0, len(text), 40)]
y = 400
for line in lines:
    draw.text((200, y), line, fill=(80, 60, 40), font=font)
    y += 50

# ffmpeg 逐段合成
subprocess.run([
    "ffmpeg", "-y",
    "-loop", "1",          # 循环帧（静止画面）
    "-i", str(frame_path),  # 帧图像
    "-i", str(audio_path),  # 音频
    "-c:v", "libx264",
    "-tune", "stillimage", # 静止图像优化
    "-c:a", "aac",
    "-b:a", "96k",
    "-pix_fmt", "yuv420p",
    "-shortest",            # 以音频长度为准
    str(seg_output)
])

# 拼接所有段
with open("concat.txt", "w") as f:
    for sf in segment_files:
        f.write(f"file '{sf}'\n")

subprocess.run([
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0",
    "-i", "concat.txt",
    "-c", "copy",
    "final.mp4"
])
```

## 配色参考（kraft-paper 主题）

| 属性 | 值 |
|------|-----|
| 背景色 | #f5edde (奶油米) |
| 文字色 | #503c22 (深棕) |
| 高亮色 | #d4a373 (陶土) |
| 卡片背景 | #efe6d3 (浅米) |
