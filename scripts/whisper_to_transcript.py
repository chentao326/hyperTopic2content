#!/usr/bin/env python3
"""whisper JSON → HyperFrames transcript.json 转换器。

用法：
    python3 whisper_to_transcript.py <whisper.json> <output.json>

示例：
    whisper audio.mp3 --model small --language zh --output_format json --output_dir .
    python3 whisper_to_transcript.py audio.json pd-video/transcript.json
"""
import json
import os
import sys
from pathlib import Path


def convert(src_path: str, dst_path: str) -> int:
    """转换并返回词数。自动创建输出目录。失败时抛异常。"""
    # 自动创建输出目录
    dst_dir = Path(dst_path).parent
    os.makedirs(dst_dir, exist_ok=True)

    # 读 whisper JSON
    try:
        with open(src_path, "r", encoding="utf-8") as f:
            d = json.load(f)
    except FileNotFoundError:
        print(f"错误: 找不到输入文件 {src_path}", file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as e:
        print(f"错误: JSON 解析失败 {src_path}: {e}", file=sys.stderr)
        sys.exit(3)

    # 提取词级时间戳
    words = []
    segments = d.get("segments", [])
    if not segments:
        print("警告: whisper JSON 中无 segments", file=sys.stderr)
        return 0

    for seg in segments:
        for w in seg.get("words", []):
            text = w.get("word", "").strip()
            if not text:
                continue
            try:
                start = round(w["start"], 3)
                end = round(w["end"], 3)
            except KeyError as e:
                print(f"警告: 词缺少时间字段 {e}，跳过: {w}", file=sys.stderr)
                continue
            words.append({
                "id": f"w{len(words)}",
                "text": text,
                "start": start,
                "end": end,
            })

    # 写 HyperFrames 格式
    try:
        with open(dst_path, "w", encoding="utf-8") as f:
            json.dump(words, f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"错误: 无法写入 {dst_path}: {e}", file=sys.stderr)
        sys.exit(4)

    if words:
        print(f"已转 {len(words)} 个词到 {dst_path}")
        print(f"首词: {words[0]}")
        print(f"末词: {words[-1]}")
        print(f"总时长: {words[-1]['end']:.2f}s")
    else:
        print("警告: 未提取到任何词", file=sys.stderr)
    return len(words)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__, file=sys.stderr)
        sys.exit(1)
    try:
        n = convert(sys.argv[1], sys.argv[2])
        sys.exit(0 if n > 0 else 2)
    except Exception as e:
        print(f"未预期错误: {e}", file=sys.stderr)
        sys.exit(5)
