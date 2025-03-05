import time
import os
import subprocess
import RPi.GPIO as GPIO
from datetime import datetime
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from picamera2.outputs import FileOutput

# GPIO setup
PIR_PIN = 6  # GPIO pin for PIR sensor
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

# Directory for saving videos
VIDEO_DIR = '/home/iot/Videos'
if not os.path.exists(VIDEO_DIR):
    os.makedirs(VIDEO_DIR)

# Initialize Picamera2 once
picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)
encoder = H264Encoder()

# Function to record video
def record_video():
    # Generate timestamped filename
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    h264_filename = f"tiger_video_{current_time}.h264"
    mp4_filename = f"tiger_video_{current_time}.mp4"
    h264_path = os.path.join(VIDEO_DIR, h264_filename)
    mp4_path = os.path.join(VIDEO_DIR, mp4_filename)

    try:
        print(f"Recording video: {h264_path}")
        output = FileOutput(h264_path)
        picam2.start_preview(Preview.QTGL)
        time.sleep(2)  # Camera warm-up

        # Start recording
        picam2.start_recording(encoder, output)
        time.sleep(6)  # Record for 6 seconds
        picam2.stop_recording()
        picam2.stop_preview()
        print(f"Video saved: {h264_path}")

        # Convert to MP4 using ffmpeg
        subprocess.run(['ffmpeg', '-framerate', '30', '-i', h264_path, '-c', 'copy', mp4_path], check=True)
        print(f"Video converted to MP4: {mp4_path}")
        os.remove(h264_path)  # Remove raw H.264 file

    except Exception as e:
        print(f"Error recording video: {e}")

try:
    print("Waiting for motion...")
    while True:
        if GPIO.input(PIR_PIN):  # Motion detected
            print("Motion detected! Recording video...")
            record_video()

            # Wait until motion stops
            while GPIO.input(PIR_PIN):
                time.sleep(0.1)

            print("Motion ended. Waiting for new motion...")

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting program...")

finally:
    GPIO.cleanup()
    picam2.close()  # Release camera resources
