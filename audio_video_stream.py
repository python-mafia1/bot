# import requests
# import time
# import os
#
from check_audio_input import text_script

#
#
# def generate_video(text_script, API_KEY, VIDEO_SAVE_PATH):
#     url = "https://api.heygen.com/v2/video/generate"
#
#     headers = {
#         "X-Api-Key": API_KEY,
#         "Content-Type": "application/json"
#     }
#
#
    # data = {
    #     "video_inputs": [
    #         {
    #             "character": {
    #                 "type": "avatar",
    #                 "avatar_id": "Daisy-inskirt-20220818",
    #                 "avatar_style": "normal"
    #             },
    #             "voice": {
    #                 "type": "text",
    #                 "input_text": text_script,
    #                 "voice_id": "2d5b0e6cf36f460aa7fc47e3eee4ba54"
    #             },
    #             "background": {
    #                 "type": "color",
    #                 "value": "#008000"
    #             }
    #         }
    #     ],
    #     "dimension": {
    #         "width": 1280,
    #         "height": 720
    #     }
    # }
#
#     response = requests.post(url, headers=headers, json=data)
#
#     if response.status_code != 200:
#         print(f"Error {response.status_code}: {response.text}")
#         exit()
#
#     response_data = response.json()
#     print(response_data)
#
#     video_id = response_data.get("data", {}).get("video_id")
#     if not video_id:
#         print("Error: No video ID returned")
#         exit()
#
#     print(f"Video ID: {video_id}")
#
#     video_url = None
#     check_url = f"https://api.heygen.com/v1/video_status.get?video_id={video_id}"
#
#     while True:
#         status_response = requests.get(check_url, headers=headers)
#
#         if status_response.status_code != 200:
#             print(f"Error fetching status: {status_response.status_code}")
#             print(status_response.text)
#             exit()
#
#         try:
#             status_data = status_response.json()
#         except requests.exceptions.JSONDecodeError:
#             print("Error: Empty or invalid response from API.")
#             exit()
#
#         video_status = status_data.get("data", {}).get("status")
#
#         if video_status == "completed":
#             video_url = status_data.get("data", {}).get("video_url")
#             print(f"Video ready: {video_url}")
#             break
#         elif video_status == "failed":
#             print("Video generation failed!")
#             exit()
#         else:
#             print("Processing video...")
#             time.sleep(10)
#
#
#     if video_url:
#         os.makedirs(VIDEO_SAVE_PATH, exist_ok=True)
#
#         video_filename = f"{VIDEO_SAVE_PATH}/{video_id}.mp4"
#
#         print(f"Downloading video to {video_filename}...")
#
#         video_response = requests.get(video_url, stream=True)
#         if video_response.status_code == 200:
#             with open(video_filename, "wb") as f:
#                 for chunk in video_response.iter_content(1024):
#                     f.write(chunk)
#             print(f"Video saved: {video_filename}")
#         else:
#             print(f"Failed to download video, status: {video_response.status_code}")
#
#
# API_KEY = "NDIwN2M1MjQwNTJiNGM0MTgwOGVjOGZlMzY5MzZjZGUtMTczODIxOTc0MQ=="
# VIDEO_SAVE_PATH = "video"
#
# generate_video(text_script, API_KEY, VIDEO_SAVE_PATH)


import os
import subprocess
import cv2
import pyaudio
import wave
import threading
import pyvirtualcam


# video_path = f"video/{video_id}.mp4"
video_path = "video/2b9c0044a2274c9897d4ea0143489069.mp4"
audio_output_path = "audio_video_stream/audio_stream.wav"
video_output_path = "audio_video_stream/video_output.mp4"

def extract_audio(video_path, audio_output_path):
    command = [
        'ffmpeg', '-i', video_path, '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2', audio_output_path
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def extract_video(video_path, video_output_path):
    command = ['ffmpeg', '-i', video_path, '-map', '0:v', '-c:v', 'copy', '-an', video_output_path]

    # Run FFmpeg
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


extract_video(video_path, video_output_path)
extract_audio(video_path, audio_output_path)

def play_audio(audio_path):
    wf = wave.open(audio_path, 'rb')
    p = pyaudio.PyAudio()

    # Open a stream to play the audio
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # Read and play the audio
    chunk_size = 1024
    data = wf.readframes(chunk_size)
    while data:
        stream.write(data)
        data = wf.readframes(chunk_size)

    # Close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

# Play Video using OpenCV
def play_video(video_path):
    # cap = cv2.VideoCapture(video_path)
    # with pyvirtualcam.Camera(width=640, height=480, fps=30) as cam:
    #     while True:
    #         ret, frame = cap.read()
    #         if not ret:
    #             break
    #
    #         desired_width = 640
    #         desired_height = 480
    #         frame = cv2.resize(frame, (desired_width, desired_height))
    #         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #         cam.send(frame)
    #         cam.sleep_until_next_frame()
    # cap.release()

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_delay = int(1000 / fps)


    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Video', frame)

        if cv2.waitKey(frame_delay) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()




video_thread = threading.Thread(target=play_video, args=(video_output_path,))
audio_thread = threading.Thread(target=play_audio, args=(audio_output_path,))

video_thread.start()
audio_thread.start()

video_thread.join()
audio_thread.join()

print("Audio and Video playback finished.")
if os.path.exists(audio_output_path):
    os.remove(audio_output_path)
    print(f"Deleted {audio_output_path}")

if os.path.exists(video_output_path):
    os.remove(video_output_path)
    print(f"Deleted {video_output_path}")
