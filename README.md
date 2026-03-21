# Feishu Voice Skill

## 飞书语音技能 / 飞书语音技能

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

1. **ChatTTS** (ByteDance's open-source high-quality text-to-speech system) - responsible for converting text into natural and fluent speech
2. **RVC** (Retrieval-based Voice Conversion) - responsible for transforming speech to specific timbres while preserving original emotion and prosody

Through the perfect combination of these two technologies, we can generate **warm, friendly, emotionally rich, and natural-sounding** voice messages and send them to users via the Feishu platform.

---

## 核心特性 / Features

### 🎯 主要功能 / Core Functions

| 功能 / Feature | 描述 / Description |
|----------------|-------------------|
| **ChatTTS 语音合成** | 将任意文本转换为自然语音 |
| **RVC 音色转换** | 将 ChatTTS 语音转换为目标音色 |
| **飞书消息发送** | 支持群聊和私聊语音消息发送 |
| **长文本处理** | 自动分段处理超长文本 |
| **数字转换** | 阿拉伯数字自动转换为中文大写 |
| **批量处理** | 支持批量语音生成 |

### 🎙️ 声音特点 / Voice Characteristics

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
│   │  Input   │    │   (TTS)  │    │ (VC/音色) │    │  (Send)  │   │
│   └──────────┘    └──────────┘    └──────────┘    └──────────┘   │
│       │                │                 │                │          │
│       ▼                ▼                 ▼                ▼          │
│   用户输入        文本→语音           音色转换          飞书发送      │
│   User Input     Text→Speech         Timbre Conv.     Message Send  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### 核心技术栈 / Technology Stack

| 组件 / Component | 技术 / Technology | 版本 / Version | 说明 / Description |
|------------------|------------------|----------------|-------------------|
| TTS 引擎 | ChatTTS | latest | 字节跳动开源高质量语音合成 |
| 声音转换 | RVC | v2 | 检索式语音转换模型 |
| AI 框架 | PyTorch | 2.x | 深度学习框架 |
| 消息平台 | 飞书 API | v1 | 语音消息发送 |
| 运行时 | Python | 3.11 | 程序运行环境 |
| 音频处理 | FFmpeg | latest | 音频格式转换 |

---

## 工作流程 / Workflow

### 完整工作流程 / Complete Workflow

```
Step 1: 用户输入文本
┌─────────────────────────────────────┐
│  用户输入或 AI 生成文本              │
│  例: "你好，今天天气真不错呀~"       │
└─────────────────────────────────────┘
                │
                ▼
Step 2: ChatTTS 语音合成
┌─────────────────────────────────────┐
│  ChatTTS 将文本转换为语音            │
│  - 自然流畅的语调                    │
│  - 保留情感表达                      │
│  - 韵律节奏自然                      │
└─────────────────────────────────────┘
                │
                ▼
Step 3: 音频预处理
┌─────────────────────────────────────┐
│  - 采样率转换                        │
│  - 格式转换 (wav/opus)              │
│  - 音频质量优化                      │
└─────────────────────────────────────┘
                │
                ▼
Step 4: RVC 音色转换
┌─────────────────────────────────────┐
│  RVC 将语音转换为目标音色            │
│  - 保留原始情感                      │
│  - 保留韵律特征                      │
│  - 应用目标音色模型                  │
└─────────────────────────────────────┘
                │
                ▼
Step 5: 后处理与发送
┌─────────────────────────────────────┐
│  - 音频合并                          │
│  - 格式转换为 OPUS (飞书专用)        │
│  - 发送至飞书                        │
└─────────────────────────────────────┘
                │
                ▼
Step 6: 用户接收
┌─────────────────────────────────────┐
│  用户在飞书中接收语音消息            │
│  直接播放，无需下载                  │
└─────────────────────────────────────┘
```

---

## 推理流程详解 / Inference Process

### 1. ChatTTS 推理流程 / ChatTTS Inference Process

```
输入文本
    │
    ▼
┌───────────────────────────────┐
│  1. 文本规范化 (Text Normalization) │
│     - 数字转中文              │
│     - 特殊符号处理            │
│     - 多音字处理              │
└───────────────────────────────┘
    │
    ▼
┌───────────────────────────────┐
│  2. 语义分析 (Semantic Analysis)   │
│     - 句子边界检测            │
│     - 情感标注                │
│     - 韵律预测                │
└───────────────────────────────┘
    │
    ▼
┌───────────────────────────────┐
│  3. 生成音频参数              │
│     - 梅尔频谱 (Mel-Spectrogram) │
│     - pitch 轮廓             │
│     - 能量曲线                │
└───────────────────────────────┘
    │
    ▼
┌───────────────────────────────┐
│  4. 声码器合成 (Vocoder)         │
│     - HiFiGAN / BigVGAN       │
│     - 波形生成                │
└───────────────────────────────┘
    │
    ▼
ChatTTS 语音输出 (raw_audio.wav)
```

### 2. RVC 推理流程 / RVC Inference Process

```
ChatTTS 语音输入
    │
    ▼
┌───────────────────────────────┐
│  1. 音频预处理                │
│     - 重采样 (根据模型要求)    │
│     - 单声道转换              │
│     - 标准化                  │
└───────────────────────────────┘
    │
    ▼
┌───────────────────────────────┐
│  2. F0 提取 (Pitch Extraction)  │
│     - RMVPE (推荐)            │
│     - Harvest                 │
│     - Crepe                   │
│     - 提取基频轮廓            │
└───────────────────────────────┘
    │
    ▼
┌───────────────────────────────┐
│  3. 特征提取                  │
│     - Huberts 特征提取        │
│     - 音频表示学习            │
│     - 1000帧/秒               │
└───────────────────────────────┘
    │
    ▼
┌───────────────────────────────┐
│  4. 音色转换                  │
│     - 加载 RVC 模型权重       │
│     - 特征映射                │
│     - 音色变换                │
└───────────────────────────────┘
    │
    ▼
┌───────────────────────────────┐
│  5. 波形重建                  │
│     - 逆变换                  │
│     - 输出目标音色语音         │
└───────────────────────────────┘
    │
    ▼
RVC 转换后语音 (voice_converted.wav)
```

### 3. 飞书发送流程 / Feishu Send Process

```
RVC 转换后语音
    │
    ▼
┌───────────────────────────────┐
│  1. 格式转换                  │
│     - WAV → OPUS (FFmpeg)     │
│     - 飞书只支持 OPUS 格式    │
└───────────────────────────────┘
    │
    ▼
┌───────────────────────────────┐
│  2. 音频上传                  │
│     - 调用飞书 API            │
│     - 获取 file_key           │
└───────────────────────────────┘
    │
    ▼
┌───────────────────────────────┐
│  3. 发送语音消息              │
│     - 调用发消息 API          │
│     - 指定接收者              │
│     - 支持群聊/私聊           │
└───────────────────────────────┘
    │
    ▼
飞书消息发送成功 ✓
```

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

# 2. 安装 Python 依赖
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu128
pip install -r packages/chatttts/requirements.txt
pip install -r packages/rvc/requirements.txt

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

# 2. Install Python dependencies
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu128
pip install -r packages/chatttts/requirements.txt
pip install -r packages/rvc/requirements.txt

# 3. Install FFmpeg (Windows)
# Download from https://ffmpeg.org/download.html
# Or use: winget install ffmpeg

# 4. Configure Feishu API credentials
# Create an app on Feishu Open Platform and get app_id and app_secret
```

---

## 使用说明 / Usage

### 基本用法 / Basic Usage

#### 中文使用

```python
# 方式1: 使用联合推理管道 (推荐)
from scripts.chattts_rvc_pipeline import ChatTTSRVCPipeline

pipeline = ChatTTSRVCPipeline()
pipeline.run(
    text="你好，今天天气真不错呀~",
    output_path="output.wav"
)

# 方式2: 发送飞书语音消息
from scripts.feishu_voice import send_voice_message

send_voice_message(
    text="这是测试语音消息",
    receive_id="ou_xxxxx",  # 飞书用户 open_id
    receive_id_type="open_id"
)
```

#### English Usage

```python
# Method 1: Use combined pipeline (Recommended)
from scripts.chattts_rvc_pipeline import ChatTTSRVCPipeline

pipeline = ChatTTSRVCPipeline()
pipeline.run(
    text="Hello, the weather is nice today~",
    output_path="output.wav"
)

# Method 2: Send Feishu voice message
from scripts.feishu_voice import send_voice_message

send_voice_message(
    text="This is a test voice message",
    receive_id="ou_xxxxx",  # Feishu user open_id
    receive_id_type="open_id"
)
```

### 命令行使用 / Command Line Usage

```bash
# 基本用法
python packages/chatttts/chattts_infer.py --text "你好世界"

# 指定参数
python packages/chatttts/chattts_infer.py \
    --text "今天天气真好" \
    --output "test.wav" \
    --temperature 0.8 \
    --top_p 0.9

# RVC 转换
python packages/rvc/rvc_infer_json.py \
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
feishu-voice-skill/
│
├── README.md                      # 主说明文件 / Main documentation
├── README_CN.md                   # 中文说明文件 / Chinese documentation
├── LICENSE                        # MIT 许可证
│
├── packages/                      # 核心代码包 / Core packages
│   │
│   ├── chatttts/                 # ChatTTS 源码包
│   │   ├── ChatTTS/             # ChatTTS 核心实现
│   │   │   ├── model/            # 模型定义
│   │   │   ├── config/           # 配置
│   │   │   └── utils/            # 工具函数
│   │   ├── chattts_infer.py      # ChatTTS 推理脚本
│   │   ├── params_chattts.json   # 默认参数
│   │   ├── requirements.txt      # Python 依赖
│   │   └── setup.py              # 安装脚本
│   │
│   └── rvc/                      # RVC 源码包
│       ├── infer/                # 推理模块
│       │   ├── modules/          # VC 模块
│       │   └── lib/              # 核心库
│       ├── assets/               # 资源文件
│       │   ├── hubert/           # HuBERT 模型
│       │   ├── rmvpe/            # RMVPE F0 提取器
│       │   └── indices/          # 检索索引
│       ├── configs/              # 配置文件
│       ├── rvc_infer_json.py     # RVC 推理脚本
│       └── requirements.txt      # Python 依赖
│
└── scripts/                      # 用户脚本 / User scripts
    ├── chattts_rvc_pipeline.py   # 联合推理管道
    ├── feishu_voice.py           # 飞书发送脚本
    └── bilibili_top20_task.py    # B站热门任务
```

---

## 开源引用 / Open Source

本项目使用了以下开源项目，遵循其相应的许可证：

This project uses the following open source projects under their respective licenses:

| 项目 / Project | 许可证 / License | 仓库 / Repository |
|---------------|-----------------|------------------|
| **ChatTTS** | BSD-3-Clause | https://github.com/2noise/ChatTTS |
| **RVC** | MIT | https://github.com/liujing04/Retrieval-based-Voice-Conversion |
| **PyTorch** | BSD-3-Clause | https://github.com/pytorch/pytorch |
| **FFmpeg** | LGPL/GPL | https://ffmpeg.org/ |

### ChatTTS 许可证声明

ChatTTS 使用 BSD-3-Clause 许可证。本项目包含 ChatTTS 源码的副本，遵循其许可证条款。

ChatTTS is licensed under BSD-3-Clause. This project includes a copy of ChatTTS source code, following its license terms.

### RVC 许可证声明

RVC 使用 MIT 许可证。本项目包含 RVC 源码的副本，遵循其许可证条款。

RVC is licensed under MIT. This project includes a copy of RVC source code, following its license terms.

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
