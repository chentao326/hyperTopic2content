# Phase 4b MP4 视频详细流程

从 `text-to-video-pipeline` skill 移植。这是 B2（MP4 视频输出）的 7 步执行细节。SKILL.md 中 Phase 4 Step E/G 会引用本文档。

## 前置条件

- Node.js >= 22 / FFmpeg / Python 3.9 + openai-whisper 20250625
- whisper small 模型已下载（~/.cache/whisper/small.pt, 461MB）
- HyperFrames CLI: `npx hyperframes 0.7.3`
- mimo-v2.5-tts key（优先 `MIMO_API_KEY`；也可放 `~/.mimo_credentials` 或 `~/.hermes/secrets/mimo.key`，权限 600）

离线预检：

```bash
npm_config_yes=false npm_config_offline=true npx --no-install hyperframes --version
```

如果报 `ENOTCACHED` 或找不到包，先在允许联网的环境执行 `npm install hyperframes@0.7.3`，再重跑预检。不要直接裸跑 `npx hyperframes`，避免交互安装或长时间等待。

## 7 步流程

如果 Step A 选择「全都要」，下面 Step 1-7 必须分别执行两轮：

```bash
# 短视频轮
VIDEO_VARIANT=short
SCRIPT_FULL=script_full_short.txt
VIDEO_DIR_NAME=my-video-short

# 完整版轮
VIDEO_VARIANT=full
SCRIPT_FULL=script_full_full.txt
VIDEO_DIR_NAME=my-video-full
```

如果只生成单一版本，默认使用：

```bash
VIDEO_VARIANT="${VIDEO_VARIANT:-full}"
SCRIPT_FULL="${SCRIPT_FULL:-script_full.txt}"
VIDEO_DIR_NAME="${VIDEO_DIR_NAME:-my-video}"
```

### Step 1: TTS 配音

**mimo 路线（推荐）**:
```bash
SCRIPT_FULL="${SCRIPT_FULL:-script_full.txt}"
if [ -z "$MIMO_API_KEY" ] && [ -f ~/.mimo_credentials ]; then
  export MIMO_API_KEY="$(cat ~/.mimo_credentials)"
fi
python3 <mimo_skill_dir>/scripts/mimo_tts.py \
  --text "(快读)$(cat "$SCRIPT_FULL")" \
  --voice <Step B 确认的音色> \
  --output mimo_audio.wav
ffmpeg -y -i mimo_audio.wav -codec:a libmp3lame -b:a 128k audio.mp3
```

`<mimo_skill_dir>` 必须从可用 skill 路径解析，不写死本机历史目录。不要传 `--context`，该脚本会把 context 放入 user message，部分部署会把 user content 一起念出来。风格控制放在 assistant 文本前缀，如 `(快读)`。

**edge-tts 降级路线**:
```bash
SCRIPT_FULL="${SCRIPT_FULL:-script_full.txt}"
export PATH=$HOME/Library/Python/3.9/bin:$PATH
edge-tts --voice <Step B 确认的音色> \
  --text "$(cat "$SCRIPT_FULL")" \
  --write-media audio.mp3
```

写入真实音频时长，供 HyperFrames 模板设置 composition/audio duration：

```bash
ffprobe -v error -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 audio.mp3 \
  | awk '{printf "{\"duration\":%.3f}\n", $1}' > duration.json
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
PROJECT_DIR="$(pwd)"
HYPERTOPIC_SKILL_DIR="<hyperTopic2content_skill_dir>"
python3 "$HYPERTOPIC_SKILL_DIR/scripts/whisper_to_transcript.py" "$PROJECT_DIR/audio.json" "$PROJECT_DIR/transcript.json"
```

### Step 4: HyperFrames 初始化

开始前必须在 B2 项目根目录执行，且该目录已经有 `audio.mp3`、`duration.json`、`transcript.json`、`DESIGN.md`。

```bash
PROJECT_DIR="$(pwd)"
VIDEO_DIR_NAME="${VIDEO_DIR_NAME:-my-video}"
VIDEO_DIR="$PROJECT_DIR/$VIDEO_DIR_NAME"

cd "$PROJECT_DIR"
npx hyperframes init "$VIDEO_DIR_NAME" --audio "$PROJECT_DIR/audio.mp3" --non-interactive
cp "$PROJECT_DIR/audio.mp3" "$PROJECT_DIR/transcript.json" "$PROJECT_DIR/duration.json" "$PROJECT_DIR/DESIGN.md" "$VIDEO_DIR/"
cd "$VIDEO_DIR"
NODE_ENV=development npm install gsap
```

⚠️ HyperFrames 0.7.3 transcribe 命令有 bug，不能用。直接用 Step 2 的 openai-whisper CLI。

### Step 5: 写 HTML 合成

当前目录必须是 HyperFrames 视频目录（默认 `my-video/`；全都要时为 `my-video-short/` 或 `my-video-full/`）。先把本 skill 的模板落到 HyperFrames 入口文件，再读 Step D 复制进来的 DESIGN.md 决定视觉风格并替换标题、配色和章节文案。

```bash
HYPERTOPIC_SKILL_DIR="${HYPERTOPIC_SKILL_DIR:-<hyperTopic2content_skill_dir>}"
VIDEO_DIR="$(pwd)"
cp "$HYPERTOPIC_SKILL_DIR/references/example-index.html" "$VIDEO_DIR/index.html"
```

`index.html` 必须基于 `references/example-index.html` 完成改写（已包含 `transcript.json` 同步读取 + `duration.json` 真实音频时长读取 + 本地 GSAP 动画 + 词级高亮模板），不能保留 `npx hyperframes init` 生成的默认页面，不能重新引入 CDN 脚本。

核心约束：
- root div 必须有 data-composition-id / data-width / data-height
- 字体只能用 built-in font（不能用 PingFang / Microsoft YaHei）
- timeline 注册名必须匹配 data-composition-id
- `#main` 和 `<audio>` 必须在 `#root[data-composition-id]` 内
- 字幕数据必须来自 `transcript.json`，不能保留示例 `WORDS` 数组
- composition/audio 时长必须来自 `duration.json`，并用 `Math.max(audioDuration, lastTranscriptEnd)` 覆盖字幕尾部误差
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
