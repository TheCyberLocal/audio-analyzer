"""
This Python script is a sophisticated tool for real-time audio processing and visualization.
It captures audio from a microphone, performs a Fast Fourier Transform (FFT) for frequency analysis,
and visualizes both the audio waveform and its spectrum using Matplotlib.
"""

import pyaudio  # Importing the PyAudio library to access microphone data.
import struct  # Importing struct for binary data manipulation.
import numpy as np  # Importing NumPy for numerical operations.
import matplotlib.pyplot as plt  # Importing Matplotlib for data visualization.
from scipy.fftpack import fft  # Importing fft from SciPy for Fast Fourier Transform.
import time  # Importing time for tracking the frame rate.
from tkinter import TclError  # Importing TclError for handling GUI-related exceptions.

CHUNK = 1024 * 2  # Number of audio samples per frame (2048).
FORMAT = pyaudio.paInt16  # Audio format (16-bit integer).
CHANNELS = 1  # Single audio channel (mono).
RATE = 44100  # Sampling rate in Hz.

fig, (ax1, ax2) = plt.subplots(2, figsize=(15, 8))  # Creating two subplots for waveform and spectrum.

p = pyaudio.PyAudio()  # Creating a PyAudio instance.

# Opening an audio stream with specified parameters.
stream = p.open(
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    input=True,
    output=True,
    frames_per_buffer=CHUNK
)

x = np.arange(0, 2 * CHUNK, 2)  # Creating an array for the waveform x-axis.
x_fft = np.linspace(0, RATE, CHUNK)  # Creating an array for the spectrum x-axis.

# Creating line objects for waveform and spectrum, initially with random data.
line, = ax1.plot(x, np.random.rand(CHUNK)/2, '-', lw=1)
line_fft, = ax2.semilogx(x_fft, np.random.rand(CHUNK)/2, '-', lw=1)

# Formatting the waveform plot.
ax1.set_title('AUDIO WAVEFORM')
ax1.set_xlabel('samples')
ax1.set_ylabel('volume')
ax1.set_ylim(0, 255)
ax1.set_xlim(0, 2 * CHUNK)
plt.setp(ax1, xticks=[0, CHUNK, 2 * CHUNK], yticks=[0, 128, 255])

ax2.set_xlim(20, RATE / 2)  # Setting the x-axis limits for the spectrum plot.

plt.show(block=False)  # Displaying the plot in a non-blocking manner.

print('stream started')  # Indicating that the stream has started.

frame_count = 0  # Initializing the frame counter.
start_time = time.time()  # Recording the start time for frame rate calculation.

while True:
    data = stream.read(CHUNK)  # Reading a chunk of binary data from the stream.
    data_int = struct.unpack(str(2 * CHUNK) + 'B', data)  # Converting the binary data to integers.

    data_np = np.array(data_int, dtype='b')[::2] + 128  # Creating a numpy array for the waveform data.
    line.set_ydata(data_np)  # Updating the waveform data.

    y_fft = fft(data_int)  # Performing FFT on the data.
    line_fft.set_ydata(np.abs(y_fft[0:CHUNK])/(128 * CHUNK))  # Updating the spectrum data.

    try:
        fig.canvas.draw()  # Redrawing the canvas for the updated data.
        fig.canvas.flush_events()  # Processing GUI events.
        frame_count += 1  # Incrementing the frame count.
    except TclError:
        frame_rate = frame_count / (time.time() - start_time)  # Calculating the average frame rate.
        print('stream stopped')  # Indicating that the stream has stopped.
        print('average frame rate = {:.0f} FPS'.format(frame_rate))  # Displaying the average frame rate.
        break  # Exiting the loop and ending the program.
