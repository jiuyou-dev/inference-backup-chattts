# Packages

This directory contains the core source code for ChatTTS and RVC frameworks.

## Structure

```
packages/
├── chatttts/     # ChatTTS text-to-speech framework
└── rvc/          # RVC (Retrieval-Based Voice Conversion) framework
```

## ChatTTTS

ChatTTS is a neural network-based text-to-speech framework with natural prosody.

### Key Files
- `ChatTTS/` - Core TTS implementation
- `tools/` - Utility tools (audio processing, logging, etc.)
- `config/` - Configuration files
- `asset/` - Model assets (GPT, tokenizer)
- `chattts_infer.py` - Inference script
- `params_chattts.json` - Default parameters

### Requirements
- Python 3.8+
- PyTorch 2.0+
- ChatTTS model files (downloaded separately)

## RVC

RVC (Retrieval-Based Voice Conversion) is a voice timbre conversion framework.

### Key Files
- `infer/` - Core inference implementation
- `tools/` - Utility tools
- `configs/` - Configuration files
- `assets/` - Model assets (hubert, rmvpe, uvr5)
- `rvc_infer_json.py` - JSON-based inference script
- `run_rvc.bat` - Quick start script

### Requirements
- Python 3.11+
- CUDA-capable GPU
- RVC model files (.pth) - downloaded separately
- FFmpeg

## Note

Model files (.pth) are NOT included due to their large size. Download them separately from:
- RVC voice models: Various sources (community sharing)
- ChatTTS models: Hugging Face or official releases

## Installation

### ChatTTS
```bash
cd chatttts
pip install -r requirements.txt
python setup.py install
```

### RVC
```bash
cd rvc
pip install -r requirements.txt
```

## Usage

See the main README.md in the repository root for the complete voice generation pipeline.
