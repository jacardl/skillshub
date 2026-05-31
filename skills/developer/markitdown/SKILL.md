---
name: markitdown
description: Microsoft 开源文件转 Markdown 工具（PDF/Word/Excel/PPT/图片OCR/音频转录/HTML/CSV/JSON/ZIP）。当用户说"转换文件为markdown"、"提取PDF内容"、"把Word转成文本"、"将PPT转Markdown"、"图片OCR识别"、"音频转写"、"批量转文件"时触发。markitdown 支持 LLM 图像描述和 Azure Document Intelligence 云端提取。
---

# MarkItDown

Microsoft 开源文件转 Markdown 工具，支持 20+ 格式，输出结构化 Markdown，适合 LLM 分析管道。

## 支持格式

| 格式 | 说明 | 可选依赖 |
|------|------|---------|
| PDF | 文本提取 | `[pdf]` |
| Word (.docx) | 段落/表格/链接 | `[docx]` |
| Excel (.xlsx/.xls) | 表格结构 | `[xlsx]`/`[xls]` |
| PowerPoint (.pptx) | 幻灯片文本 | `[pptx]` |
| 图片 | EXIF 元数据 + OCR | `[all]` |
| 音频 | EXIF + 语音转写 | `[audio-transcription]` |
| HTML | 结构化提取 | 内置 |
| CSV/JSON/XML | 文本格式 | 内置 |
| ZIP | 遍历内容 | 内置 |
| YouTube URL | 字幕转 Markdown | `[youtube-transcription]` |
| EPUB | 电子书 | 内置 |
| Outlook (.msg) | 邮件提取 | `[outlook]` |

## 安装

```bash
pip install 'markitdown[all]'          # 全量安装
pip install 'markitdown[pdf,docx,pptx,xlsx]'  # 按需安装
```

从源码安装：
```bash
git clone git@github.com:microsoft/markitdown.git
cd markitdown
pip install -e 'packages/markitdown[all]'
```

## CLI 用法

```bash
# 标准转换
markitdown path-to-file.pdf -o document.md

# 管道输入
cat file.docx | markitdown

# 列出已安装插件
markitdown --list-plugins

# Azure Document Intelligence 云端提取（高质量布局分析）
markitdown file.pdf -d -e "https://<endpoint>.cognitiveservices.azure.com/"

# Azure Content Understanding（结构化字段提取）
markitdown file.pdf --use-cu --cu-endpoint "<cu_endpoint>"
```

## Python API

```python
from markitdown import MarkItDown

md = MarkItDown()
result = md.convert("report.xlsx")
print(result.text_content)   # 纯文本
print(result.markdown)        # Markdown 格式
```

### 使用 Azure Document Intelligence

```python
from markitdown import MarkItDown

md = MarkItDown(docintel_endpoint="<document_intelligence_endpoint>")
result = md.convert("document.pdf")
print(result.text_content)
```

### 使用 LLM 图像描述（OCR + 视觉）

```python
from markitdown import MarkItDown
from openai import OpenAI

client = OpenAI()
md = MarkItDown(llm_client=client, llm_model="gpt-4o")
result = md.convert("screenshot.png")
print(result.text_content)
```

### Azure Content Understanding（结构化字段 YAML front matter）

```python
from markitdown import MarkItDown

md = MarkItDown(cu_endpoint="<content_understanding_endpoint>")
result = md.convert("invoice.pdf")
print(result.markdown)
# 输出含 YAML front matter:
# ---
# fields:
#   VendorName: CONTOSO LTD.
#   InvoiceDate: '2019-11-15'
# ---
```

### 细粒度 API（更安全）

```python
# 仅转换本地文件
md = MarkItDown()
result = md.convert_local("file.pdf")

# 转换 HTTP 响应
import requests
resp = requests.get("https://example.com/file.docx")
result = md.convert_response(resp)
```

## Docker

```bash
docker build -t markitdown:latest .
docker run --rm -i markitdown:latest < ~/your-file.pdf > output.md
```

## 安全注意事项

> [!IMPORTANT]
> MarkItDown 以当前进程权限执行 I/O。在不受信任的环境中使用时：
> - **优先使用 `convert_local()`** 而非 `convert()`，限制文件访问范围
> - 验证输入路径，阻止 `../../../etc/passwd` 等路径遍历
> - YouTube/远程 URL 功能会发起网络请求
> - ZIP 文件会遍历解压内部所有文件

## OCR 插件（markitdown-ocr）

独立插件，支持 PDF/DOCX/PPTX/XLSX 内嵌图片的 LLM OCR，无需额外 ML 依赖：

```bash
pip install markitdown-ocr openai
```

```python
from markitdown import MarkItDown
from openai import OpenAI

md = MarkItDown(
    enable_plugins=True,
    llm_client=OpenAI(),
    llm_model="gpt-4o",
)
result = md.convert("scanned.pdf")
print(result.text_content)
```

## 依赖项速查

```
markitdown              # 核心（内置：CSV/JSON/XML/EPUB/HTML/ZIP）
[pdf]        → pdfminer.six
[docx]      → python-docx
[pptx]      → python-pptx
[xlsx]      → openpyxl
[xls]       → xlrd
[outlook]   → extract-msg
[audio-transcription] → openai / whisper
[youtube-transcription] → youtube-transcript-api
[az-doc-intel] → azure-ai-documentintelligence
[az-content-understanding] → azure-ai-contentunderstanding
```

## 适用场景

- **文档预处理**：将 PDF/Word/Excel 转为 LLM 可读的 Markdown
- **数据提取管道**：批量转换文件做 RAG 或分析
- **图片 OCR**：截图、扫描件文字提取
- **会议记录**：音频转 Markdown 供 LLM 总结
- **知识库构建**：ZIP 批量导入文档
- **结构化提取**：Azure Content Understanding 提取发票/合同关键字段

## 限制

- 高保真排版转换不是主要目标，输出以文本分析为导向
- 视频文件需通过 Azure Content Understanding
- 无视频内置支持