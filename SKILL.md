# voice-generation

飞书语音生成技能 - 支持两种语音生成方案。

## 方案一：ChatTTS + RVC（高质量，首选）

**适用场景**：需要高质量、自然的语音效果

### 流程
1. 使用 `F:\实验文件夹\ChatTTS\chattts_infer.py` 生成 ChatTTS 语音
2. 使用 `F:\研究文件夹\RVC重构项目\原项目\rvc_infer_json.py` 进行 RVC 变声
3. 通过飞书发送语音

### 参数文件
- ChatTTS 参数：`F:\实验文件夹\ChatTTS\params_chattts.json`
- RVC 参数：`F:\实验文件夹\ChatTTS\params_rvc.json`

### 输出路径
- ChatTTS 输出：`E:\tts_output\ChatTTS\chattts_raw_{timestamp}.wav`
- RVC 输出：`E:\tts_output\推理\chattts_raw_{timestamp}_to_{model}_p{pitch}_{f0}.wav`

### 使用方法
```bash
# Step 1: ChatTTS 生成
python chattts_infer.py "要说的文本" --params "F:/实验文件夹/ChatTTS/params_chattts.json"

# Step 2: RVC 变声
python rvc_infer_json.py "input.wav" --params "F:/实验文件夹/ChatTTS/params_rvc.json"

# Step 3: 发送飞书语音
python feishu_voice.py --file "output.wav"
```

### Python 环境
- 必须使用：`C:\Espressif\tools\idf-python\python.exe`

### ⚠️ 重要：数字必须转换为中文大写
- **所有阿拉伯数字必须转换为中文大写**再传入 ChatTTS
- 例如：`20` → `二十`，`2024` → `二零二四`，`30秒` → `三十秒`
- 原因：ChatTTS 对阿拉伯数字的发音处理不佳，容易吞字或跳过
- 转换规则：
  - `0` → `零`，`1` → `一`，`2` → `二`，`3` → `三`，`4` → `四`
  - `5` → `五`，`6` → `六`，`7` → `七`，`8` → `八`，`9` → `九`
  - `10` → `十`，`100` → `百`，`1000` → `千`

### ⚠️ 重要：长文本自动分段处理
- **触发条件**：文本字符数超过 20 个字符
- **处理方式**：
  1. 根据上下文语境，在句号 `。`、逗号 `，` 等自然断句处将文本切分成多个部分
  2. 每个部分分别进行 ChatTTS + RVC 推理
  3. 推理完成后，将各部分音频合并成一个音频文件
  4. 最后发送合并后的完整音频
- **目的**：解决 ChatTTS 长文本（超过 20-30 秒）会出现截断、口齿不清的问题
- **注意**：分段时尽量保持语义完整，避免在句子中间截断

---

## 方案二：EdgeTTS + RVC（快速生成，备用）

**适用场景**：需要快速生成、不需要高质量音色

### 流程
1. 使用 EdgeTTS 生成基础语音
2. 使用 RVC 进行变声处理
3. 通过飞书发送语音

### 使用方法
```bash
# 直接使用 feishu_voice.py 的 RVC 模式
python feishu_voice.py "要说的文本" --rvc --model guanguanV1.pth --pitch 0
```

### 参数
- 默认模型：`guanguanV1.pth`
- 默认音调：0
- 默认 F0：rmvpe

---

## 发送飞书语音

### 方式一：通过 feishu_voice.py（推荐）
```bash
# 发送已有音频文件
python feishu_voice.py --file "E:\tts_output\推理\xxx.wav"

# 生成 TTS + RVC 后发送
python feishu_voice.py "文本" --rvc --model xxx.pth --pitch N
```

### 方式二：通过飞书 API
```bash
python feishu_voice.py --file "audio.opus"
```

### 防重复发送
- 发送前计算文件 MD5 hash
- 发送成功后创建标记文件 `E:\tts_output\.sent_{hash}.marker`
- 重复发送同一文件会被拒绝，如需重发请删除标记文件

### 发送后处理
- ✅ 发送成功后自动清理临时 OPUS 文件
- ⚠️ 保留原始 ChatTTS 和 RVC 输出文件在以下目录：
  - ChatTTS 输出：`E:\tts_output\ChatTTS\`
  - RVC 输出：`E:\tts_output\推理\`
- 💡 如需清理历史文件，可手动删除或说"清理语音文件"

---

## 核心脚本路径

| 脚本 | 路径 |
|------|------|
| ChatTTS 推理 | `F:\实验文件夹\ChatTTS\chattts_infer.py` |
| RVC 推理 | `F:\研究文件夹\RVC重构项目\原项目\rvc_infer_json.py` |
| 飞书语音发送 | `C:\Users\23375\.openclaw\workspace\scripts\feishu_voice.py` |
| ChatTTS WebUI | `F:\实验文件夹\ChatTTS\examples\web\webui.py` (端口 8080) |
| RVC WebUI | `F:\研究文件夹\RVC重构项目\原项目\rvc_infer_only.py` (端口 7860) |

---

## Python 环境要求

- **必须使用**：`C:\Espressif\tools\idf-python\python.exe`
- 端口要求：8080（ChatTTS）、7860（RVC）

---

## 触发方式

当用户说以下关键词时触发：
- "发语音"
- "说给我听"
- "语音消息"
- "变声"
- "生成语音"
- 直接请求发送语音

用户只需提供文本内容，技能自动选择最佳方案生成并发送。
