# macOS WeasyPrint PDF 生成环境配置

## 环境

- macOS 15.7.5 (Apple Silicon)
- Homebrew 安装于 /opt/homebrew

## 依赖安装

```bash
# 1. 系统库（Pango 渲染引擎 + GObject）
brew install pango gobject-introspection

# 2. Python 包 —— 注意不要装到系统 Python 3.9
# 系统 Python 3.9 的 weasyprint v66 无法加载 macOS .dylib 文件
# 用 Hermes 运行时 Python 3.12（已预装 weasyprint v69+）
```

## 执行命令

```bash
DYLD_LIBRARY_PATH=/opt/homebrew/lib \
  /Users/chentao/.hermes-web-ui/desktop-runtime/hermes/0.16.0/mac-arm64/python/bin/python3 \
  scripts/md_to_pdf.py input.md output.pdf --title "标题" --author "作者"
```

关键点：
- `DYLD_LIBRARY_PATH` 必须指向 Homebrew 的 lib 目录，否则 Python 找不到 libgobject 和 libpango
- 只能用 Hermes 运行时的 Python 3.12，系统 Python 3.9 的 weasyprint 版本太旧

## 验证环境

```bash
# 确认 pango 库存在
ls /opt/homebrew/lib/libgobject-2.0*.dylib
ls /opt/homebrew/lib/libpango-1.0*.dylib

# 确认 weasyprint 可导入
DYLD_LIBRARY_PATH=/opt/homebrew/lib \
  /Users/chentao/.hermes-web-ui/desktop-runtime/hermes/0.16.0/mac-arm64/python/bin/python3 \
  -c "from weasyprint import HTML; print('OK')"
```

## 常见错误

| 错误 | 解决 |
|------|------|
| `cannot load library 'libgobject-2.0-0'` | 缺 pango：`brew install pango gobject-introspection` |
| 装了 pango 仍报错 | 检查 Python 版本：系统 py3.9 的 weasyprint v66 不兼容，用 Hermes 运行时的 py3.12 |
| `pip install weasyprint` 装到了错误位置 | `which pip` 确认路径；Hermes 运行时 Python 已自带 weasyprint |
