# Background Remover for Documents, Tables, and Diagrams

A Python script that intelligently removes white backgrounds from images while preserving text, tables, diagrams, and fine details like lines and arrows. Perfect for document scanning, preprocessing for OCR, or creating transparent PNGs from technical illustrations.

## 🎯 Features

- **Targeted White Removal**: Only removes white/light backgrounds, keeps dark content intact
- **Preserves Fine Details**: Maintains thin table lines, diagram arrows, and small text
- **Multiple Processing Modes**:
  - Simple mode for quick results
  - Advanced mode with HSV color detection for better gradient handling
- **Batch Processing**: Process entire folders of images automatically
- **Preview Mode**: Test different thresholds to find optimal settings
- **Smart Detection**: Automatically handles anti-aliasing and smooths edges
- **Statistics**: Shows percentage of image made transparent

## 📋 Requirements

```
opencv-python
numpy
pillow
```

Install with:
```bash
pip install opencv-python numpy pillow
```

## 🚀 Usage

### Basic Usage
```bash
# Process a single image
python bg_remover.py image.jpg -o output.png

# Process all images in a folder
create a folder called images and fill it with all your images then in your terminal enter :
python bg_remover.py ./images -o ./results

```

### Advanced Options
```bash
# Adjust white detection threshold (higher = more conservative)
python bg_remover.py ./images -o ./results -t 220

# Adjust tolerance for near-white colors
python bg_remover.py ./images -o ./results --tolerance 40

# Use advanced HSV-based detection for better gradient handling
python bg_remover.py ./images -o ./results --mode advanced

# Preview different settings to find optimal parameters
python bg_remover.py problem_image.jpg --preview
```

### Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `-t, --threshold` | White threshold (0-255). Lower = more aggressive | 200 |
| `--tolerance` | Tolerance for near-white detection | 30 |
| `--mode` | Processing mode: 'simple' or 'advanced' | 'simple' |
| `--preview` | Generate previews with different settings | False |

## 📊 How It Works

1. **White Detection**: Identifies white and near-white pixels using thresholding and color space analysis
2. **Content Preservation**: Ensures dark elements (text, lines, diagrams) remain opaque
3. **Alpha Channel Creation**: Converts detected white areas to transparent
4. **Edge Smoothing**: Applies Gaussian blur for cleaner edges and anti-aliasing
5. **Statistics**: Reports percentage of image made transparent

## 🖼️ Best Results With

- Scanned documents with white backgrounds
- Technical diagrams and schematics
- Tables and charts
- Black text on white background
- Line art and illustrations

## ⚡ Tips for Best Results

1. **Start with preview mode** on a representative image to find optimal settings
2. **Adjust threshold** based on paper quality:
   - Clean white paper: higher threshold (220-240)
   - Slightly yellowed/dark paper: lower threshold (180-200)
3. **Increase tolerance** for images with gradients or shadows
4. **Use advanced mode** for photos of documents with uneven lighting

## 📁 Output

- Saves images as PNG with transparency
- Maintains original image dimensions and quality
- Creates organized folder structure for batch processing
- Generates preview folder when testing thresholds

## 🔧 Troubleshooting

**Problem**: Text or lines disappear
- **Solution**: Increase threshold value (`-t 220` or higher)

**Problem**: White background remains
- **Solution**: Decrease threshold (`-t 180`) or increase tolerance

**Problem**: Rough edges around text
- **Solution**: Use advanced mode for better edge smoothing

**Problem**: Colored background not removed
- **Solution**: Adjust tolerance or use advanced HSV mode

## 📝 License

MIT License - feel free to use and modify for your projects.

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional color space detection methods
- Machine learning integration for smarter background detection
- GUI interface
- Support for more image formats

## ⭐ Support

If you find this tool useful, please star the repository! For issues or suggestions, open a GitHub issue.
