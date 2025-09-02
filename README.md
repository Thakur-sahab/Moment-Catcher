# Moment Catcher - Automatic Trailer Generator

🎬 **Transform your videos into exciting trailers automatically!**

Moment Catcher is an AI-powered web application that analyzes videos and automatically generates compelling trailers by detecting and combining the most engaging moments. Using advanced audio, visual, and motion analysis, it identifies exciting segments and creates professional-quality trailers in minutes.

## ✨ Features

- **🎯 Smart Moment Detection**: AI algorithms analyze audio energy, visual motion, edge density, and color variance
- **🎬 Automatic Trailer Generation**: Intelligently combines the most exciting moments into cohesive trailers
- **🌐 Web Interface**: Beautiful, responsive web UI for easy video upload and preview
- **📊 Detailed Analytics**: View detected moments with timestamps and excitement scores
- **💾 Multiple Export Formats**: Download trailers in various video formats
- **⚡ Fast Processing**: Optimized algorithms for quick video analysis and generation

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- FFmpeg (for video processing)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd moment-catcher
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install FFmpeg** (if not already installed)
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```
   
   **macOS:**
   ```bash
   brew install ffmpeg
   ```
   
   **Windows:**
   Download from [FFmpeg official website](https://ffmpeg.org/download.html)

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 🎮 How to Use

1. **Upload Video**: Drag and drop or click to select your video file (max 500MB)
2. **Generate Trailer**: Click "Generate Trailer" to start the AI analysis
3. **Review Results**: View detected moments and trailer statistics
4. **Download**: Get your automatically generated trailer

## 🔧 Technical Details

### Algorithm Overview

The moment detection algorithm combines multiple analysis techniques:

1. **Audio Analysis**
   - Energy levels
   - Zero crossing rate
   - Spectral centroid

2. **Visual Analysis**
   - Motion detection between frames
   - Edge density (complexity)
   - Brightness variance
   - Color variance

3. **Moment Selection**
   - Peak detection in excitement scores
   - Temporal clustering to avoid redundancy
   - Score-based ranking and selection

### Architecture

```
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Web interface
├── static/
│   ├── css/style.css     # Styling
│   └── js/app.js         # Frontend JavaScript
├── uploads/              # Temporary video storage
├── outputs/              # Generated trailers
└── requirements.txt      # Python dependencies
```

## 🛠️ Configuration

### Environment Variables

- `MAX_CONTENT_LENGTH`: Maximum file upload size (default: 500MB)
- `UPLOAD_FOLDER`: Directory for temporary uploads (default: 'uploads')
- `OUTPUT_FOLDER`: Directory for generated trailers (default: 'outputs')

### Customization

You can modify the moment detection parameters in `app.py`:

```python
# Adjust these parameters in the detect_moments method
num_moments = 10          # Number of moments to detect
moment_duration = 3.0     # Duration of each moment in seconds
max_duration = 30         # Maximum trailer length in seconds
```

## 📊 API Endpoints

- `GET /`: Main web interface
- `POST /upload`: Upload and process video
- `GET /download/<filename>`: Download generated trailer

## 🎯 Use Cases

- **Content Creators**: Generate highlight reels from long-form content
- **Event Organizers**: Create event trailers from footage
- **Sports Teams**: Extract exciting moments from game footage
- **Social Media**: Create engaging clips for platforms
- **Marketing**: Generate promotional trailers from product demos

## 🔍 Troubleshooting

### Common Issues

1. **FFmpeg not found**
   - Ensure FFmpeg is installed and in your PATH
   - Restart your terminal after installation

2. **Large file uploads fail**
   - Check file size limit (500MB default)
   - Ensure sufficient disk space

3. **Video processing errors**
   - Verify video format is supported
   - Check video file integrity

### Performance Tips

- Use compressed video formats for faster processing
- Ensure adequate RAM for large video files
- Close other applications during processing

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenCV for computer vision capabilities
- MoviePy for video processing
- Librosa for audio analysis
- Flask for the web framework
- Bootstrap for the UI framework

---

**Built with ❤️ and AI**