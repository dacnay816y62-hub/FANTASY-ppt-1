# 脚本与检查

[返回首页](../README.md)

以下命令在仓库根目录执行。脚本不负责检索、概念创作或自动生成原生可编辑页面。

## 图片合并为 PPT

```bash
python scripts/merge_images_to_pptx.py ./slides ./exports/deck.pptx --fit contain
```

Python 包装器调用随包 Node 实现。Node 实现依赖宿主管理的 `CODEX_PRIMARY_RUNTIME_NODE_MODULES`，该目录中必须能解析 `@oai/artifact-tool`；请使用宿主支持的运行环境。文件按自然顺序排列，支持 PNG、JPG、JPEG、WebP，输出16:9页面。

`contain` 保留完整图片；`cover` 铺满但可能裁切。建议源图本身为16:9，避免留边。图片中的文字不会变为可编辑对象。

## 检查 PPT 结构

```bash
python scripts/inspect_pptx.py ./exports/deck.pptx --mode editable --check-fonts
python scripts/inspect_pptx.py ./exports/deck.pptx --mode image-only
```

`editable` 检查原生文字等结构条件，不代表所有对象均可编辑。字体检查对照当前系统字体，不保证接收者设备相同。该脚本主要使用 Python 标准库，字体检测可能依赖系统 fontconfig。

## 检查项目目录

```bash
python scripts/validate_project.py ./project --stage structure
python scripts/validate_project.py ./project --stage pilot --pilot-count 3
python scripts/validate_project.py ./project --stage final --mode editable
```

`--pilot-count 3` 只是示例：应按本项目代表页数填写。

必需文本：`project-truth.txt`、`analysis.txt`、`visual-dna.txt`、`outline.txt`；最终阶段增加 `qa.txt`。旧 `.md` 文件仍可读取，但会提示使用新格式。

大纲页号使用 `Slide 1` 或 `第 1 页`，从1开始、连续、不重复。`pilot-preview/` 放试排预览，`slides-preview/` 放最终逐页预览，`exports/` 放 PPTX。

## 检查范围

脚本验证文件存在、页号和页数、部分 PPT 结构及字体情况。它无法验证历史是否真实、设计是否高级、地图是否准确或预览是否与最终页面相符。这些仍需内容核对和实际渲染。
