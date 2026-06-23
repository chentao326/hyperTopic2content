# 已知坑（已验证，下次遇到直接按修复方法走）

## 信息收集

| 坑 | 症状 | 修复 |
|----|------|------|
| delegate_task 子Agent 联网搜索 | 子Agent 返回「浏览器/Camofox 未运行」或「工具不可用」 | 不用子Agent，本Agent直接用 DDGS + Playwright |
| DDGS 搜中文被 shell 破坏 | 搜索无结果或乱码 | 先 write_file 写脚本到 /tmp，再 python3 执行 |
| curl 抓中文站正文 | 知乎/CSDN 只返回标题和 JS，无正文 | curl 只拿 URL 列表和元数据；正文走 Playwright |
| Playwright 抓知乎 | 返回 403「请求异常」 | 知乎反爬极严，放弃，用 DDGS body 摘要兜底 |
| Playwright 抓 CSDN | 返回 403 WAF | 同上，但 CSDN 的文章 meta description 足够详细（含评分和总结） |
| Google 搜索 | 返回 CAPTCHA/challenge 页面 | 换 Bing 或 DDGS；Google 几乎不可用 |

## npm

| 坑 | 症状 | 修复 |
|----|------|------|
| NODE_ENV=production | npm install 只装 4 个包（react+react-dom），显示 "up to date" | `NODE_ENV=development npm install` |
| npm install -g mmx-cli 报 EACCES | 系统 /usr/local/lib/ 不可写 | `npm config set prefix ~/.npm-global` + `export PATH=$HOME/.npm-global/bin:$PATH` |
| npm prefix 干扰 | 包装到了 ~/.npm-global 而非项目 node_modules | `npm config delete prefix` 或 `npm install --prefix .` |
| npm install 被识别为长进程 | terminal 报 "appears to start a long-lived server" | 用 background=true + notify_on_complete=true |

## WeasyPrint (PDF 生成)

| 坑 | 症状 | 修复 |
|----|------|------|
| libgobject 找不到 | `cannot load library 'libgobject-2.0-0'` | `brew install pango gobject-introspection` |
| 装了 pango 还报错 | 用了系统 Python 3.9 的 weasyprint v66 | 改用 Hermes 运行时 Python 3.12 (/Users/chentao/.hermes-web-ui/desktop-runtime/hermes/0.16.0/mac-arm64/python/bin/python3) |
| DYLD_LIBRARY_PATH 没设 | weasyprint 找不到 .dylib | 命令前加 `DYLD_LIBRARY_PATH=/opt/homebrew/lib` |

## web-video-presentation

| 坑 | 症状 | 修复 |
|----|------|------|
| narrations.ts 用 { text, durationMs } 格式 | extract-narrations 报 "narration must be a string" | 全部改成 string[]（纯字符串数组） |
| npm 装不上依赖 | npm install 失败（NODE_ENV 等问题） | 先用 npx create-vite 重建脚手架，再 cp 章节代码进去 |
| Vite dev server 无法启动 | `sh: vite: command not found` | 检查 npm install 是否成功；如失败走「重建脚手架」流程 |
| 播放模式 manual 模式不播 audio | useAudioPlayer 设计：manual 模式不播 | 按 M 键切到 audio 模式（播 audio 但手动翻）或 auto 模式（按 Space 触发） |
| 音频格式 mp3 | 项目代码 src 用 `.mp3` 后缀 | 改为 `.wav`（HTML5 audio 原生支持 24kHz PCM16）。在 `App.tsx` 改一行 |
| React 组件缺 jpeg/png 图片 | 视觉演示项目只能用 CSS/SVG | 0 外部图片，所有"图"用 CSS+SVG Raw 块 |

## TTS 音频合成（5 种 provider 实测对比）

### Qwen3-TTS via DashScope API（推荐首选）

| 坑 | 症状 | 修复 |
|----|------|------|
| 环境无 GPU | 本地推理 1.7B 极慢 | 走 DashScope API（阿里云百炼），不需要本地 GPU |
| dashscope SDK 未装 | ModuleNotFoundError | `pip install dashscope soundfile` |
| API key 未设 | auth 报错 | `export DASHSCOPE_API_KEY=***` |
| 输出是 PCM 不是 WAV | 浏览器不能直接播 | `ffmpeg -f s16le -ar 24000 -ac 1 -i out.pcm out.wav` 转码 |
| 模型名找不到 | 报 model not found | 用 `qwen3-tts-flash-realtime`（预置音色）或 `qwen3-tts-instruct-flash-realtime`（指令控制） |
| 中文音色不自然 | Cherry/Lucy 都不满意 | 换 Vivian（明亮）或 Serena（温柔）；或开音色克隆 |

### Mimo TTS（`mimo-v2.5-tts` + 中文 voice="冰糖"/"苏打"）

| 坑 | 症状 | 修复 |
|----|------|------|
| API 必须含 assistant role | 报 400 `"messages must contain an assistant role for TTS model"` | 必须有 `user + assistant` 两种 role |
| user content 放文本会被念 | 合成结果念了"嗯好继续"或整段指导语 | `user.content = ""`（**必须空字符串**）。文档说"user 不会出现在合成中"是错的。 |
| voice 选错 | 念出音色不是想要的 | 中文内容用 `冰糖` / `苏打` / `茉莉` / `白桦`，不要用 `mimo_default` 或英文音色 |
| 节奏偏慢（纪录片风） | 50 字念 9 秒 | assistant content 前面加 `(快读)` style tag。**不能**用 `audio.speed`（Mimo API 不支持）|
| stream chunk 是 base64-encoded PCM16 | 直接拼 raw bytes 写 .wav 即可 | 用 `wave` 标准库，不需要 ffmpeg/soundfile |
| audio 文件太大 (60MB for 93 段) | 1.5 min 合成时间 | 接受（HTML5 audio 优先 PCM16 native）。要瘦身需 ffmpeg 转 mp3 |
| Key 不能在命令行暴露 | auto mode classifier 拦截 | 把 key 写到 `~/.mimo_credentials` (chmod 600)，脚本读文件 |

### 备选 1：edge-tts（完全免费，零 API key）

```bash
edge-tts --voice zh-CN-YunjianNeural --text "你好" --write-media out.mp3
```

适合快速原型。中文女声 `zh-CN-XiaoxiaoNeural` 默认。**不能商用**。

### 备选 2：MiniMax mmx-cli（需 `mmx config set base_url`）

| 坑 | 症状 | 修复 |
|----|------|------|
| 第三方 base URL 没设 | 报 `Param Incorrect` 或 401 | `mmx config set --key base_url --value "https://third-party.com/v1"` |
| API key 在命令行 | auto mode classifier 拦截 | 用户自己 export 后跑 `mmx auth login --api-key "$MIMO_API_KEY"` |
| 合成变慢 | 1.5 min 跑完 93 段比 Mimo 慢 | 接受（质量好） |

### 备选 3：OpenAI TTS（需 key + proxy）

中文用 alloy/onyx/nova，**不像 Mimo 适合中文长段**。

## 公众号文章

| 坑 | 症状 | 修复 |
|----|------|------|
| 冒号 | 「有致命问题：一是贵」→ AI 味 | 全部改成逗号「有致命问题，一是贵」 |
| 错别字 | 「绑绑有余」非标准写法 | 标准成语是「绰绰有余」 |
| 核心论点重复 | 同一句话在 70 行间隔出现两次 | 一处展开论述，一处用「前面聊了这么多，归根结底就是...」做回环呼应 |

## beautiful-article

### reacticle d.ts props（按字母顺序）

| 组件 | 错误写法 | 正确写法 |
|------|----------|----------|
| `Summary` | `<Summary><p>...</p></Summary>` | `<Summary points={["...", "..."]} />` |
| `Quote` | `attribution="..." emphasis="..."` | `who="..." source="..."` |
| `Aside` | `tone="scope"` | `tone="note"` / `principle` / `capability` / `warning` |
| `Section` | 用 h3 标签当小标题 | `Section` 自带 `title` prop，或用 `<h3>` 包 `Subsection` |

### 主题

| 坑 | 修复 |
|----|------|
| 用户要求"避免红色" | freddie 主题（accent 是 `#241c15` 深棕近黑，**不是红色**）；或 press 主题（氧化血红 — 是红色，要避免）|
| freddie accent 看起来"沉闷" | 改用 `--mc-yellow: #ffe01b`（明黄）作局部高亮 |
| 想要 vignelli 风格但用户上一轮拒绝 | 改用 knuth（学术）或 freddie（暖白） |

### 文件系统

| 坑 | 症状 | 修复 |
|----|------|------|
| 路径含空格 | `/Volumes/My SSD/` | 所有命令必须双引号包围 |
| scaffold 启动工作区时 `source/` 已存在 | 报"目标目录已存在且非空" | 移动 source 到 /tmp → 重 scaffold → 把 source 移回 |
| 软链目标名重名 | mv 失败 | 删旧链 → 建新链 |
| 软链循环 | 用简化名建软链，源目录里又出现同名 | 用 native 名字（`20260618_xxx_视频演示_v1`）|

### 交付

| 坑 | 症状 | 修复 |
|----|------|------|
| `document.title` 是 "Beautiful Article" | 浏览器标签/PDF 显示默认名 | 改 `index.html` `<title>` 为文章标题 |
| Google Fonts link | 断网时降级 | 移除 `<link href="https://fonts...">`，让 freddie 主题 fallback 到 system serif |
| article.html 2.0 MB | 体积大 | 接受（gzip 1.1 MB，分享 OK）。瘦身需 tree-shake reacticle（不在本任务范围） |

## 环境特殊性

| 坑 | 环境 | 影响 |
|----|------|------|
| macOS 全局 NODE_ENV=production | 用户 macOS 15.7.5 | 所有 npm 命令需显式设 NODE_ENV=development |
| 移动硬盘路径含空格 | /Volumes/My SSD/ | 所有路径需双引号包围 |
| edge-tts 路径 | 装在 Hermes 运行时 Python /Users/chentao/.hermes-web-ui/desktop-runtime/hermes/0.16.0/mac-arm64/python/bin/edge-tts | 不在默认 PATH，但 pip show 能找到 |
| audio HTML element 默认 stream=False | 看不到 duration / 当前时间 | 改用 useAudioPlayer hook（已封装 stream + onended + autoadvance） |
| Vite 默认端口冲突 | 5173/5174 被视频项目占 | 自动找下一个空 port (5175/5176/...) |

## 发布渠道

| 坑 | 症状 | 修复 |
|----|------|------|
| 知乎需要登录 | curl/Playwright 拿不到知乎正文 | 如果需要发布知乎，用 lark-* skill 或手动发布 |
| 飞书知识库 | 依赖 lark-cli 配置 | 确认 lark-cli --as user 可用 |
| Chrome headless PDF 渲染 | 脚本找不到浏览器 | macOS 自带 Chrome：`/Applications/Google Chrome.app/Contents/MacOS/Google Chrome` |

## Phase 4b MP4 视频（新增，来自 text-to-video-pipeline）

| 坑 | 症状 | 修复 |
|----|------|------|
| mimo key 401 | `openai.AuthenticationError: Invalid API Key` | 检查 ~/.mimo_credentials 是否最新 key（52 字符）。降级用 edge-tts |
| HyperFrames transcribe bug | 拼 whisper-cpp 参数 `--dtw --suppress-nst ggml-tiny.en.bin` 报错 | 绕开：直接用 openai-whisper CLI，输出 JSON 自己转格式 |
| whisper small.pt checksum 错 | `RuntimeError: SHA256 checksum does not match` | 删 ~/.cache/whisper/small.pt 重下 |
| whisper small.en 翻译中文 | 中文音频被转成英文输出 | 必须显式 `--language zh` |
| HyperFrames lint root 缺 composition-id | 报 root_missing_composition_id / dimensions 错 | root div 必须有 data-composition-id + data-width + data-height |
| timeline id 不匹配 | `timeline_id_mismatch` | window.__timelines 名称 = root div data-composition-id |
| font 引用系统字体 | 报 `font_family_without_font_face` | 删 CSS 中 PingFang/Microsoft YaHei/Source Han |
| data-duration 太短 | 视频过早停止 | root duration = 音频时长 + buffer（3-5s） |
| TTS 试听文本含标点 | mimo 会念出全部文字，不自然 | 试听用 script_full.txt 前 2-3 句纯文本 |
| mimo voice name 用错 | 传 "mimo_default" 用错音色 | 用 "冰糖"/"苏打"/"茉莉"/"白桦" 确切名字 |
