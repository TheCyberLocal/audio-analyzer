"""
This Python script is designed to stream audio data from a microphone in real-time,
 converting the binary audio data into integers for visualization.
The data is visualized as an audio waveform using matplotlib.
The script provides a real-time view of the audio signal captured by the microphone.
It's a practical application of Python in audio processing and real-time data visualization.
"""

import pyaudio  # Importing the PyAudio library for accessing the microphone.
import struct  # Importing struct for converting binary data to integers.
import numpy as np  # Importing NumPy for numerical operations on data.
import matplotlib.pyplot as plt  # Importing Matplotlib for plotting the audio waveform.
import time  # Importing the time module for timing the frame rate.
from tkinter import TclError  # Importing TclError to handle potential GUI errors.

# Setting up constants for audio streaming.
CHUNK = 1024 * 2             # Defining the number of audio samples per frame (2048 samples).
FORMAT = pyaudio.paInt16     # Audio format set to 16-bit integer.
CHANNELS = 1                 # Single audio channel for the microphone.
RATE = 44100                 # Defining the sample rate as 44100 samples per second.

# Creating a matplotlib figure and axis for displaying the waveform.
fig, ax = plt.subplots(1, figsize=(10, 5))

# Creating an instance of PyAudio to handle the audio stream.
p = pyaudio.PyAudio()

# Opening a stream to capture audio data from the microphone.
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)

# Creating an array for the x-axis of the plot (time/sample points).
x = np.arange(0, 2 * CHUNK, 2)
# Initializing the line object for the plot with random data.
line, = ax.plot(x, np.random.rand(CHUNK), '-', lw=1)

# Setting up the plot with titles, labels, and axis limits.
ax.set_title('AUDIO WAVEFORM')
ax.set_xlabel('samples')
ax.set_ylabel('volume')
ax.set_ylim(0, 255)
ax.set_xlim(0, 2 * CHUNK)
plt.setp(ax, xticks=[0, CHUNK, 2 * CHUNK], yticks=[0, 128, 255])

# Displaying the plot in a non-blocking way.
plt.show(block=False)

print('stream started')  # Printing to console that the stream has started.

# Variables for calculating the frame rate.
frame_count = 0
start_time = time.time()

while True:
    data = stream.read(CHUNK)  # Reading a chunk of data from the stream.
    # Unpacking the binary data to integers.
    data_int = struct.unpack(str(2 * CHUNK) + 'B', data)
    # Converting data to a numpy array and offsetting by 128.
    data_np = np.array(data_int, dtype='b')[::2] + 128
    line.set_ydata(data_np)  # Updating the data of the line plot.

    try:
        fig.canvas.draw()  # Redrawing the canvas.
        fig.canvas.flush_events()  # Processing GUI events.
        frame_count += 1  # Incrementing the frame count.
    except TclError:
        # Calculating the average frame rate.
        frame_rate = frame_count / (time.time() - start_time)
        print('stream stopped')  # Indicating that the stream has stopped.
        print('average frame rate = {:.0f} FPS'.format(frame_rate))  # Printing the average frame rate.
        break  # Breaking the loop to end the program.
