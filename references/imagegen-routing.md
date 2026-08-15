# 出图路由

提示词填完必须出像素。禁止只交提示词。禁止调用 baoyu、即梦、jimeng 或其他外部生图技能。

按**当前会话实际拥有的工具**选路：磁盘上有技能文件 ≠ 本会话能调原生工具。Grok 与 Codex 任一条能出像素即可，不要两条都跑。没有对应工具就降级，禁止假装已调用。

1. **用户点名的后端**（「用 Codex」「用 CLI」「用 Grok」）
2. **Grok 宿主**（本会话同时有 `image_gen` 与 `image_edit`）：
   - 先读 Grok 宿主内置的生图技能说明
   - 新图：`image_gen(prompt, aspect_ratio)`，prompt = 出图封装（prompt-craft.md）
   - 改图 / 系列锚定：`image_edit`。已有过关成图时不要全新 `image_gen`
   - 交付路径 = 工具返回的 session-relative 路径（如 `images/3.jpg`）。用户指定目录才拷
   - 出图后读回图片，走质量自检（prompt-craft.md）
3. **Codex 宿主**（有内置 `image_gen`、没有 Grok 的 `image_edit`）。Codex 自己有两条生图能力，**任一条都能出图**，prompt 都用出图封装，不要为了路径或分辨率擅自切 CLI：
   - 先读 `$CODEX_HOME/skills/.system/imagegen/SKILL.md`（默认 `$HOME/.codex/...`）
   - **默认：内置 `image_gen`**。不需要 `OPENAI_API_KEY`。新图直接 `image_gen`；改图先 `view_image` 把图送进对话，再走 imagegen 编辑流。产物默认 `$CODEX_HOME/generated_images/`，再拷到用户指定路径或工作区
   - **第二条：官方 CLI** `scripts/image_gen.py`。只在用户点名 CLI / API / 模型，或内置工具不可用且用户确认后用。需要 `OPENAI_API_KEY`。默认模型 `gpt-image-2`，质量 `high`，`--size` 用下表。禁止为了改路径或分辨率从内置切过来
     ```bash
     python "${CODEX_HOME:-$HOME/.codex}/skills/.system/imagegen/scripts/image_gen.py" generate \
       --prompt "..." --size <下表> --quality high --out <交付路径.png>
     python "${CODEX_HOME:-$HOME/.codex}/skills/.system/imagegen/scripts/image_gen.py" edit \
       --image <原图> --prompt "只改X，其余不动" --quality high --out <新路径.png>
     ```
   - 出图后 `view_image` 读回，走质量自检。修图走上面同一条后端的 edit，不要调用 Grok 的 `image_edit`
4. **非宿主**（Kimix / Claude 等，两条内置都没有）：走第 3 条的 Codex CLI，缺 Key 就停，**落到降级交付**（见第 5 条）
5. **降级交付（内置与 CLI 都不可用）**：不假装已出图。交付时**必须附「验证待办」**：明示「本会话无生图工具（缺 image_gen / OPENAI_API_KEY），请用你常用的生图工具出图，把结果图回传给我做自检与偏好记录」。同时按 memory-protocol.md 降级记录把这条交付写入使用历史（反馈待补）。这是正常路径，不是失败路径——提示词质量靠用户回传校准，闭环不依赖会话内工具

## 比例真源

（Grok 无 `21:9` / `5:2`，用 `20:9` / `2:1`。Codex CLI 的 `--size` 两边须为 16 的倍数）

| 用途 | Codex 内置 / CLI `--size` | Grok `aspect_ratio` |
|------|---------------------------|---------------------|
| 人物 / 海报竖（默认） | `1536x2048` | `3:4` |
| 立轴 / F7-V 影棚 | `1024x1536` | `2:3` |
| 城市卡 C / 纸雕 | `2048x1536` | `4:3` |
| 治愈 F4 方图 | `1536x1536` | `1:1` |
| 头图 / 封面横 | `2048x1152` | `16:9` |
| 壁纸 / F1-Y | `1152x2048` | `9:16` |
| 横幅摄影 | `1536x1024` | `3:2` |
| 超宽横幅 | `1920x864` | `20:9` |
| 长卷 / banner | `2048x1024` | `2:1` |
| 概念海报 F8-V8（5:2） | `2048x816` | 无 `5:2`，用 `20:9` 或 `2:1` |

Grok 可用：`1:1` `3:4` `4:3` `9:16` `16:9` `2:3` `3:2` `2:1` `1:2` `9:19.5` `19.5:9` `9:20` `20:9` `auto`。Codex 内置不暴露 `aspect_ratio` / `--size` 参数，尺寸按模型默认；要精确像素用 CLI 的 `--size`。
