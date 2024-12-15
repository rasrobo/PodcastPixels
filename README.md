# PodcastPixels

## Overview
PodcastPixels is a versatile audio-to-video conversion tool that allows you to transform audio files into MP4 videos with optional visualization features.

## Features
- Simple audio to video conversion
- Optional audio visualization types
- Supports multiple audio formats
- Customizable output options

## Installation
```bash
git clone https://github.com/rasrobo/PodcastPixels.git
cd PodcastPixels
python3 -m venv podcast_pixels_env
source podcast_pixels_env/bin/activate
pip install -r requirements.txt
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

## Visualization Types
- `waveform`: Displays audio amplitude over time
- `spectrogram`: Shows frequency intensity
- `circular`: Radial frequency representation
- `bar_graph`: Frequency magnitude bars

## Requirements
- Python 3.7+
- MoviePy
- NumPy
- Matplotlib

## License
MIT License

## Donations

If you find this code useful and would like to support its development, you can buy me a coffee! Your support is greatly appreciated.

[![Buy Me A Coffee](https://cdn.buymeacoffee.com/buttons/default-orange.png)](https://buymeacoffee.com/robodigitalis)
