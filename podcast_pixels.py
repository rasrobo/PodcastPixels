import numpy as np
from moviepy.editor import ColorClip, AudioFileClip
import argparse
import os
import logging
import tempfile
import shutil

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

def create_simple_video(audio_path, output_path):
    """
    Convert audio to a simple video with a blank background
    """
    # Validate paths
    output_directory = os.path.dirname(output_path)
    validate_paths(audio_path, output_directory)
    
    # Use system's temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Generate a temporary output path in the system's temp directory
        temp_output_path = os.path.join(temp_dir, 'temp_video.mp4')
        
        logging.info(f"Creating simple video from audio: {audio_path}")
        
        try:
            # Load the audio file
            audio = AudioFileClip(audio_path)
            
            # Create a blank black video clip with the same duration as the audio
            blank_clip = ColorClip(size=(1280, 720), color=(0, 0, 0), duration=audio.duration)
            
            # Set the audio
            video = blank_clip.set_audio(audio)
            
            # Write the video file to the temporary location
            video.write_videofile(temp_output_path, fps=30, logger=None)
            
            # Copy the temporary file to the final output location
            shutil.copy(temp_output_path, output_path)
            
            # Clean up
            audio.close()
            video.close()
            
            logging.info(f"Simple video created: {output_path}")
            
        except Exception as e:
            logging.error(f"Error during video creation: {str(e)}")
            raise

def create_audio_visualization(audio_path, output_path, vis_type):
    """
    Create an audio visualization video
    """
    logging.warning(f"Visualization type '{vis_type}' not implemented yet")
    create_simple_video(audio_path, output_path)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Convert audio to video')
    parser.add_argument('audio_path', type=str, help='Path to the input audio file')
    parser.add_argument('--output_path', type=str, help='Path to the output video file (optional)')
    parser.add_argument('--vis_type', type=str, choices=['waveform', 'spectrogram', 'circular', 'bar_graph'],
                        help='Create a visualization video instead of a simple conversion')
    return parser.parse_args()

if __name__ == "__main__":
    try:
        args = parse_arguments()
        
        # Get the input audio file path
        audio_path = args.audio_path
        
        # If no output path is specified, set the output path to the same directory as the input audio file
        if args.output_path:
            output_path = args.output_path
        else:
            output_directory = os.path.dirname(audio_path)
            output_filename = os.path.splitext(os.path.basename(audio_path))[0] + '.mp4'
            output_path = os.path.join(output_directory, output_filename)
        
        # Create video based on visualization flag
        if args.vis_type:
            create_audio_visualization(audio_path, output_path, args.vis_type)
        else:
            create_simple_video(audio_path, output_path)
        
        logging.info("Script completed successfully")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise
