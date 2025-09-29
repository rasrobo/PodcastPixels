# PodcastPixels

## Overview
PodcastPixels is a versatile audio-to-video conversion tool that transforms audio files into MP4 videos with optional visualization features.

## Features
- Simple audio to video conversion
- YouTube upload preparation
- Supports multiple audio formats
- Flexible output configuration
- Progress indicators for conversion process
- Optimized for quick audio-to-video conversion
- Minimal processing overhead

## Installation
```bash
git clone https://github.com/rasrobo/PodcastPixels.git
cd PodcastPixels
python3 -m venv podcast_pixels_env
source podcast_pixels_env/bin/activate
pip install -r requirements.txt
```

### Optional extras for visualizations
Some visualizations may require additional libraries. Install optional extras only if you need them:
```bash
pip install matplotlib pillow numpy
```

## Usage
### Basic Audio to Video Conversion
```bash
python podcast_pixels.py /path/to/your/audio/file.mp3
```

### With Visualizations
```bash
# Waveform visualization
python podcast_pixels.py /path/to/audio.mp3 --vis_type waveform

# Spectrogram visualization
python podcast_pixels.py /path/to/audio.mp3 --vis_type spectrogram

# Circular visualization
python podcast_pixels.py /path/to/audio.mp3 --vis_type circular

# Bar graph visualization
python podcast_pixels.py /path/to/audio.mp3 --vis_type bar_graph
```

### Custom Output Path
```bash
python podcast_pixels.py /path/to/audio.mp3 --output_path /custom/path/output.mp4
```

### Performance/quality flags
```bash
# Faster encode, smaller file, web-friendly
python podcast_pixels.py input.mp3 \
  --fps 24 \
  --preset faster \
  --crf 23 \
  --threads 0 \
  --audio_bitrate 128k \
  --pixel_format yuv420p \
  --faststart
```

## Requirements
- Python 3.7+
- MoviePy
- tqdm (for progress bars)
- Optional: NumPy, Matplotlib, Pillow (for advanced visualizations)

## Roadmap
- Implement basic visual components
- Improve video writing performance
- Add parallel processing capabilities
- Develop user-friendly GUI
- Static image background
- Color gradient animations
- Text overlay options

## Contribution
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Performance Tracking
- Monitor video conversion times
- Track file size transformations
- Log processing steps for debugging

## License
MIT License

## Donations
**Note:** This project is actively developed with a "eat your own dog food" approach, ensuring practical and user-focused improvements.

If you find this code useful and would like to support its development, you can buy me a coffee! Your support is greatly appreciated.

[![Buy Me A Coffee](https://cdn.buymeacoffee.com/buttons/default-orange.png)](https://buymeacoffee.com/robodigitalis)