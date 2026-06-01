# 案例库更新说明

## 更新目标

把最新高质量案例同步到本地，便于后续补充 prompt 脚手架和参考图素材。

## 当前重点来源

- OpenAI 官方图片生成文档
- OpenAI 官方 prompting guide
- `EvoLinkAI/awesome-gpt-image-2-prompts`
- `YouMind-OpenLab/awesome-gpt-image-2`
- X 上最近几天的高热案例
- 微信文章标题线索

## 使用脚本

```bash
python scripts/sync_case_sources.py
```

默认会把原始文件和整理后的索引写到：

- `references/cache/raw/`
- `references/cache/normalized/`

## 更新节奏建议

### 模型刚发布的前两周

- 每天更新一次

### 稳定期

- 每周更新 1-2 次

## 更新后人工要做的事

1. 看新增案例都集中在哪些场景。
2. 只挑“可复用”的案例进入主表。
3. 每个新增场景至少补一条 prompt 骨架。
4. 必要时补参考图样本。
