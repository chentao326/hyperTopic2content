# Bundled Skills

hyperTopic2content 所依赖的子 skill。安装本仓库后，将这些目录复制或软链到 `~/.hermes/skills/` 即可。

## 已打包

| Skill | Phase | 安装方式 |
|-------|-------|---------|
| topic2content | Phase 4 B1 | 复制到 ~/.hermes/skills/ |
| hv-analysis | Phase 2 | 复制到 ~/.hermes/skills/ |
| khazix-writer | Phase 3 | 复制到 ~/.hermes/skills/ |

## 外部安装

| Skill | Phase | 获取方式 |
|-------|-------|---------|
| last30days-cn | Phase 1 | `npx skills@latest add last30days-cn -g` |
| video-pipeline | Phase 4 B2 | [github.com/chentao326/video-pipeline](https://github.com/chentao326/video-pipeline) |
| hottake-writer | Phase 3（半佛） | `npx skills@latest add hottake-writer -g` |
| beautiful-article | Phase 5 | `npx skills@latest add beautiful-article -g` |

## 一键安装

```bash
# 克隆本仓库
git clone https://github.com/chentao326/hyperTopic2content.git
cd hyperTopic2content

# 安装已打包 skill
cp -r bundled-skills/topic2content ~/.hermes/skills/
cp -r bundled-skills/hv-analysis ~/.hermes/skills/
cp -r bundled-skills/khazix-writer ~/.hermes/skills/

# 安装外部 skill
npx skills@latest add last30days-cn -g
npx skills@latest add hottake-writer -g
npx skills@latest add beautiful-article -g

# video-pipeline 单独克隆
git clone https://github.com/chentao326/video-pipeline.git ~/.hermes/skills/software-development/video-pipeline
```
