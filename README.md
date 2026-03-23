# Feishu Voice Skill

## 飞书语音技能 / Feishu Voice Skill

> 一款基于 OpenClaw 的飞书语音消息生成技能，融合 ChatTTS 与 RVC 语音转换技术，为您打造温和自然、亲切温暖的声音体验。

> A Feishu (Lark) voice message generation skill for OpenClaw, combining ChatTTS and RVC voice conversion technologies to deliver warm, natural, and friendly voice experiences.

---

## 目录 / Table of Contents

- [仓库信息 / Repository](#仓库信息-repository)
- [项目介绍 / Introduction](#项目介绍-introduction)
- [核心特性 / Features](#核心特性-features)
- [技术架构 / Architecture](#技术架构-architecture)
- [工作流程 / Workflow](#工作流程-workflow)
- [推理流程详解 / Inference Process](#推理流程详解-inference-process)
- [快速开始 / Quick Start](#快速开始-quick-start)
- [Python 环境自动检测](#python-环境自动检测)
- [给 AI Agent 的使用指南](#给-ai-agent-的使用指南)
- [使用说明 / Usage](#使用说明-usage)
- [项目结构 / Project Structure](#项目结构-project-structure)
- [开源引用 / Open Source](#开源引用-open-source)
- [免责声明 / Disclaimer](#免责声明-disclaimer)

---

## 仓库信息 / Repository

| 项目 / Item | 信息 / Info |
|-------------|-------------|
| **仓库地址 / URL** | https://github.com/jiuyou-dev/feishu-voice-skill |
| **所有者 / Owner** | jiuyou-dev (九幽实验室) |
| **许可证 / License** | MIT License |
| **开源协议 / Open Source** | ChatTTS (BSD-3-Clause), RVC (MIT) |

---

## 项目介绍 / Introduction

### 中文介绍

**Feishu Voice Skill** 是一款专为 OpenClaw AI 助手设计的飞书语音消息生成技能。它巧妙地结合了两大核心技术：

1. **ChatTTS**（字节跳动开源的高质量语音合成系统）- 负责将文本转换为自然流畅的语音
2. **RVC**（检索式语音转换）- 负责将语音转换为特定音色，保留原始语音的情感和韵律

通过这两者的完美结合，我们能够生成**温和亲切、情感丰富、韵律自然**的语音消息，并通过飞书平台发送给用户。

### English Introduction

**Feishu Voice Skill** is a voice message generation skill designed specifically for the OpenClaw AI assistant. It ingeniously combines two core technologies:

1. **ChatTTS** (ByteDance's open-source high quality text-to-speech system) - responsible for converting text into natural and fluent speech
2. **RVC** (Retrieval-based Voice Conversion) - responsible for transforming speech to specific timbres while preserving original emotion and prosody

Through the perfect combination of these two technologies, we can generate **warm, friendly, emotionally rich, and natural-sounding** voice messages and send them to users via the Feishu platform.

---

## 核心特性 / Features

### 主要功能 / Core Functions

| 功能 / Feature | 描述 / Description |
|----------------|-------------------|
| **ChatTTS 语音合成** | 将任意文本转换为自然语音 |
| **RVC 音色转换** | 将 ChatTTS 语音转换为目标音色 |
| **飞书消息发送** | 支持群聊和私聊语音消息发送 |
| **长文本处理** | 自动分段处理超长文本 |
| **数字转换** | 阿拉伯数字自动转换为中文大写 |
| **Python 自动检测** | 自动选择仓库内嵌 Python 或系统 Python |

### 声音特点 / Voice Characteristics

- **温和亲切 / Warm & Friendly** - 音质温暖自然，如同与朋友交谈
- **情感丰富 / Rich Emotion** - 保留文本中的情感表达
- **韵律自然 / Natural Prosody** - 语调起伏自然，听感舒适
- **清晰准确 / Clear & Accurate** - 发音标准，语义传达准确

---

## 技术架构 / Architecture

### 系统架构图 / System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Feishu Voice Skill                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐   │
│   │   Text   │───▶│  ChatTTS │───▶│    RVC   │───▶│  Feishu  │   │
│   │  Input   │    │   (TTS)  │    │ (VC/音色) │    │  (Send) │   │
│   └──────────┘    └──────────┘    └──────────┘    └──────────┘   │
│       │                │                 │                │          │
│       ▼                ▼                 ▼                ▼          │
│   用户输入        文本→语音           音色转换          飞书发送      │
│   User Input     Text→Speech         Timbre Conv.     Message Send  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 工作流程 / Workflow

### 完整工作流程 / Complete Workflow

```
Step 1: 用户输入文本
Step 2: ChatTTS 语音合成
Step 3: 音频预处理
Step 4: RVC 音色转换
Step 5: 后处理与发送
Step 6: 用户接收
```

详见 [推理流程详解 / Inference Process](#推理流程详解-inference-process)。

---

## 快速开始 / Quick Start

### 环境要求 / Requirements

| 要求 / Requirement | 最低配置 / Minimum | 推荐配置 / Recommended |
|-------------------|-------------------|----------------------|
| Python | 3.11 | 3.11 |
| GPU | GTX 1060 6GB | RTX 3060 12GB+ |
| 内存 / RAM | 8GB | 16GB+ |
| 磁盘空间 / Disk | 10GB | 20GB+ |
| FFmpeg | ✓ 必需 / Required | Latest |

### 安装步骤 / Installation

#### 中文安装

```bash
# 1. 克隆仓库
git clone https://github.com/jiuyou-dev/feishu-voice-skill.git
cd feishu-voice-skill

# 2. 安装依赖（仓库内嵌 Python 已包含大部分依赖）
# 如使用仓库内嵌 Python：
python/python.exe -m pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu128

# 或使用系统 Python：
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu128

# 3. 安装 FFmpeg (Windows)
# 下载 https://ffmpeg.org/download.html
# 或使用: winget install ffmpeg

# 4. 配置飞书 API 密钥
# 在飞书开放平台创建应用并获取 app_id 和 app_secret
```

#### English Installation

```bash
# 1. Clone the repository
git clone https://github.com/jiuyou-dev/feishu-voice-skill.git
cd feishu-voice-skill

# 2. Install dependencies (bundled Python includes most dependencies)
# Using bundled Python:
python/python.exe -m pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu128

# Or using system Python:
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu128

# 3. Install FFmpeg (Windows)
# Download from https://ffmpeg.org/download.html
# Or use: winget install ffmpeg

# 4. Configure Feishu API credentials
# Create an app on Feishu Open Platform and get app_id and app_secret
```

---

## Python 环境要求

本项目**仅支持仓库内嵌 Python**，位于 `<repo_root>/python/python.exe`（Python 3.11.9）。

> **重要**：不提供其他 Python 环境选项，请确保使用仓库内嵌 Python。

### 环境变量

| 环境变量 | 说明 | 默认值 |
|----------|------|--------|
| `TTS_OUTPUT_DIR` | TTS 输出根目录 | `E:\tts_output` |

---

## 给 AI Agent 的使用指南

如果你是在 OpenClaw、Qclaw 或其他 Agent 框架中运行此技能的 AI Agent，请按以下步骤操作：

### 步骤 0：克隆仓库（如尚未克隆）

如果 Agent 尚未获取到仓库代码，先克隆到本地：

```bash
git clone https://github.com/jiuyou-dev/feishu-voice-skill.git <目标目录>
cd feishu-voice-skill
```

> **仓库地址**：https://github.com/jiuyou-dev/feishu-voice-skill
>
> **说明**：克隆后，Agent 应将 `<目标目录>` 记录为 `repo_root`，后续所有路径解析都基于这个目录。

### 步骤 1：读取 SKILL.md

Agent 应读取仓库中的 `SKILL.md` 文件，理解：
- **触发关键词**：当用户说"发语音"、"与我说"、"和我说"、"说给我听"等时触发
- **路径解析模块**：`scripts/_python_resolver.py` 负责 Python 路径和输出路径的自动解析
- **Python 环境**：自动检测，无须硬编码

### 步骤 2：获取 Python 解释器

Agent 通过导入 `_python_resolver.py` 获取正确的 Python 路径：

```python
import sys
import os

repo_root = "<仓库根目录>"  # Agent 应从上下文获知
sys.path.insert(0, os.path.join(repo_root, "scripts"))
from _python_resolver import get_python_exe, get_repo_root

python_exe = get_python_exe()   # 自动选择正确的 Python
repo_root = get_repo_root()       # 获取仓库根目录
```

### 步骤 3：执行环境检查

```python
import subprocess

env_check = os.path.join(repo_root, "scripts", "check_environment.py")
result = subprocess.run(
    [python_exe, env_check],
    capture_output=True,
    text=True
)
print(result.stdout)
if result.returncode != 0:
    print("环境检查失败:", result.stderr)
```

### 步骤 4：根据检查结果向用户报告

**情况一：检查通过（返回码 = 0）**

```
✅ 环境检查通过！

检查结果：
- PyTorch：已安装，支持 CUDA
- GPU：NVIDIA GeForce RTX [型号]
- CUDA：可用
- FFmpeg：已安装
- Edge-TTS：已安装
- Python：{自动检测到的 Python 路径}

语音技能已就绪，可以正常使用了！
```

**情况二：检查失败（返回码 ≠ 0）**

```
❌ 环境检查失败：您的 GPU 不支持 PyTorch

可能的原因：
  1. 您的显卡太旧（需要 NVIDIA GPU，计算能力 >= 3.5）
  2. NVIDIA 驱动未正确安装
  3. PyTorch CUDA 版本与驱动不匹配

解决方案：
  1. 更新 NVIDIA 驱动到最新版本
  2. 重新安装匹配 CUDA 版本的 PyTorch
  3. 如无法解决，请提交 Issue:
     https://github.com/jiuyou-dev/feishu-voice-skill/issues

【自动切换】
  系统将自动使用 EdgeTTS 方案替代，语音功能仍可正常使用。
```

**情况三：部分警告（可继续但功能受限）**

```
⚠️ 环境检查完成，但存在以下警告：
- CUDA 不可用，将使用 CPU 模式（速度较慢）
- 建议安装 GPU 版本的 PyTorch 以提升性能

语音技能仍可正常使用，但推荐配置 GPU 环境。
```

### 步骤 5：技能使用流程

环境检查通过后，Agent 可以按以下流程使用技能：

```python
import subprocess
import os

repo_root = get_repo_root()
python_exe = get_python_exe()

chattts_script = os.path.join(repo_root, "ChatTTS", "chattts_infer.py")
rvc_script = os.path.join(repo_root, "RVC", "rvc_infer_json.py")
feishu_script = os.path.join(repo_root, "scripts", "feishu_voice.py")

# 1. 调用 ChatTTS 生成语音
chat_result = subprocess.run(
    [python_exe, chattts_script, "你好啊，今天天气真不错！"],
    capture_output=True,
    text=True,
    cwd=repo_root
)
print(chat_result.stdout)

# 2. 调用 RVC 变声（根据上一步输出的文件路径）
# 假设上一步输出到 E:\tts_output\ChatTTS\chattts_raw_xxx.wav
chat_output_wav = "...(从上一个命令输出中提取文件路径)..."

rvc_result = subprocess.run(
    [python_exe, rvc_script, chat_output_wav,
     "--model", "guanguanV1.pth", "--pitch", "0"],
    capture_output=True,
    text=True,
    cwd=repo_root
)
print(rvc_result.stdout)

# 3. 发送飞书语音
feishu_result = subprocess.run(
    [python_exe, feishu_script, "--file", rvc_output_wav],
    capture_output=True,
    text=True,
    cwd=repo_root
)
print(feishu_result.stdout)
```

### 步骤 6：遇到错误时的处理

当技能出现任何错误时，Agent 应主动引导用户反馈：

```
🐛 抱歉，技能运行过程中遇到了问题！

为了更好地解决这个情况，麻烦你到 GitHub 提交 Issue 反馈一下：
https://github.com/jiuyou-dev/feishu-voice-skill/issues

反馈时建议包含：
- 问题描述（做了什么操作、出现了什么错误）
- 错误日志（如果有的话）
- 你的环境信息（操作系统、Python 版本等）

我们会尽快跟进处理！感谢你的反馈～
```

---

## 使用说明 / Usage

### 基本用法 / Basic Usage

#### 中文使用

```python
# 方式1: 使用联合推理管道 (推荐)
import sys
import os

repo_root = "<仓库根目录>"
sys.path.insert(0, os.path.join(repo_root, "scripts"))
from chattts_rvc_pipeline import ChatTTSRVCPipeline

pipeline = ChatTTSRVCPipeline()
pipeline.run(
    text="你好，今天天气真不错呀~",
    output_path="output.wav"
)

# 方式2: 发送飞书语音消息
from feishu_voice import send_voice_message

send_voice_message(
    text="这是测试语音消息",
    receive_id="ou_xxxxx",  # 飞书用户 open_id
    receive_id_type="open_id"
)
```

#### English Usage

```python
# Method 1: Use combined pipeline (Recommended)
import sys
import os

repo_root = "<repo_root>"
sys.path.insert(0, os.path.join(repo_root, "scripts"))
from chattts_rvc_pipeline import ChatTTSRVCPipeline

pipeline = ChatTTSRVCPipeline()
pipeline.run(
    text="Hello, the weather is nice today~",
    output_path="output.wav"
)

# Method 2: Send Feishu voice message
from feishu_voice import send_voice_message

send_voice_message(
    text="This is a test voice message",
    receive_id="ou_xxxxx",  # Feishu user open_id
    receive_id_type="open_id"
)
```

### 命令行使用 / Command Line Usage

```bash
# 基本用法
python ChatTTS/chattts_infer.py "你好世界"

# 指定参数
python ChatTTS/chattts_infer.py \
    --text "今天天气真好" \
    --output "test.wav"

# RVC 转换
python RVC/rvc_infer_json.py \
    --input "chatttts_output.wav" \
    --model "guanguanV1.pth" \
    --output "final_output.wav"
```

### 参数说明 / Parameters

| 参数 / Parameter | 类型 / Type | 默认值 / Default | 说明 / Description |
|-----------------|------------|-----------------|-------------------|
| `--text` | string | 必填 / Required | 要转换的文本 |
| `--output` | string | auto | 输出文件路径 |
| `--temperature` | float | 0.8 | 采样温度 |
| `--top_p` | float | 0.9 | Nucleus 采样 |
| `--pitch` | int | 0 | 音调调整 (-24~24) |
| `--f0_method` | string | rmvpe | F0 提取方法 |

---

## 项目结构 / Project Structure

```
feishu-voice-skill/              ← 仓库根目录 (<repo_root>)
│
├── README.md                    # 主说明文件 / Main documentation
├── LICENSE                     # MIT 许可证
│
├── ChatTTS/                   # ChatTTS 推理模块
│   ├── chattts_infer.py       # ChatTTS 推理脚本
│   └── params_chattts.json    # 默认参数
│
├── RVC/                       # RVC 推理模块
│   ├── rvc_infer_json.py      # RVC 推理脚本
│   ├── params_rvc.json       # RVC 参数
│   └── assets/                # 模型资源
│       └── weights/           # RVC 模型权重
│
├── scripts/                   # 用户脚本
│   ├── _python_resolver.py   # Python 路径自动解析（核心模块）
│   ├── feishu_voice.py        # 飞书发送脚本
│   └── check_environment.py   # 环境检查脚本
│
├── packages/                  # 原始包结构（参考）
│   ├── chatttts/             # ChatTTS 官方包
│   └── rvc/                  # RVC 官方包
│
└── python/                   # 内嵌 Python 环境（可选，不上传 Git）
    └── python.exe             # Python 3.11.9
```

---

## 开源引用 / Open Source

本项目使用了以下开源项目，遵循其相应的许可证：

| 项目 / Project | 许可证 / License | 仓库 / Repository |
|---------------|-----------------|------------------|
| **ChatTTS** | BSD-3-Clause | https://github.com/2noise/ChatTTS |
| **RVC** | MIT | https://github.com/RVC-Project/Retrieval-Based-Voice-Conversion |
| **PyTorch** | BSD-3-Clause | https://github.com/pytorch/pytorch |
| **FFmpeg** | LGPL/GPL | https://ffmpeg.org/ |

---

## 免责声明 / Disclaimer

### 中文免责声明

1. **仅供学习研究**：本项目仅供学习与研究使用，请勿用于任何商业目的。
2. **尊重隐私**：请勿使用本项目进行未经授权的语音合成或声音模仿。
3. **遵守法律**：请遵守当地法律法规，不要将本项目用于任何非法用途。
4. **风险自担**：使用本项目产生的任何问题，由使用者自行承担风险和责任。
5. **声音模型授权**：声音模型仅供授权使用，请勿随意传播或滥用。

### English Disclaimer

1. **For Learning Only**: This project is for learning and research purposes only. Do not use it for any commercial purposes.
2. **Respect Privacy**: Do not use this project for unauthorized voice synthesis or voice imitation.
3. **Comply with Laws**: Please comply with local laws and regulations. Do not use this project for any illegal purposes.
4. **Use at Your Own Risk**: Any issues arising from the use of this project are at the user's own risk and responsibility.
5. **Voice Model Authorization**: Voice models are for authorized use only. Do not distribute or misuse them.

---

## 联系方式 / Contact

- **GitHub Issues**: https://github.com/jiuyou-dev/feishu-voice-skill/issues
- **Owner**: jiuyou-dev

---

*打造温暖的声音，传递真挚的情感*

*Creating warm voices, delivering genuine emotions*
