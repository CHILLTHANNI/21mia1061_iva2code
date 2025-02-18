
#Lab Task 1: Setup and Basic Extraction#

import ffmpeg

def get_video_info(video_path):
    try:
        probe = ffmpeg.probe(video_path)
        video_info = next(stream for stream in probe['streams'] if stream['codec_type'] == 'video')
        return {
            'width': video_info['width'],
            'height': video_info['height'],
            'duration': float(video_info['duration']),
            'frame_rate': eval(video_info['r_frame_rate']),
            'nb_frames': int(video_info['nb_frames']),
        }
    except ffmpeg.Error as e:
        print(f"Error: {e.stderr.decode('utf8')}")
        return None

# Example usage
video_path = '/Users/bharathvikram/Downloads/fotages/spark.mp4'
info = get_video_info(video_path)
if info:
    print("Video Information:")
    print(f"Width: {info['width']} pixels")
    print(f"Height: {info['height']} pixels")
    print(f"Duration: {info['duration']} seconds")
    print(f"Frame Rate: {info['frame_rate']} fps")
    print(f"Number of Frames: {info['nb_frames']}")


#------------------------------------------------------------------------------------------#

#Lab Task 2: Frame Type Analysis#

import subprocess
import json
import matplotlib.pyplot as plt

def extract_frame_info(video_path):
    try:
        # Run ffprobe to get frame type information
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'frame=pict_type',
            '-of', 'json',
            video_path
        ]
        
        # Execute the command and capture the output
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Parse the JSON output
        frames = json.loads(result.stdout)['frames']
        
        # Count the number of I, P, and B frames
        frame_counts = {'I': 0, 'P': 0, 'B': 0}
        for frame in frames:
            pict_type = frame['pict_type']
            frame_counts[pict_type] += 1
        
        # Calculate total frames
        total_frames = sum(frame_counts.values())
        
        # Calculate the percentage of each frame type
        frame_percentages = {key: (count / total_frames) * 100 for key, count in frame_counts.items()}
        
        return {
            'Frame Counts': frame_counts,
            'Frame Percentages': frame_percentages
        }
    
    except Exception as e:
        return {"error": str(e)}

# Example usage
video_path = '/Users/bharathvikram/Downloads/fotages/spark.mp4'  # Replace with the correct path
frame_info = extract_frame_info(video_path)
print(frame_info)

# Extract data for plotting
frame_counts = frame_info['Frame Counts']
frame_percentages = frame_info['Frame Percentages']

# Plotting the distribution
def plot_frame_distribution(frame_counts, frame_percentages):
    # Bar Chart
    plt.figure(figsize=(10, 5))
    
    # Plot frame counts
    plt.subplot(1, 2, 1)
    plt.bar(frame_counts.keys(), frame_counts.values(), color=['blue', 'green', 'red'])
    plt.title('Frame Type Counts')
    plt.xlabel('Frame Type')
    plt.ylabel('Count')
    
    # Plot frame percentages
    plt.subplot(1, 2, 2)
    plt.pie(frame_percentages.values(), labels=frame_percentages.keys(), autopct='%1.1f%%', colors=['blue', 'green', 'red'])
    plt.title('Frame Type Distribution (%)')
    
    plt.tight_layout()
    plt.show()

# Plot the results
plot_frame_distribution(frame_counts, frame_percentages)


#----------------------------------------------------------------------------------------#

#Lab Task 3: Visualizing Frames#

import subprocess
import os

def extract_frames(video_path, output_dir, frame_type):
    try:
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Define the ffmpeg command
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vf', f'select=eq(pict_type\\,{frame_type})',
            '-vsync', 'vfr',
            f'{output_dir}/frame_%04d.png'
        ]
        
        # Run the command
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        print(f"{frame_type} frames extracted successfully to {output_dir}")
    
    except Exception as e:
        print(f"Error extracting {frame_type} frames: {str(e)}")

# Example usage
video_path = '/Users/bharathvikram/Downloads/fotages/spark.mp4'  # Replace with the correct path

# Extract I frames
extract_frames(video_path, 'I_frames', 'I')

# Extract P frames
extract_frames(video_path, 'P_frames', 'P')

# Extract B frames
extract_frames(video_path, 'B_frames', 'B')


from PIL import Image
import os

def display_frames(frame_dir, frame_type):
    # Get the list of frame files
    frames = sorted([os.path.join(frame_dir, f) for f in os.listdir(frame_dir) if f.endswith('.png')])

    # Display each frame
    for frame_file in frames:
        img = Image.open(frame_file)
        img.show(title=f"{frame_type} Frame")

# Example usage
display_frames('I_frames', 'I')
display_frames('P_frames', 'P')
display_frames('B_frames', 'B')

def load_and_convert_to_array(frame_dir):
    """Load the first frame from the directory and convert it to a numpy array."""
    frame_files = sorted([f for f in os.listdir(frame_dir) if f.endswith('.png')])
    if frame_files:
        img = Image.open(os.path.join(frame_dir, frame_files[0]))
        return img
    else:
        return None



# Load frames
i_frame = load_and_convert_to_array('I_frames')
p_frame = load_and_convert_to_array('P_frames')
b_frame = load_and_convert_to_array('B_frames')

# Display frames side by side
def plot_frame_comparison(i_frame, p_frame, b_frame):
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    # Plot I-Frame
    if i_frame is not None:
        axs[0].imshow(i_frame)
        axs[0].set_title('I-Frame')
        axs[0].axis('off')

    # Plot P-Frame
    if p_frame is not None:
        axs[1].imshow(p_frame)
        axs[1].set_title('P-Frame')
        axs[1].axis('off')

    # Plot B-Frame
    if b_frame is not None:
        axs[2].imshow(b_frame)
        axs[2].set_title('B-Frame')
        axs[2].axis('off')

    plt.show()

# Visualize the comparison
plot_frame_comparison(i_frame, p_frame, b_frame)

#----------------------------------------------------------------------------------------#

#Lab Task 4: Frame Compression Analysis#

import os

def calculate_frame_sizes(directory):
    # List all PNG files in the directory
    frame_files = [f for f in os.listdir(directory) if f.endswith('.png')]
    
    # Calculate the size of each frame file
    frame_sizes = [os.path.getsize(os.path.join(directory, f)) for f in frame_files]
    
    # Calculate the total and average sizes
    total_size = sum(frame_sizes)
    average_size = total_size / len(frame_sizes) if frame_sizes else 0
    
    return total_size, average_size, len(frame_sizes)

def compare_frame_sizes():
    # Directories where frames are stored
    i_frames_dir = 'I_frames'
    p_frames_dir = 'P_frames'
    b_frames_dir = 'B_frames'
    
    # Calculate frame sizes for each type
    i_total_size, i_avg_size, i_count = calculate_frame_sizes(i_frames_dir)
    p_total_size, p_avg_size, p_count = calculate_frame_sizes(p_frames_dir)
    b_total_size, b_avg_size, b_count = calculate_frame_sizes(b_frames_dir)
    
    # Print results
    print(f"I Frames: {i_count} frames, Total Size: {i_total_size / 1024:.2f} KB, Average Size: {i_avg_size / 1024:.2f} KB")
    print(f"P Frames: {p_count} frames, Total Size: {p_total_size / 1024:.2f} KB, Average Size: {p_avg_size / 1024:.2f} KB")
    print(f"B Frames: {b_count} frames, Total Size: {b_total_size / 1024:.2f} KB, Average Size: {b_avg_size / 1024:.2f} KB")
    
    # Compare average sizes
    if i_avg_size > p_avg_size and i_avg_size > b_avg_size:
        print("I Frames have the largest average size, indicating lower compression.")
    if p_avg_size > i_avg_size and p_avg_size > b_avg_size:
        print("P Frames have the largest average size, indicating lower compression.")
    if b_avg_size > i_avg_size and b_avg_size > p_avg_size:
        print("B Frames have the largest average size, indicating lower compression.")

# Example usage
compare_frame_sizes()


#----------------------------------------------------------------------------------------#

#Lab Task 5: Advanced Frame Extraction#

import subprocess
import os

def extract_i_frames(video_path, output_dir):
    try:
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Define the ffmpeg command to extract I-frames
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vf', 'select=eq(pict_type\\,I)',
            '-vsync', 'vfr',
            f'{output_dir}/frame_%04d.png'
        ]

        # Run the command
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"I-frames extracted successfully to {output_dir}")
    
    except Exception as e:
        print(f"Error extracting I-frames: {str(e)}")

# Example usage
video_path = '/Users/bharathvikram/Downloads/fotages/MVI_1303.MP4'  # Replace with the correct path
i_frames_dir = 'I_frames'  # Directory to save I-frames

extract_i_frames(video_path, i_frames_dir)


def reconstruct_video_from_i_frames(i_frames_dir, output_video_path, frame_rate=1):
    try:
        # Define the ffmpeg command to reconstruct the video
        cmd = [
            'ffmpeg',
            '-framerate', str(frame_rate),  # Set the frame rate
            '-i', os.path.join(i_frames_dir, 'frame_%04d.png'),
            '-c:v', 'libx264',  # Use H.264 codec
            '-pix_fmt', 'yuv420p',
            output_video_path
        ]

        # Run the command
        subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print(f"Video reconstructed successfully and saved to {output_video_path}")
    
    except Exception as e:
        print(f"Error reconstructing video: {str(e)}")

# Example usage
output_video_path = 'reconstructed_video.mp4'  # Path to save the reconstructed video
reconstruct_video_from_i_frames(i_frames_dir, output_video_path, frame_rate=1)
