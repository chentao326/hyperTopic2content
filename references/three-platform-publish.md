# 三平台发布工作流

Phase 6 的实操参考。适用于已完成公众号文章+横纵分析报告的项目，需要同时发布到知乎和飞书知识库的场景。

## 标准流程

1. 公众号（优先）：通过 wechat-oa-publisher skill 或手动发布半佛版/卡兹克版
2. 知乎：发布横纵分析报告（HTML版），带上话题标签
3. 飞书知识库：创建 wiki 节点并写入内容摘要+三平台交叉链接

## 知乎发布实操

```bash
# 1. 确认登录状态
zhihu whoami

# 2. 搜索合适的话题标签
zhihu search "半导体" -t topic -l 5

# 3. 将横纵分析报告 Markdown 转为 HTML
python3 -c "
import markdown
with open('报告.md') as f:
    html = markdown.markdown(f.read(), extensions=['extra', 'smarty'])
with open('/tmp/zhihu-article.html', 'w') as f:
    f.write(html)
"

# 4. 发布文章（标题不能太长，否则报「标题格式不正确」）
zhihu article "标题（简短有力）" "$(cat /tmp/zhihu-article.html)" -t 话题ID1 -t 话题ID2
```

注意：zhihu article 命令不支持更新已有文章。如需加参考文献或交叉链接，只能在发布时一并包含。

## 飞书知识库发布实操

```bash
# 1. 创建 wiki 节点
npx @larksuite/cli wiki nodes create --as user \\
  --params '{"space_id":"SPACE_ID"}' \\
  --data '{"node_type":"origin","obj_type":"docx","title":"文档标题"}' \\
  --format json
# 返回 node_token 和 obj_token

# 2. 写入内容（支持 markdown 格式）
npx @larksuite/cli docs +update --api-version v2 \\
  --doc "NODE_TOKEN" \\
  --command append \\
  --doc-format markdown \\
  --content "$(cat content.md)" \\
  --as user
```

## 三平台交叉引用

- 飞书知识库文档内：在内容开头/结尾加入公众号链接和知乎链接
- 知乎文章：发布时在正文末尾加入其他平台链接（发布后无法修改）
- 公众号：发布后不可编辑，交叉引用需在发布前加入

## 话题 ID 参考

| 话题 | ID |
|------|-----|
| 半导体 | 19557452 |
| 半导体产业 | 19815862 |
| 半导体行业 | 20775821 |
