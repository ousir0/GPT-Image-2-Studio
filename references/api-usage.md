# API 使用说明

这个 skill 走的是 OpenAI 兼容图片接口。

如果你有自己的接入层文档，也可以把它补充到这个 skill 的私有工作流里。

## 1. 鉴权

这里用的是标准 API Key。

建议环境变量：

```bash
export OPENAI_BASE_URL="https://api.openai.com/v1"
export OPENAI_API_KEY="YOUR_API_KEY"
```

脚本会自动读取：

- `OPENAI_BASE_URL`
- `OPENAI_API_KEY`

## 2. 两个接口

### 文生图

- `POST /v1/images/generations`

### 图片编辑

- `POST /v1/images/edits`

## 3. 当前建议

- 默认模型用 `gpt-image-2`
- 当前稳定可控字段优先用：`prompt`、`model`、`n`、`response_format`
- 如果需要本地直接落盘，优先 `response_format=b64_json`
- 如果只是想拿到公网图地址，使用 `response_format=url`

## 4. 调试命令

文生图：

```bash
python scripts/gpt_image2_api.py generate \
  --prompt "为一家未来感 AI 公司做一张蓝绿色科技风 PPT 封面图，预留标题区" \
  --outdir ./tmp/gpt-image-demo
```

改图：

```bash
python scripts/gpt_image2_api.py edit \
  --prompt "保留主体构图，把画面改成赛博朋克夜景风格" \
  --image ./input.png \
  --outdir ./tmp/gpt-image-edit-demo
```
