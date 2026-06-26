# Cron 模式下的文章自检替代方案

当 hyperTopic2content 在 cron 定时任务环境下运行时，`execute_code` 被安全策略阻止（`BLOCKED: execute_code runs arbitrary local Python in cron mode`），无法使用 Python 脚本做 L1 自检扫描。以下是在 cron 模式下完成 khazix-writer L1-L4 自检的替代方案。

## 核心原则

cron 模式下可用工具：`search_files`、`read_file`、`patch`
cron 模式下不可用：`execute_code`（任意 Python）

所有自检通过常规搜索/替换工具完成。

## L1 硬性规则扫描（search_files）

```python
# 实际执行方式（非 Python，直接调工具）：
# 禁用词扫描
search_files(pattern="说白了", path="<article_path>", output_mode="count")
search_files(pattern="意味着什么|这意味着", path="<article_path>", output_mode="count")
search_files(pattern="本质上|换句话说|不可否认", path="<article_path>", output_mode="count")

# 禁用标点扫描
search_files(pattern="：", path="<article_path>", output_mode="count")  # 冒号
search_files(pattern="——", path="<article_path>", output_mode="count") # 破折号
search_files(pattern="[\"\"\u201c\u201d]", path="<article_path>", output_mode="count") # 双引号

# 注意：search_files 会在参考来源区域、作者信息区匹配到冒号
# 这些区域不需要修复。确认具体位置用 context=1 参数：
search_files(pattern="：", path="<article_path>", output_mode="content", context=1)
```
然后逐条用 `patch` 修复正文中的违规（body 部分），参考来源部分的冒号/破折号保留。

## L1-L4 内容检查

- L1 — 通过 `search_files` + `patch` 修复硬性规则
- L2-L4 — 通过 `read_file` 通读全文，凭上下文判断风格一致性、内容质量和活人感。cron 模式下只有 AI 自身的判断力可用，没有 Python 脚本的自动化检查

## 限制

- 无法做精确的字符数统计（被 blocked 的 execute_code 才能做）
- 无法做复杂的正则匹配和替换
- 建议在 cron 模式下优先确保 L1 硬性规则（最容易被自动化检查到），L2-L4 人工判断
