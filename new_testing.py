import pyaudio
import wave

audio_path = "audio_stream.wav"

# Open the audio file
wf = wave.open(audio_path, 'rb')

# Initialize PyAudio
p = pyaudio.PyAudio()
device_index = 0

# Open an audio stream
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                output_device_index = device_index)

# Read and play the audio file
data = wf.readframes(1024)
while data:
    stream.write(data)
    data = wf.readframes(1024)

# Cleanup
stream.stop_stream()
stream.close()
p.terminate()
wf.close()
print("Audio played successfully.")
