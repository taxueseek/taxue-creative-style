---
name: taxue-creative-style
description: >
  踏雪影像风格引擎。四种能力：①按开放风格库出图（笔意水墨、留白海报、城市建筑、治愈插画、东方古典、氛围实验、写实摄影、概念海报、照片转艺术，以及独立语法：剪纸纸艺、皮影偶戏、釉面器物、纸本档案、美术片媒介；金融隐喻走 F8-V8 或纪念碑参考模板）②优化任意已有提示词（七维诊断打分+修复+注入踏雪DNA）③元提示词创作（任意需求从零构建精确提示词，按主题路由到独立语法，不锁死在 9 个家族）④学习用户偏好。子技能路由：个人 IP 插画、民国漫画杂志、面向领导生图、图片反推、节气档案全书、正宗艺术门类（见正文 §0）。触发：踏雪风格、taxue style、签名风格、文人水墨、上美影、剪纸、染色剪纸、窗花、皮影、木偶、青花瓷、年画、折纸、赛璐璐、纸本档案、节气海报、纸雕、水墨城市、概念海报、踏雪寻仙、层叠城市、3D书法、金石印象、篆刻、器物禅意、赛博东方、提示词优化、帮我写提示词、元提示词、出图、生成图片、帮我画、人物锁定卡、陶瓷素材图、中式纹样素材。
---

# Taxue Creative Style — 踏雪创意风格

## 0. 本质与模式路由

**第一性原理定义**：本 skill 是一套「风格化图片创作」体系。输入任意意图，输出模型能精确执行的提示词。输出质量 = 意图识别精度 × 风格模板精度 × 参数化完整度 × 依据反馈持续改进。

**体系分层（治理视角，对外介绍见 `references/taxonomy.md`）**：①资产层 = 开放注册的风格卡（现 14 家族 77 变体；家族是索引不是上限）；②组合层 = 参考模板（母题/单件范式/技法包/批量架构/人物场面，不占变体号）；③方法层 = 三条管线 + 出图封装与自检；④治理层 = 台账 + 偏好 + 检查器；⑤生态层 = 子技能。用户问「有哪些风格」时按独立视觉语法回答，不按「第几层」。独立判定与新增流程见 `references/style-independence.md`。

**加载协议（先读本文件，再按需读 references，禁止一次全读）**：

| 场景 | 必读文件 |
|------|---------|
| 模式一按家族出图 | 对应家族文件（§1 速查表末列）+ 出图时读 imagegen-routing.md + prompt-craft.md（只读封装/尺寸/自检段） |
| 模式二提示词优化 | optimize-pipeline.md（含七维诊断 + 修复块表） |
| 模式三元提示词创作 | create-pipeline.md |
| 封面 / 头图 / banner | cover-constraints.md |
| 出图前 | imagegen-routing.md（选宿主 + 尺寸）+ prompt-craft.md（封装 + 比例 + 自检） |
| 胶印 / 专色 / Riso / 单色双色印刷封面 | 路由 `taxue-poster-studio` 印刷模式；本库家族模板不因此改写 |
| 任务类型 / 锁定清单 / 多参考角色 | task-constraints.md（凡涉参考图、局部编辑、系列、产品/电商，先判任务类型再动笔） |
| 跨模型方言 / 视频关键帧 | model-dialect.md（用户点名其他模型、跨模型一致或静帧转视频时） |
| 妖兽 / 神兽 / 异兽母题 | beast-myth.md（东方三档 + 西式生物：狼人/吸血鬼/兽人/美人鱼/西方龙；先定档再选家族适配） |
| 刺绣 · 混合媒介技法 | embroidery-illustration.md（彩锦绣肖像 / 苏绣肖像 / 实景×2D涂鸦；介质优先、身份保留） |
| 人物一致性 / 角色锁定 / 人物取扱说明书 | character-lock-sheet.md（人物锁定卡：先按 task-constraints 判任务类型，再按卡制作身份锚点资料板） |
| 人物场面 / 雅士仕女 / 背影 / 倚栏 / 时装人像 | character-scene.md（场面语法：先定人在空间里做什么，再套家族媒介；与锁定卡分工：场面=在做什么，锁定卡=这是谁） |
| C4D 陶瓷素材 / 中式纹样素材图 | motif-ceramic-asset.md（素材卡：工艺语法固定、母题笔意词表、描边色随主题推演） |
| 交付后记录 | memory-protocol.md（归档 + 偏好双写） |
| 出图验证后状态回填 | verification-ledger.md（状态/证据/下一步，三处同步） |
| 场景快捷推荐 | scenario-pack.md |
| 主题未指定风格 | theme-router.md（九类主题 → 主风格+备选；点名皮影/剪纸/年画/人物场面先看此表） |
| 新风格该不该独立 | style-independence.md（四问打分，≥3 分独立成家族） |
| 对外介绍 / 体系说明 | taxonomy.md（开放注册表、表现族、五变量语法、77 变体口径） |
| 批量系列 / 品牌手册 / 彩虹色相 | brand-manual-visual.md（踏雪化系列色相纪律） |
| 旧编号引用 | legacy-migration.md |

**家族文件读取**：选家族后读对应家族文件，**先读「变体索引」选变体，再读选中变体段**，禁止整文件通读。出图自检时对照风格卡片禁忌逐项勾掉。

**四种模式（MECE 划分，可串联执行）**。封面不是第五种模式，是叠在任一家族上的约束档（cover-constraints.md）。

| 模式 | 输入 | 输出 | 触发判断 |
|------|------|------|---------|
| 一：风格出图 | 主题 + 选定风格家族 | 完整提示词 + 成图 | 用户要「踏雪某风格画 X」 |
| 二：提示词优化 | 用户已有的任意提示词 | 优化版提示词 + 逐条变更说明 | 用户拿来一段提示词要改进 |
| 三：元提示词创作 | 任意需求（一句话到一段描述） | 从零构建的完整提示词 + 成图 | 用户要「写个提示词」「帮我画」且无风格指定 |
| 四：学习记忆 | 使用记录 / 用户反馈 | 更新的偏好档案 | 完成出图后自动记录；用户说「记住」「以后都」时显式更新 |

串联规则：模式二/三产出提示词后，默认接出图验证（除非用户只要文本）。模式四贯穿始终，静默执行。用户要「封面 / 头图 / banner」时，先走模式一选家族，再叠加 cover-constraints.md 约束档（文字槽留空、安全边距）。

**路由决策顺序**：
1. 读 `memory/user-preferences.md`，查用户历史偏好（若存在）。表格里带「（示例）」的行一律忽略
2. 判断模式（上表）；封面只加约束档，不另开模式
3. **子技能路由（先于家族匹配）**：用户需求命中以下场景时，路由到对应子技能，不强行套本库家族：
   - **个人 IP / 卡通形象 / 形象一致性插画** → `taxue-ip-illustration`（形象基底→风格化变体→场景化应用。管「同一个角色在不同场景长得统一」，不是头像成图）
   - **一张可过 85 分、缩略图可认的 1:1 媒介头像** → `taxue-avatar-studio`（纸本编辑头像：圆形安全区、身份锚点、媒介质感、85/100 评测协议。管「把单个角色/宠物做成好看且不裁坏的方圆头像」，与形象一致性不同轴）
   - **民国漫画 / 月份牌 / 鲁迅排版 / 苏式海报 / 老上海复古** → `taxue-minguo-comic`（民国杂志风格系统）
   - **甲方黑话 / 五彩斑斓的黑 / 面向领导 / 需求转译** → `taxue-zhongyizhong`（中译中：把领导的中文黑话翻译成 AI 能画出来的中文提示词，交得了差、守得住底线）
   - **一张图 → 多风格/多视角/多世界观/多美学的系列变体** → `taxue-vanxiang`（踏雪万象，独立技能：核不变，七轴可变）
   - **本地图片/截图 → 反推提示词（复刻版 + 踏雪化两件套）** → `taxue-image-reverse`（图片反推：七维拆解 + 家族归类 + 归档双写）
   - **抽设计系统 / GPT Image 2 或 Seedream 5.0 Pro 可粘贴词 / 锁皮换槽众产** → `taxue-prompt-compiler`（生图编译器：不吞并本库家族；要踏雪风时先取家族模板再回本编译器编方言）
   - **生视频 / 活照片 / 把静帧做成镜头** → 先走本技能出第一帧，再交 `taxue-photo-studio/sub-skills/moving-image`（只编运动，不改介质）
   - **传统艺术门类：国画/岩画/雕塑/脸谱/工艺美术/民间美术** → `taxue-artist`（踏雪艺术家；正宗门类还原与本库踏雪化互不替代。本库 F10–F14 是踏雪化压缩卡，不是正宗工艺全书）
   - **完整节气推演 / 解释矩阵 / 开放编辑视觉全书** → `taxue-solar-polaroid`（本库 F13 只接「要一张档案图/物证快照」）
   - 子技能输出同样遵循本 skill 的踏雪 DNA、出图路由（imagegen-routing.md）、比例建议（prompt-craft.md）、归档双写（memory-protocol.md）。点名胶印/专色/Riso/单色双色印刷封面时，交 `taxue-poster-studio` 印刷模式，不把印版合同套进家族模板
4. 模式一 → 走家族匹配（§1）；未点名风格时先读 theme-router.md 再打开对应家族文件。模式二 → 读 optimize-pipeline.md；模式三 → 读 create-pipeline.md
5. 出图封装（prompt-craft.md）→ 出图（imagegen-routing.md）→ 自检（prompt-craft.md）→ 记录（memory-protocol.md）

---

## 1. 风格库（14 家族，77 个变体）

先定家族再定变体。家族数量开放，新增走 `style-independence.md`。**状态列决定可用性**：✅ 已验证（体系内出图通过，可默认）｜无标注 = 默认变体（模板已固化、来源已验证——外部发布、多平台出图、用户提供或早期迭代固化；可默认路由，不因未在本体系复验而受限，对外不得自称已验证）｜⚠️ 实验、🔶 测试中（点名才用，禁止默认路由与场景包推荐）。全部变体的验证状态、证据与下一步的单一真源 = verification-ledger.md；任何状态变更必须三处同步（家族文件索引+正文状态行、本速查表状态列、验证台账）。

**家族速查**（详细模板在各家族文件，选中后读对应文件）：

| 家族 | 适用主题 | 变体 | 默认比例 | 文件 |
|------|---------|------|---------|------|
| F1 笔意水墨 | 孤寂人物、水墨美女、文人雅士、水墨背影、猫、线舞猫、实验混搭、宋画、飞天、赛博国潮、写意油画微景观、墨迹微缩世界、极枯古物、踏雪寻仙、赛博东方（静谧） | A、P、Q1、Q2、W、Y✅、Z⚠️、AA⚠️、AE🔶、AF、AG、F1-AH🔶、F1-TX、F1-CO、F1-YS、F1-BY | 竖 3:4（F1-TX 例外 2:3） | style-library/F1-ink-wash.md |
| F2 留白海报 | 节日、概念、书法字、隐喻、国潮、信息图、欧普线描、叠纸文字、3D书法、篆刻印章 | B、E、F、H、I、F2-K⚠️、AB⚠️、F2-OP✅、F2-AC🔶、F2-3D、F2-JS | 竖 3:4（F2-OP 2:3 / F2-3D 16:9 / F2-JS 1:1 例外） | style-library/F2-blank-poster.md |
| F3 城市建筑 | 城市卡、纸雕大场景、层叠城市地标 | C、O、F3-LC | 横 4:3（LC 水墨版 3:4、夜景版 16:9） | style-library/F3-city.md |
| F4 治愈插画 | 日常小物、动物、温馨场景、儿童绘本手账、橡皮章版画 | G、J、R、K、F4-RB | 方 1:1 | style-library/F4-healing.md |
| F5 东方古典 | 仕女、倚栏闲立、琴案雅集、剪纸、复古杂志、仙侠、日式时尚插画、仿真绣、彩锦绣、多层剪纸景深、绢本工笔仕女、民国月份牌 | L、M1、M2、M3、M4、N、AC⚠️、AD、F5-AE🔶、F5-AF🔶、F5-DC、F5-DY、F5-MP、F5-YL、F5-QS | 竖 3:4 | style-library/F5-oriental.md |
| F6 氛围实验 | 黑暗行者、符号雕塑 | D、X | 竖 3:4 | style-library/F6-atmosphere.md |
| F7 写实摄影 | 纪实、胶片、CCD、影棚、环境编辑人像、高速运动、非遗器物微距、器物禅意静物 | S、T、U、V、H、F7-AE🔶、F7-QW、F7-ED | 按变体 | style-library/F7-photography.md |
| F8 概念海报 | 文字/词语/短句的视觉化、词义隐喻、高级概念海报 | V8✅ | 横 5:2 | style-library/F8-concept-poster.md |
| F9 照片转艺术 | 日常照片/废片 → 诗意手绘/抽象编辑/涂鸦/赛璐璐/皮影 | R1、R2、R3、R4、R5 | 竖 3:4 | style-library/F9-photo-art.md |
| F10 剪纸纸艺 | 染色剪纸、窗花透光（与 F5 剪纸旧卡分工见家族文件） | F10-ST、F10-WH | 竖 3:4 | style-library/F10-papercut.md |
| F11 皮影偶戏 | 皮影戏台、木偶定格（点名皮影禁止再走 F5-M1 混卡） | F11-PY、F11-MU | 横 16:9（MU 4:3） | style-library/F11-puppetry.md |
| F12 釉面器物 | 青花釉面、器物组字 | F12-QH、F12-BX | 竖 3:4 | style-library/F12-glaze.md |
| F13 纸本档案 | 物证档案卡、即时成像物证（全书仍走 solar-polaroid） | F13-AR、F13-PL | 竖 3:4 | style-library/F13-archive.md |
| F14 美术片媒介 | 木版年画、折纸构造、赛璐璐原创（照片转赛璐璐走 F9-R4） | F14-YZ、F14-ZZ、F14-SM | 按变体 | style-library/F14-animation.md |

**编号纪律**：H 与 K 均有重号——F2-H（招聘海报）≠ F7-H（高速运动）；F2-K（国潮连字）≠ F4-K（绘本手账）。按家族编号区分，禁止混用。

**签名风格并入**（2026-08-17）：原独立「taxue-signature-style」7 种签名风格已吸纳进本库：S2→F3-LC、S3→F5-M2（增强）+F5-DC、S4→F1-TX、S5→F2-3D、S6→F2-JS、S8→F7-QW、S9→F1-CO。**S1（色域水墨）与 S7（金融隐喻）未纳入**：验证后已裁撤，不再有对应变体；金融隐喻主题走 F8-V8 或 references/geometric-monument-poster.md 参考模板。默认模板按本库已验证语法重写（单段可执行句，禁止豆包式【气质】长散文）。外部出图样图见 references/gallery/（旧效果基准，非本体系标准）。状态 = 默认（来源已验证语义，非本体系 ✅）。

**主题默认映射**（无历史偏好时使用；细表见 theme-router.md）：概念/人生隐喻 → F8 或 F2；城市 → F3；猫 → F1 或 F4；美女/回眸 → F1-P 或 F5-L；雅士/书生/案前 → F1-YS 或 F5-QS；仕女闲立/倚栏 → F5-YL；背影 → F1-BY；时装人像/蓝调 → F7-ED；人物场面未点名媒介 → 先读 character-scene.md 再套家族；**剪纸** → F10（染色/窗花）或 F5-M2/DC（极简红剪影/多层）；**皮影** → F11-PY（禁止 F5-M1）；**木偶** → F11-MU；**年画** → F14-YZ；**折纸** → F14-ZZ；**赛璐璐原创** → F14-SM（照片转才走 F9-R4）；**青花/釉面** → F12-QH；**器物组字** → F12-BX；**节气物证/档案卡** → F13-AR（完整节气组图走子技能）；即时成像物证 → F13-PL；纸雕 → F3；刺绣 → F5-AE / F5-AF（🔶 点名才用）；藏品微距 → F7-AE（🔶）；文人器物 → F7-QW；写实 → F7；节日海报 → F2；篆刻 → F2-JS；3D 书法 → F2-3D；照片转艺术 → F9；绘本手账 → F4-K；只说「踏雪风格」未指定 → 先读 theme-router 再读偏好默认（当前 F8-V8），无偏好才回落 F1-A。**禁止把实验变体（F1-Z / F1-AA / F2-K / F2-AB / F5-AC）或测试中变体（F1-AE / F1-AH / F2-AC / F5-AE / F5-AF / F7-AE）当作未指定时的默认。**

**通用 DNA 原则（纸底、浅底家族的默认气质；满构图 / 灯屏 / 釉面 / 年画 / 摄影按各家族量化豁免留白百分比）**：
1. **留白第一**（浅底家族）：大面积空白是构图主体，不是空缺。F6 深底、F5-M3 影棚、F11 灯屏、F14-YZ 年画满幅不写留白百分比
2. **克制**：少即是多，宁意犹未尽不一览无余
3. **文字即设计**：中文字是视觉元素，非附属说明
4. **纸感优先**：宣纸肌理、印刷颗粒优于数字光泽（写实家族除外）
5. **概念深度**：捕捉本质而非图解表面
6. **色彩纪律**：受限色板，单一强调色常已足够
7. **文字纯净**：凡画面含指定文字，正文用自然语言写明「画面中除[指定文字]外不出现任何其他文字与标点，[指定文字]原样呈现不加标点，无任何水印、日期、签名」，不加「负面」标签

**家族用法**：选家族后读对应家族文件，**先读「变体索引」表选变体，再读选中变体段**（Best for → 模板 → 量化 → 槽位 → 状态），禁止整文件通读。出图自检时对照风格卡片禁忌，逐项勾掉才算过关。

---

## 2. 硬约束清单（交付前逐项核对，缺一即不合格）

1. **缺比例建议 = 交付不完整，禁止交付**（判断规则见 prompt-craft.md）
2. **交付完整性 6 项**：优化版提示词 / 建议比例 / 变更说明 / 矛盾扫描结果 / 归档+偏好双写 / 出图验证待办（optimize-pipeline.md）
3. **输出前五查 + 矛盾扫描关卡 + 机械核对**：形态/标点/可执行性守恒、改动量匹配、变量最小化、比喻具象化、比例建议、矛盾扫描（optimize-pipeline.md 步骤 1.5，十二类类型学，严重矛盾直接修复，轻微矛盾保留并指出）；原句保留率 ≥90%（打磨）/ ≥80%（补全），矛盾修复句豁免
4. **出图后必自检**：盲写画面实际内容再对照量化规格；失败只修一项；同一项连续 2 次失败即停（prompt-craft.md）
5. **实验 / 测试变体门**：⚠️ 实验 F1-Z / F1-AA / F2-K / F2-AB / F5-AC、🔶 测试中 F1-AE / F1-AH / F2-AC / F5-AE / F5-AF / F7-AE，点名才用，禁止默认路由、禁止场景包推荐
6. **验证待办必附**：本会话无生图工具时，交付必须附「验证待办」并写明原因，禁止假装已出图、禁止静默交付（imagegen-routing.md 第 5 条）
7. **归档 + 偏好双写 + 状态三处同步**：每次交付必须同时写本地归档版本记录与 user-preferences.md 偏好字段；出图验证后必须同步家族文件状态、SKILL §1 速查表、verification-ledger.md（memory-protocol.md）
8. **模板维护硬规则**：已验证变体只许补负向、参数化硬编码、拆冲突，禁止以「优化」名义稀释已验证约束（prompt-craft.md）
9. **语言形态守恒 + 原句优先**：优化 ≠ 重写，能改词不改句（optimize-pipeline.md）
10. **枚举不进正文**：MECE 枚举是自检逻辑，禁止整段写进 prompt 正文，正文只留一句推演指令（create-pipeline.md）
11. **可执行性硬规则**：禁止把「踏雪审美 / 踏雪 DNA / 踏雪留白 / 踏雪纸感 / 踏雪化」等内部术语原样写进交付给生图模型的 prompt；必须展开为可执行视觉描述（brand-manual-visual.md 零节）
12. **色板按风格选择**：没有单一“踏雪参考色板”；必须按所选家族/场景选色并写具体 HEX，禁止用水墨五色替代全库（prompt-craft.md）

---

## References

| 文件 | 用途 |
|------|------|
| `references/style-library/F1-ink-wash.md` | F1 笔意水墨 16 变体（A P Q1 Q2 W Y Z AA AE AF AG F1-AH F1-TX F1-CO F1-YS F1-BY） |
| `references/style-library/F2-blank-poster.md` | F2 留白海报 11 变体（B E F H I F2-K AB F2-OP F2-AC F2-3D F2-JS） |
| `references/style-library/F3-city.md` | F3 城市建筑 3 变体（C O F3-LC） |
| `references/style-library/F4-healing.md` | F4 治愈插画 5 变体（G J R K F4-RB） |
| `references/style-library/F5-oriental.md` | F5 东方古典 15 变体（L M1 M2 M3 M4 N AC AD F5-AE F5-AF F5-DC F5-DY F5-MP F5-YL F5-QS） |
| `references/style-library/F6-atmosphere.md` | F6 氛围实验 2 变体（D X） |
| `references/style-library/F7-photography.md` | F7 写实摄影 8 变体（S T U V H F7-AE F7-QW F7-ED） |
| `references/style-library/F8-concept-poster.md` | F8 概念海报 1 变体（V8 已验证） |
| `references/style-library/F9-photo-art.md` | F9 照片转艺术 5 变体（R1-R5） |
| `references/style-library/F10-papercut.md` | F10 剪纸纸艺 2 变体（F10-ST F10-WH） |
| `references/style-library/F11-puppetry.md` | F11 皮影偶戏 2 变体（F11-PY F11-MU） |
| `references/style-library/F12-glaze.md` | F12 釉面器物 2 变体（F12-QH F12-BX） |
| `references/style-library/F13-archive.md` | F13 纸本档案 2 变体（F13-AR F13-PL） |
| `references/style-library/F14-animation.md` | F14 美术片媒介 3 变体（F14-YZ F14-ZZ F14-SM） |
| `references/style-independence.md` | 风格独立协议（四问打分、开放注册、新增流程） |
| `references/theme-router.md` | 主题路由（九类主题 → 主风格/备选 + 对照填槽） |
| `references/taxonomy.md` | 体系分类总览（开放注册表 / 表现族 / 五变量语法 / 77 变体口径） |
| `references/optimize-pipeline.md` | 模式二完整管线：七维诊断、修复规则、缺维修复块表、输出纪律、机械核对、交付完整性 |
| `references/create-pipeline.md` | 模式三完整管线：重定义需求、七维填充、风格 DNA 决策、量化锁定、三道闸 |
| `references/memory-protocol.md` | 模式四：归档格式、偏好双写、手改 diff 学习、路由应用 |
| `references/imagegen-routing.md` | 出图路由（Grok / Codex 内置 / Codex CLI / 降级）+ 比例真源表 |
| `references/prompt-craft.md` | 出图封装、关键词库、HEX 色板、比例判断规则、尺寸表、质量自检 |
| `taxue-poster-studio/references/print-mode.md` | 印刷封面模式正源（opt-in，不套本库默认出图） |
| `references/task-constraints.md` | 任务类型 × 不可变约束（新图/参考改造/局部编辑/系列/一致性/视频；多参考角色分配；产品电商补全） |
| `references/model-dialect.md` | 跨模型方言层（模型无关母版 → 各模型方言；图像/编辑/视频/关键帧链路；双层质量检查） |
| `references/beast-myth.md` | 妖兽/神兽母题系统（东方三档：偏人/偏兽/神兽 + 西式生物：狼人/吸血鬼/兽人/美人鱼/西方龙；家族适配；不占变体号） |
| `references/embroidery-illustration.md` | 刺绣 · 混合媒介技法（彩锦绣肖像 / 苏绣肖像 / 实景×2D涂鸦；介质优先、身份保留；不占变体号） |
| `references/character-lock-sheet.md` | 人物锁定卡（身份锚点资料板：恒变量二分、全身五视角+脸部五角度+九表情、六类色卡与再生成固定点；人物一致性任务的锚点制作与复用工具；不占变体号） |
| `references/character-scene.md` | 人物场面语法包（回眸/窗下/背影/倚栏/案前/环境立；跨家族注入；不占变体号） |
| `references/motif-ceramic-asset.md` | 中式纹样陶瓷素材卡（C4D 矢量风：工艺语法固定、母题笔意词表八种、描边色随主题推演、三向配色规则；不占变体号） |
| `references/cover-constraints.md` | 封面约束档（安全原则、负空间技巧、失败修复表、版画工作流） |
| `references/scenario-pack.md` | 场景应用包（仅默认/已验证变体） |
| `references/brand-manual-visual.md` | 踏雪批量系列：品牌手册式三段信息架构 + 彩虹色相纪律（模型无关，只吸精髓） |
| `references/legacy-migration.md` | 变体编号迁移表（旧 A-X 编号 → 新家族编号） |
| `references/geometric-monument-poster.md` | 纪念碑几何概念海报元提示词（关系比喻「方尖碑投影」出处，模式二/三可参考） |
| `references/style-combination-matrix.md` | 风格组合优化矩阵（A 已验证 9 组 / B 高潜力 / C 探索 / D 禁止） |
| `references/verification-ledger.md` | 77 变体验证台账（状态/证据/下一步的单一真源；验证后与家族文件、SKILL §1 三处同步） |
| `references/gallery/` | 签名风格吸纳的外部出图样图（7 张，豆包 2026-08-16 验证）+ 索引 README |
| `memory/user-preferences.md` | 用户偏好档案（模式四维护，路由第 1 步读取） |
