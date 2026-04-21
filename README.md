# ID ID-Remover (SynthID Remover)

A Flask-based web tool to strip SynthID AI watermarks from generated imagery.

## Features

- Upload PNG / JPG / WEBP images
- Removes SynthID neural watermarks from AI-generated images
- Cyberpunk-themed UI with real-time terminal log
- Drag & drop or click-to-upload interface
- One-click download of the clean image

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python app.py
```

Then open your browser at: `http://localhost:5000`

1. Drop or select your AI-generated image
2. Click **REMOVE SYNTHID WATERMARK**
3. Download the processed clean image

## Requirements

- Python 3.8+
- Flask 3.0+
- requests 2.31+

## Developer

Developed by **Tofazzal Hossain**

## License

MIT License
