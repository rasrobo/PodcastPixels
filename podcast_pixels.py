import argparse
import os
import logging
import tempfile
import shutil
from typing import List

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def _build_ffmpeg_params(crf: int, faststart: bool, pixel_format: str) -> List[str]:
    """
    Build ffmpeg params for MoviePy write_videofile.
    """
    params: List[str] = ["-crf", str(crf), "-pix_fmt", pixel_format]
    if faststart:
        params += ["-movflags", "+faststart"]
    return params

def validate_paths(audio_path, output_directory):
    """
    Validate input and output paths
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        logging.info(f"Created output directory: {output_directory}")

def create_simple_video(
    audio_path,
    output_path,
    output_format='mp4',
    fps=24,
    preset='faster',
    crf=23,
    threads: int = 0,
    audio_bitrate: str = '128k',
    faststart: bool = True,
    pixel_format: str = 'yuv420p',
):
    """
    Convert audio to a simple video with a blank background
    """
    # Lazy imports to reduce CLI startup time and optional install footprint
    try:
        from tqdm import tqdm
        from moviepy.audio.io.AudioFileClip import AudioFileClip
        from moviepy.video.VideoClip import ColorClip
    except ImportError as import_error:
        logging.error("Missing dependencies. Install with: pip install -r requirements.txt")
        raise
    # Validate paths
    output_directory = os.path.dirname(output_path)
    validate_paths(audio_path, output_directory)
    
    logging.info(f"Creating simple video from audio: {audio_path}")
    
    try:
        # Load the audio file with progress indicator
        logging.info("Loading audio file...")
        with tqdm(desc="Loading audio", total=1) as pbar:
            audio = AudioFileClip(audio_path)
            pbar.update(1)

        # Create a blank black video clip
        logging.info("Creating video clip...")
        with tqdm(desc="Creating video", total=1) as pbar:
            blank_clip = ColorClip(size=(1280, 720), color=(0, 0, 0), duration=audio.duration)
            pbar.update(1)

        # Combine audio and video
        logging.info("Combining audio and video...")
        with tqdm(desc="Combining", total=1) as pbar:
            video = blank_clip.with_audio(audio)
            pbar.update(1)

        ffmpeg_params = _build_ffmpeg_params(crf=crf, faststart=faststart, pixel_format=pixel_format)

        # Preferred: write directly to the destination
        logging.info("Writing video file (direct)...")
        write_kwargs = {
            "fps": fps,
            "codec": "libx264",
            "audio_codec": "aac",
            "preset": preset,
            "ffmpeg_params": ffmpeg_params,
            "audio_bitrate": audio_bitrate,
            "logger": 'bar',
        }
        if threads and threads > 0:
            write_kwargs["threads"] = threads

        try:
            video.write_videofile(output_path, **write_kwargs)
        except Exception as direct_error:
            logging.warning(f"Direct write failed ({direct_error}). Falling back to temp file then copy...")
            # Fallback: write to a temp file then copy
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_output_path = os.path.join(temp_dir, f'temp_video.{output_format}')
                video.write_videofile(temp_output_path, **write_kwargs)

                logging.info("Moving to final location...")
                with tqdm(desc="Finalizing", total=1) as pbar:
                    try:
                        shutil.copy2(temp_output_path, output_path)
                        logging.info(f"Video saved to: {output_path}")
                    except PermissionError:
                        logging.warning(f"Permission denied when writing to {output_path}")
                        # Try alternative locations for WSL compatibility
                        fallback_locations = [
                            os.path.join(os.path.expanduser("~"), "podcastpixels_output.mp4"),
                            os.path.join("/tmp", "podcastpixels_output.mp4"),
                            os.path.join(os.getcwd(), "podcastpixels_output.mp4")
                        ]

                        for fallback_path in fallback_locations:
                            try:
                                shutil.copy2(temp_output_path, fallback_path)
                                logging.info(f"Video saved to fallback location: {fallback_path}")
                                output_path = fallback_path
                                break
                            except Exception as fallback_error:
                                logging.debug(f"Fallback location {fallback_path} failed: {fallback_error}")
                                continue
                        else:
                            logging.error("All output locations failed. Check permissions and try again.")
                            raise PermissionError("Could not write to any location. Try specifying --output_path with a writable directory.")
                    except OSError as e:
                        logging.error(f"Failed to copy file: {str(e)}")
                        raise
                    pbar.update(1)

        # Clean up
        audio.close()
        video.close()

        logging.info(f"Simple video created: {output_path}")

    except Exception as e:
        logging.error(f"Error during video creation: {str(e)}")
        raise

def create_audio_visualization(audio_path, output_path, vis_type, output_format='mp4'):
    """
    Create an audio visualization video
    """
    logging.warning(f"Visualization type '{vis_type}' not implemented yet")
    create_simple_video(audio_path, output_path, output_format)

def parse_arguments():
    # Supported video formats
    supported_formats = ['mp4', 'mov', 'mpeg1', 'mpeg2', 'mpeg4', 'mpg', 'avi', 'wmv', 'mpegps', 'flv', '3gpp', 'webm']
    
    parser = argparse.ArgumentParser(description='Convert audio to video')
    parser.add_argument('audio_path', type=str, help='Path to the input audio file')
    parser.add_argument('--output_path', type=str, help='Path to the output video file (optional)')
    parser.add_argument('--format', type=str, choices=supported_formats, default='mp4',
                        help='Output video format (default: mp4)')
    parser.add_argument('--vis_type', type=str, choices=['waveform', 'spectrogram', 'circular', 'bar_graph'],
                        help='Create a visualization video instead of a simple conversion')
    parser.add_argument('--fps', type=int, default=24, help='Frames per second (default: 24)')
    parser.add_argument('--preset', type=str, default='faster', choices=[
        'ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow'
    ], help='x264 preset for speed/quality tradeoff (default: faster)')
    parser.add_argument('--crf', type=int, default=23, help='Constant Rate Factor 0-51, lower is better quality (default: 23)')
    parser.add_argument('--threads', type=int, default=0, help='FFmpeg threads (0=auto)')
    parser.add_argument('--audio_bitrate', type=str, default='128k', help='AAC audio bitrate (default: 128k)')
    parser.add_argument('--pixel_format', type=str, default='yuv420p', choices=['yuv420p', 'yuv444p', 'yuv420p10le'], help='Pixel format (default: yuv420p)')
    faststart_group = parser.add_mutually_exclusive_group()
    faststart_group.add_argument('--faststart', dest='faststart', action='store_true', help='Enable MP4 faststart (moov atom at beginning)')
    faststart_group.add_argument('--no-faststart', dest='faststart', action='store_false', help='Disable MP4 faststart')
    parser.set_defaults(faststart=True)
    return parser.parse_args()

if __name__ == "__main__":
    try:
        args = parse_arguments()
        
        # Get the input audio file path
        audio_path = args.audio_path
        
        # If no output path is specified, set the output path to the same directory as the source file
        if args.output_path:
            output_path = args.output_path
        else:
            # Always save in the same directory as the source file
            output_directory = os.path.dirname(audio_path)
            
            # Use the selected format for the output file extension
            output_filename = os.path.splitext(os.path.basename(audio_path))[0] + '.' + args.format
            output_path = os.path.join(output_directory, output_filename)
            logging.info(f"Output will be saved to: {output_path}")
        
        # Create video based on visualization flag
        if args.vis_type:
            create_audio_visualization(audio_path, output_path, args.vis_type, args.format)
        else:
            create_simple_video(
                audio_path,
                output_path,
                args.format,
                fps=args.fps,
                preset=args.preset,
                crf=args.crf,
                threads=args.threads,
                audio_bitrate=args.audio_bitrate,
                faststart=args.faststart,
                pixel_format=args.pixel_format,
            )
        
        logging.info("Script completed successfully")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise
