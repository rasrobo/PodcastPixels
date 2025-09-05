import numpy as np
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import ColorClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
import argparse
import os
import logging
import tempfile
import shutil
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def validate_paths(audio_path, output_directory):
    """
    Validate input and output paths
    """
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        logging.info(f"Created output directory: {output_directory}")

def create_simple_video(audio_path, output_path, output_format='mp4'):
    """
    Convert audio to a simple video with a blank background
    """
    # Validate paths
    output_directory = os.path.dirname(output_path)
    validate_paths(audio_path, output_directory)
    
    # Use system's temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Generate a temporary output path in the system's temp directory
        temp_output_path = os.path.join(temp_dir, f'temp_video.{output_format}')
        
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
            
            # Write the video file to the temporary location
            logging.info("Writing video file...")
            video.write_videofile(temp_output_path, fps=30, logger='bar')
            
            # Move the temporary file to the final output location
            logging.info("Moving to final location...")
            with tqdm(desc="Finalizing", total=1) as pbar:
                try:
                    shutil.copy2(temp_output_path, output_path)
                    logging.info(f"Video saved to: {output_path}")
                except PermissionError:
                    logging.warning(f"Permission denied when writing to {output_path}")
                    # Try alternative locations for WSL compatibility
                    fallback_locations = [
                        os.path.join(os.path.expanduser("~"), "danyoga41.mp4"),
                        os.path.join("/tmp", "danyoga41.mp4"),
                        os.path.join(os.getcwd(), "danyoga41.mp4")
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
                        raise PermissionError(f"Could not write to any location. Try specifying --output_path with a writable directory.")
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
            create_simple_video(audio_path, output_path, args.format)
        
        logging.info("Script completed successfully")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise
