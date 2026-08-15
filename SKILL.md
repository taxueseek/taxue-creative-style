---
name: taxue-creative-style
description: >
  踏雪影像风格引擎。四种能力：①按风格库出图（文人水墨、留白海报、城市卡、治愈插画、上美影、剪纸、纸雕、日式杂志、写实胶片、CCD、影棚人像等）②优化任意已有提示词（七维诊断打分+修复+注入踏雪DNA）③元提示词创作（任意需求从零构建精确视觉指令，保持踏雪独到影像风格）④学习用户偏好（记录使用历史与反馈，下次路由优先匹配）。子技能路由：个人 IP 插画、民国漫画杂志、图片反推（见正文 §0）。触发：踏雪风格、taxue style、文人水墨、上美影、剪纸、纸雕、水墨城市、概念海报、提示词优化、优化提示词、帮我写提示词、写个提示词、元提示词、创作提示词、提示词创作、出图、生成图片、帮我画。
---

# Taxue Creative Style — 踏雪创意风格

## 0. 本质与模式路由

**第一性原理定义**：本 skill 是一个「影像指令编译器」。输入任意意图，输出模型能精确执行的视觉指令。输出质量 = 意图识别精度 × 风格模板精度 × 参数化完整度 × 反馈闭环。

**加载协议（先读本文件，再按需读 references，禁止一次全读）**：

| 场景 | 必读文件 |
|------|---------|
| 模式一按家族出图 | 对应家族文件（§1 速查表末列）+ 出图时读 imagegen-routing.md + prompt-craft.md |
| 模式二提示词优化 | optimize-pipeline.md（含七维诊断 + 修复块表） |
| 模式三元提示词创作 | create-pipeline.md |
| 封面 / 头图 / banner | cover-constraints.md |
| 出图前 | imagegen-routing.md（选宿主 + 尺寸）+ prompt-craft.md（封装 + 比例 + 自检） |
| 交付后记录 | memory-protocol.md（归档 + 偏好双写） |
| 出图验证后状态回填 | verification-ledger.md（状态/证据/下一步，三处同步） |
| 场景快捷推荐 | scenario-pack.md |
| 批量系列 / 品牌手册 / 彩虹色相 | brand-manual-visual.md（踏雪化系列色相纪律） |
| 旧编号引用 | legacy-migration.md |

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
3. **子技能路由（先于家族匹配）**：用户需求命中以下场景时，路由到对应子技能，不强行套 9 家族：
   - **个人 IP / 卡通形象 / 形象一致性插画** → `taxue-ip-illustration`（形象基底→风格化变体→场景化应用）
   - **民国漫画 / 月份牌 / 鲁迅排版 / 苏式海报 / 老上海复古** → `taxue-minguo-comic`（民国杂志风格系统）
   - **一张图 → 多风格/多视角/多世界观/多美学的系列变体** → `taxue-vanxiang`（踏雪万象，独立技能：核不变，七轴可变）
   - **本地图片/截图 → 反推提示词（复刻版 + 踏雪化两件套）** → `taxue-image-reverse`（图片反推：七维拆解 + 家族归类 + 归档双写）
   - **传统艺术门类：国画/岩画/雕塑/脸谱/工艺美术/民间美术** → `taxue-artist`（踏雪艺术家，独立技能：门类卡片 + 元提示词 + 定制提示词；正宗国画门类与本库 F1 踏雪水墨互不替代）
   - 子技能输出同样遵循本 skill 的踏雪 DNA、出图路由（imagegen-routing.md）、比例建议（prompt-craft.md）、归档双写（memory-protocol.md）
4. 模式一 → 走家族匹配（§1）；模式二 → 读 optimize-pipeline.md；模式三 → 读 create-pipeline.md
5. 出图封装（prompt-craft.md）→ 出图（imagegen-routing.md）→ 自检（prompt-craft.md）→ 记录（memory-protocol.md）

---

## 1. 风格库（9 家族，47 个变体）

先定家族再定变体。**状态列决定可用性**：✅ 已验证（体系内出图通过，可默认）｜无标注 = 默认变体（模板已固化、来源已验证——外部发布、多平台出图、用户提供或早期迭代固化；可默认路由，不因未在本体系复验而受限，对外不得自称已验证）｜⚠️ 实验、🔶 测试中（点名才用，禁止默认路由与场景包推荐）。47 个变体的验证状态、证据与下一步的单一真源 = verification-ledger.md；任何状态变更必须三处同步（家族文件索引+正文状态行、本速查表状态列、验证台账）。

**家族速查**（详细模板在各家族文件，选中后读对应文件）：

| 家族 | 适用主题 | 变体 | 默认比例 | 文件 |
|------|---------|------|---------|------|
| F1 笔意水墨 | 孤寂人物、水墨美女、猫、线舞猫、实验混搭、宋画、飞天、赛博国潮、写意油画微景观、墨迹微缩世界 | A、P、Q1、Q2、W、Y✅、Z⚠️、AA⚠️、AE🔶、AF、AG | 竖 3:4 | style-library/F1-ink-wash.md |
| F2 留白海报 | 节日、概念、书法字、隐喻、国潮、信息图、欧普线描 | B、E、F、H、I、F2-K⚠️、AB⚠️、OP✅ | 竖 3:4（OP 例外 2:3） | style-library/F2-blank-poster.md |
| F3 城市建筑 | 城市卡、纸雕大场景 | C、O | 横 4:3 | style-library/F3-city.md |
| F4 治愈插画 | 日常小物、动物、温馨场景、儿童绘本手账、橡皮章版画 | G、J、R、K、RB | 方 1:1 | style-library/F4-healing.md |
| F5 东方古典 | 仕女、剪纸、复古杂志、仙侠、日式时尚插画 | L、M1、M2、M3、M4、N、AC⚠️、AD | 竖 3:4 | style-library/F5-oriental.md |
| F6 氛围实验 | 黑暗行者、符号雕塑 | D、X | 竖 3:4 | style-library/F6-atmosphere.md |
| F7 写实摄影 | 纪实、胶片、CCD、影棚、高速运动 | S、T、U、V、H | 按变体 | style-library/F7-photography.md |
| F8 概念海报 | 文字/词语/短句的视觉化、词义隐喻、高级概念海报 | V8✅ | 横 5:2 | style-library/F8-concept-poster.md |
| F9 照片转艺术 | 日常照片/废片 → 诗意手绘/抽象编辑/涂鸦/赛璐璐/皮影 | R1、R2、R3、R4、R5 | 竖 3:4 | style-library/F9-photo-art.md |

**编号纪律**：H 与 K 均有重号——F2-H（招聘海报）≠ F7-H（高速运动）；F2-K（国潮连字）≠ F4-K（绘本手账）。按家族编号区分，禁止混用。

**主题默认映射**（无历史偏好时使用）：概念/人生隐喻 → F8（词义视觉化）或 F2（非文字主题）；城市 → F3；猫 → F1 或 F4；美女 → F1 或 F5；剪纸 → F5；纸雕 → F3；写实 → F7；节日海报 → F2；实验 → F6；照片转艺术（复活/抽象编辑/涂鸦/赛璐璐/皮影）→ F9；儿童绘本/手账/抽象概念诗意化 → F4-K；只说「踏雪风格」未指定 → 优先按 memory/user-preferences.md 的默认家族（当前 F8-V8）；无偏好记录才回落 F1-A。**禁止把实验变体（F1-Z / F1-AA / F2-K / F2-AB / F5-AC）或测试中变体（F1-AE）当作未指定时的默认。**

**通用 DNA 原则（所有家族适用）**：
1. **留白第一**：大面积空白是构图主体，不是空缺
2. **克制**：少即是多，宁意犹未尽不一览无余
3. **文字即设计**：中文字是视觉元素，非附属说明
4. **纸感优先**：宣纸肌理、印刷颗粒优于数字光泽（写实家族除外）
5. **概念深度**：捕捉本质而非图解表面
6. **色彩纪律**：受限色板，单一强调色常已足够
7. **文字纯净**：凡画面含指定文字，正文用自然语言写明「画面中除[指定文字]外不出现任何其他文字与标点，[指定文字]原样呈现不加标点，无任何水印、日期、签名」，不加「负面」标签

**家族用法**：选家族后读对应家族文件，先读风格卡片（调性→视觉特征→经典结构→禁忌）再填模板，保证风格不漂移。出图自检时对照卡片禁忌，逐项勾掉才算过关。

---

## 2. 硬约束清单（交付前逐项核对，缺一即不合格）

1. **缺比例建议 = 交付不完整，禁止交付**（判断规则见 prompt-craft.md）
2. **交付完整性 5 项**：优化版提示词 / 建议比例 / 变更说明 / 归档+偏好双写 / 出图验证待办（optimize-pipeline.md）
3. **输出前五查 + 机械核对**：形态/标点/可执行性守恒、粒度匹配、变量最小化、比喻具象化、比例建议；原句保留率 ≥90%（打磨）/ ≥80%（补全）（optimize-pipeline.md）
4. **出图后必自检**：盲写画面实际内容再对照量化规格；失败只修一项；同一项连续 2 次失败即停（prompt-craft.md）
5. **实验 / 测试变体门**：⚠️ 实验 F1-Z / F1-AA / F2-K / F2-AB / F5-AC、🔶 测试中 F1-AE，点名才用，禁止默认路由、禁止场景包推荐
6. **验证待办必附**：本会话无生图工具时，交付必须附「验证待办」并写明原因，禁止假装已出图、禁止静默交付（imagegen-routing.md 第 5 条）
7. **归档 + 偏好双写 + 状态三处同步**：每次交付必须同时写本地归档版本记录与 user-preferences.md 偏好字段；出图验证后必须同步家族文件状态、SKILL §1 速查表、verification-ledger.md（memory-protocol.md）
8. **模板维护铁律**：已验证变体只许补负向、参数化硬编码、拆冲突，禁止以「优化」名义稀释已验证约束（prompt-craft.md）
9. **语言形态守恒 + 原句优先**：优化 ≠ 重写，能改词不改句（optimize-pipeline.md）
10. **枚举不进正文**：MECE 枚举是自检逻辑，禁止整段写进 prompt 正文，正文只留一句推演指令（create-pipeline.md）
11. **可执行性铁律**：禁止把「踏雪审美 / 踏雪 DNA / 踏雪留白 / 踏雪纸感 / 踏雪化」等内部术语原样写进交付给生图模型的 prompt；必须展开为可执行视觉描述（brand-manual-visual.md 零节）
12. **色板按风格选择**：没有单一“踏雪参考色板”；必须按所选家族/场景选色并写具体 HEX，禁止用水墨五色替代全库（prompt-craft.md）

---

## References

| 文件 | 用途 |
|------|------|
| `references/style-library/F1-ink-wash.md` | F1 笔意水墨 11 变体（A P Q1 Q2 W Y Z AA AE AF AG） |
| `references/style-library/F2-blank-poster.md` | F2 留白海报 8 变体（B E F H I F2-K AB OP） |
| `references/style-library/F3-city.md` | F3 城市建筑 2 变体（C O） |
| `references/style-library/F4-healing.md` | F4 治愈插画 5 变体（G J R K RB） |
| `references/style-library/F5-oriental.md` | F5 东方古典 8 变体（L M1 M2 M3 M4 N AC AD） |
| `references/style-library/F6-atmosphere.md` | F6 氛围实验 2 变体（D X） |
| `references/style-library/F7-photography.md` | F7 写实摄影 5 变体（S T U V H） |
| `references/style-library/F8-concept-poster.md` | F8 概念海报 1 变体（V8，已验证） |
| `references/style-library/F9-photo-art.md` | F9 照片转艺术 5 变体（R1-R5） |
| `references/optimize-pipeline.md` | 模式二完整管线：七维诊断、修复规则、缺维修复块表、输出纪律、机械核对、交付完整性 |
| `references/create-pipeline.md` | 模式三完整管线：重定义需求、七维填充、风格 DNA 决策、量化锁定、三道闸 |
| `references/memory-protocol.md` | 模式四：归档格式、偏好双写、手改 diff 学习、路由应用 |
| `references/imagegen-routing.md` | 出图路由（Grok / Codex 内置 / Codex CLI / 降级）+ 比例真源表 |
| `references/prompt-craft.md` | 出图封装、关键词库、HEX 色板、比例判断规则、尺寸表、质量自检 |
| `references/cover-constraints.md` | 封面约束档（安全原则、负空间技巧、失败修复表、版画工作流） |
| `references/scenario-pack.md` | 场景应用包（仅默认/已验证变体） |
| `references/brand-manual-visual.md` | 踏雪批量系列：品牌手册式三段信息架构 + 彩虹色相纪律（模型无关，只吸精髓） |
| `references/legacy-migration.md` | 变体编号迁移表（旧 A-X 编号 → 新家族编号） |
| `references/geometric-monument-poster.md` | 纪念碑几何概念海报元提示词（关系比喻「方尖碑投影」出处，模式二/三可参考） |
| `references/style-combination-matrix.md` | 风格组合优化矩阵（A 已验证 9 组 / B 高潜力 / C 探索 / D 禁止） |
| `references/verification-ledger.md` | 47 变体验证台账（状态/证据/下一步的单一真源；验证后与家族文件、SKILL §1 三处同步） |
| `memory/user-preferences.md` | 用户偏好档案（模式四维护，路由第 1 步读取） |
