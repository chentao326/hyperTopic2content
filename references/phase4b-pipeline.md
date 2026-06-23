# Phase 4b MP4 视频详细流程

从 `text-to-video-pipeline` skill 移植。这是 B2（MP4 视频输出）的 7 步执行细节。SKILL.md 中 Phase 4 Step E/G 会引用本文档。

## 前置条件

- Node.js >= 22 / FFmpeg / Python 3.9 + openai-whisper 20250625
- whisper small 模型已下载（~/.cache/whisper/small.pt, 461MB）
- HyperFrames CLI: `npx hyperframes 0.7.3`
- mimo-v2.5-tts key（优先 `MIMO_API_KEY`；也可放 `~/.mimo_credentials` 或 `~/.hermes/secrets/mimo.key`，权限 600）

## 7 步流程

### Step 1: TTS 配音

**mimo 路线（推荐）**:
```bash
if [ -z "$MIMO_API_KEY" ] && [ -f ~/.mimo_credentials ]; then
  export MIMO_API_KEY="$(cat ~/.mimo_credentials)"
fi
python3 <mimo_skill_dir>/scripts/mimo_tts.py \
  --text "(快读)$(cat script_full.txt)" \
  --voice <Step B 确认的音色> \
  --output mimo_audio.wav
ffmpeg -y -i mimo_audio.wav -codec:a libmp3lame -b:a 128k audio.mp3
```

`<mimo_skill_dir>` 必须从可用 skill 路径解析，不写死本机历史目录。不要传 `--context`，该脚本会把 context 放入 user message，部分部署会把 user content 一起念出来。风格控制放在 assistant 文本前缀，如 `(快读)`。

**edge-tts 降级路线**:
```bash
export PATH=$HOME/Library/Python/3.9/bin:$PATH
edge-tts --voice <Step B 确认的音色> \
  --text "$(cat script_full.txt)" \
  --write-media audio.mp3
```

### Step 2: whisper 转字幕

```bash
export PATH=$HOME/Library/Python/3.9/bin:$PATH
whisper audio.mp3 --model small --language zh \
  --output_dir . --output_format json --word_timestamps True
```

⚠️ 必须显式 `--language zh`（small.en 默认翻译中文）。

### Step 3: 字幕格式转换

```bash
python3 <hyperTopic2content_skill_dir>/scripts/whisper_to_transcript.py audio.json transcript.json
```

### Step 4: HyperFrames 初始化

```bash
npx hyperframes init my-video --audio audio.mp3 --non-interactive
cp audio.mp3 transcript.json DESIGN.md my-video/
cd my-video
```

⚠️ HyperFrames 0.7.3 transcribe 命令有 bug，不能用。直接用 Step 2 的 openai-whisper CLI。

### Step 5: 写 HTML 合成

当前目录必须是 `my-video/`。读 Step D 复制进来的 DESIGN.md 决定视觉风格。参考本 skill 的 `references/example-index.html`（已包含完整的字幕挂载 + GSAP 动画 + 词级高亮模板）。

核心约束：
- root div 必须有 data-composition-id / data-width / data-height
- 字体只能用 built-in font（不能用 PingFang / Microsoft YaHei）
- timeline 注册名必须匹配 data-composition-id
- 字幕按 8 词/标点分组，每组一个独立 div

### Step 6: lint

```bash
npx hyperframes lint
```

常见错误：
- root_missing_composition_id → 补 data-composition-id
- root_missing_dimensions → 补 data-width/height
- timeline_id_mismatch → window.__timelines["X"] 匹配 data-composition-id
- font_family_without_font_face → 删除非内置字体引用

### Step 7: render

```bash
npx hyperframes inspect --at 1.5,5,15,25,35 --no-contrast --timeout 60000
npx hyperframes render --output final.mp4 --quality standard
```

- 短视频版: `xxx_social_v1.mp4`（30-60s）
- 完整版: `xxx_full_v1.mp4`（按脚本长度，默认 90-180s；如用户明确要长视频才扩展到 5-15min）

## 踩坑清单

1. mimo key 401 → 降级 edge-tts
2. HyperFrames transcribe bug → 绕开，用 openai-whisper CLI
3. whisper small.pt checksum 错 → 删除重下
4. whisper small.en 翻译中文 → 必须 --language zh
5. root 缺 composition-id → lint 报 3 错
6. timeline id 不匹配 → lint 报错
7. font 警告 → 删除非内置字体
8. data-duration 总时长必须覆盖音频 + buffer
