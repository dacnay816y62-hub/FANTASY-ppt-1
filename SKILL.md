---
name: ppt-image-deck
description: Create and improve Chinese spatial design proposal presentations for interior, architecture, hotel, residential, clubhouse, restaurant, retail, and cultural projects. Use for 设计方案PPT、空间提案、项目汇报、概念方案汇报 and editable or image-based PPT deliverables; connect project evidence to design decisions, create coherent visual assets, and verify the finished deck.
---

# 空间设计提案 PPT

把项目资料组织成有依据、有空间判断、可供讨论的设计提案。新做视觉提案默认先形成整页视觉稿，检验构图与图像表达，再准备无字独立素材、重建可编辑 PPT。按用户要求保留图片版、混合版和既有模板的选择。

当前用户确认的方向是 **简约、高级的品牌排版，设计师的汇报框架与推导**：以文化、概念、元素、设计手法和氛围建立方向；进入空间方案阶段后，再通过平面、空间、材质与陈设说明设计如何成立。完整提案包含用户指定版式的目录页，章节按阶段调整，具体见 [designer-report-framework.md](references/designer-report-framework.md)。

## 先确定任务范围

- 沿用会话中已明确的项目、受众、汇报阶段、比例、页数与视觉方向。修改既有 PPT 时先检查原文件，优先修复相关页面，不重新发明整套流程。
- 用户限定“效果图、平面图先不出，只考虑文字概念、设计手法和设计元素”时，采用**概念研究阶段**，后续同阶段测试沿用这一范围。先讲清元素依据、抽象特征、具体设计动作及希望形成的体验，不生成项目效果图、平面图或完整空间局部渲染，也不以缺少这些图判定未完成。文化、唯美氛围、材料特写及抽象元素演示仍可服务概念；若用户要求纯文字或全部不出图，则只写概念和手法。用户要求推进空间方案时再恢复平面与效果图。
- 用户要求“优化并测试”且未指定项目时，可选择一个明确标注的虚构项目完成小型样例。模拟资料用于测试判断和表达，不补造实际平面、面积、造价或运营结论。
- 已授权完成整套时，试做是内部质量检查，不是必须再次询问的许可关。用户明确要“先看几页”或某个关键选择确实无法合理判断时，才停在约定的节点。
- 输出 PPT 时读取并遵循当前 **Presentations** skill，包括模板路由、运行时、原生编辑、来源备注和逐页渲染要求。用户指定 HTML 时使用可用的 **html-spatial-deck** skill；不要用 HTML 代替所需 PPTX。

## 工作流

### 1. 从资料提炼设计判断

读取 [project-truth.md](references/project-truth.md)，在临时项目目录建立 `project-truth.txt`，区分 **FACT / JUDGMENT / PROPOSAL / UNKNOWN**。

在 `analysis.txt` 写清：这次汇报要让谁理解或选择什么。抓住最有影响的项目矛盾，形成：

> 已知条件或明确假设 → 使用上的问题/机会 → 设计动作 → 可展示的空间结果

例如，“入口直对安静席位”只有在图纸或现场可证实时才是事实；“错开入口视线以减少干扰”可以是设计建议。每个核心概念应落实为组织、边界、尺度、光、材料或使用方式，不能只靠“隐、境、雅”等词完成推导。

### 2. 组织页纲与视觉方向

读取 [outline-schema.md](references/outline-schema.md)，建立 `outline.txt`，每页用五个字段说明观点、文字、视觉证据、版式、资料属性。完整提案先读取 [designer-report-framework.md](references/designer-report-framework.md)，按指定目录母版和设计论证组织章节；目录对应实际内容，不机械增加章节过场。局部修改、单页模板和限定试页遵守任务范围。

包含空间方案的完整提案默认补齐 **当地文化分析、区位/地理位置图、效果图之前的对应平面图**。读取 [culture-site-plan.md](references/culture-site-plan.md)：文化依据必须支撑后续元素与空间，区位图说明真实位置与周边关系，平面先说明空间组织再展示对应效果图。概念研究阶段保留与设计有关的文化和区位判断，目录使用概念阶段章名，不安排平面、效果图或空白占位章节。内容要求不固定页数或版式；局部修改与限定试页遵守其范围，缺少资料时不伪造项目条件。

先选本项目值得解释的问题，再选分析表达。禁止默认安排“第一眼、第二眼”或“看见—停留—试衣”等固定体验流程；没有依据或新增判断价值的功能关系页直接删除。元素、边界、光或材料比较均只是可选表达，不替换成另一套必出章节。

读取 [visual-dna.md](references/visual-dna.md)，在 `visual-dna.txt` 定义字体、色彩、图像和版式。模板只是可选的表达方法，参考文件见下方；用户的品牌和参考优先。没有适合模板时自行建立方向。

读取 [font-system.md](references/font-system.md) 和 [typography-lock.md](references/typography-lock.md)，先定义文字角色，供视觉稿与 PPT 共用。封面展示字按构图决定，无统一字号上限；内页同角色保持稳定，不逐页缩字适配。

用户要求品牌提案感，或反馈内页字太大、排版太满时，读取 [brand-proposal-layout.md](references/brand-proposal-layout.md)，按实际参考与阅读场景重定内页字级、图幅和留白。不要用通用投影字号覆盖这个明确方向，也不要把“更丰富”误解为填满页面。

承接既有参考或返工时，先恢复可查的参考图与分析，将其落实为素材角色、背景质感、图像比例和叠层关系，再展开代表页。

制作文化、设计元素或设计概念的**氛围页**时，读取 [culture-concept-mood-templates.md](references/culture-concept-mood-templates.md)，查看其中用户指定的原图，从五类固定构图中按内容选用。保留图像组合、文字锚点与留白关系，替换项目素材与文案；不把氛围页统一排成侧栏说明配单张图片，也不要求每套用齐五类。此处优先检验唯美素材与图文共同构图，区别于承担推导的分析演示图。

用户提供行业标杆文件时，读取 [benchmark-selection.md](references/benchmark-selection.md)。先通览整套结构，再放大筛选具体页面，分别判断论证方法与视觉质量；不按公司名整套照收。把保留、需重排和排除的做法落实到本次页纲，避免只添加风格形容词。

多图项目概念页用与各图对应的简短概念词共同建立主题，保留已认可的图片，并以可编辑文字组织层级，见 [概念氛围模板](references/culture-concept-mood-templates.md)。完整提案默认以项目化的“设计愿景 + 谢谢 / THANK YOU”收尾，采用可辨识的氛围底图，不再默认用深化工作清单作末页；具体编辑范围见 [汇报框架](references/designer-report-framework.md)。

### 3. 先用整页视觉稿检验方向

按当前任务选能暴露不同排版风险的代表页，通常是封面、核心分析、视觉页；更短的任务可直接检查全部页面。用户重点测试排版时，用分析图、氛围拼贴或材料页检验信息层级、图文关系与节奏；不必先生成空间效果图。需要空间表达时再选择重点空间页和参照图，避免三页都是同一种大图布局。

概念宣言或停顿页在当前空间提案方向中默认有可辨识的氛围底图，文字与影像共同构图；纯色或轻微纸纹不能代替用户要求的底图。只有用户明确选择纯文字过场时才使用纯色版。

新提案或视觉重做时，读取 [layered-editable-workflow.md](references/layered-editable-workflow.md)，用图像工具先做代表页的完整画幅视觉稿，直接检验底纹、图像主次、叠层、分析表达和文字占位。整页稿是构图依据，不能当作可编辑成品；其中的文字和精确关系须在重建时核准。

代表页方向成立后，先把它们重建为 PPT 并渲染，确认视觉效果能保留，再按同一方向完成其余页面。允许分批推进，不要求先生成全套再统一拆层。已有明确模板或只改少量页面时，直接编辑并检查相关 PPT 页面。已授权制作则检查后继续，不增设确认关。

### 4. 选择素材与原生排版

按已确定的项目文字角色，用真实字体与 pt 值重建文本，不把图像稿的偶然字形大小当作字号规范。

以整页视觉稿为依据准备干净背景、摄影、意向和拼贴区域。文化、元素、材质和概念的氛围图片先从 **Pinterest 或其他网络来源**筛选，按美感、意境、分辨率及成组后的构图判断；找到能表达概念的合适图片就直接使用，不默认整套生图，不设生成比例。Pinterest 用于发现素材，尽量追溯原始页面；检索受限时换公开原始来源，不能虚称来自 Pinterest。真实文化证据与联想意向分清来源属性。缺少合适图片或需要特定图文留白时再用 **Image Gen** 补充。承担元素提炼、概念转译和空间策略推导的演示图使用 **Image Gen**，以材质、体积、形态或光影显示关系；文字、图注与少量圆点/方块锚点独立原生排版。不要因可编辑或实现方便，把概念演示降成线条、方框、箭头与文字拼装。只对需要透明边缘的素材做透明 PNG，不要求每个视觉元素都抠成图层，也不承诺无损自动拆图。

设计手法优先采用**可追溯的元素演化分析**：让原始线索、被提取的特征及设计变化在图像中形成对应，具体见 [element-evolution-analysis.md](references/element-evolution-analysis.md)。抽象用于归纳关系，不以孤立的石块、漂浮薄片或艺术雕塑代替推导。分析可为前后对照、连续演化或并行比较，步数与构图按内容决定；概念阶段保持关系示意，不补完整空间效果图。

- **Level A，默认**：标题、正文、标注、页码可编辑；概念演示图、摄影和空间图为独立图片，真实图纸使用原始文件或可靠矢量。图内物体不承诺拆分可编辑。
- **Level B**：复杂拼贴作为图片，关键文字独立可编辑；说明哪些视觉内容已合成。
- **Level C**：用户需要的整页图像版，明确非文字可编辑。不要因此强行改成 Level A。

用户愿意后续手调时，优先保住图像尺度、裁切、留白和叠层；可采用 Level B 的复杂合成区配独立文字，不因程序容易实现就改成等大卡片。保留用户要求的可编辑部分，并在交付前修好可见的丑页，不能把手调意愿当作降低成品标准的理由。

后续空间图继承材料、构造和家具语言；同一空间锁定其位置关系。焦段、机位、景别按每页要说明的内容调整，不能用“镜头相同”代替一致性。

制作效果图章节时，先明确对应平面及其资料属性，再确定机位与空间不变项；在该组效果图之前排入平面说明。地图与平面按真实地理或原始图纸保持准确，可用原生线条与矢量；不要把抽象分析的 Image Gen 路线用于重画准确地图、尺寸或未知建筑布局。

空间图与文化意向图可调用图像工具。真实图纸、准确数据图表和有依据的工程连接关系按 Presentations 的规则制作，不用生成图冒充精确证据；未知空间仅作概念意向，不画得像完成的测绘或施工成果。所有生成中间文字，包括提示词、设计记录与 QA，使用 `.txt`；`.md` 仅用于已安装技能资源。

### 5. 检查成品并交付

读取 [quality-checklist.md](references/quality-checklist.md)。检查每页观点是否有依据，文化和材料是否落实到空间动作，结论是否回应开场。逐页查看最终 PPT 的渲染图，并与对应整页视觉稿比较，修复层次丢失、文字断行、溢出、裁切和无意重叠；montage 仅用于整套节奏检查。

可在技能目录运行：

```bash
python scripts/validate_project.py <project-dir> --stage final
python scripts/inspect_pptx.py <output.pptx>
```

项目校验可加 `--pilot-count N` 检查本次选定的代表页数量，不固定要求三页；Level C 加 `--mode image-only`。这些脚本只辅助检查，不证明内容真实、设计成立或视觉通过。按用户所需交付最终 PPTX；用户要求测试展示时可附少量最终预览。源文件和素材包按需提供。按当前环境保存最终文件；技能自身的维护文件与项目交付物分别处理。

## 临时项目目录

```text
image-ppt/{project-slug}/
  source/
  project-truth.txt
  analysis.txt
  visual-dna.txt
  outline.txt
  source-notes.txt
  prompts/
  visual-drafts/
  pilot-preview/
  assets-generated/
  slides-preview/
  exports/
    {project-slug}-editable-cn.pptx
  qa.txt
```

`visual-drafts/` 保存整页视觉探索，`pilot-preview/` 保存代表页 PPT 渲染，`slides-preview/` 保存最终 PPT 渲染；不要用前者冒充后两者。短任务的记录可以合并，避免为简单修改制造文档负担；调用项目校验脚本时按其约定提供相应文件。外部资产与非平凡来源事实在 PPT 讲者备注中记录 `[Sources]`，生成图记录其概念属性。

## 按需参考

- 阶段组织、资料不足、返工：[workflow-rules.md](references/workflow-rules.md)
- 黑暗文化目的地酒店：[hotel-01](references/templates/hotel-01-dark-cultural-destination.md)
- 黑金住宅与样板间：[residential-01](references/templates/residential-01-dark-luxury-sample-room.md)
- 浅色东方园林住宅：[residential-02](references/templates/residential-02-light-oriental-garden-lifestyle.md)
- 现代滨海极简住宅：[residential-03](references/templates/residential-03-modern-coastal-minimal.md)
- 东方植物、器物与商业生活方式：[commercial-01](references/templates/commercial-01-oriental-botanical-brand-manual.md)

只读当前任务有用的参考；任何模板的页数、色彩、符号和示例概念都不应覆盖项目事实或用户要求。
