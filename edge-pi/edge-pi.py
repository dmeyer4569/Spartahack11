#!/usr/bin/env python3

# Generic Python Imports
import time
import os
import shutil
import sys
from datetime import datetime
import threading
import numpy as np

# Accessing the GPIO
import RPi.GPIO as GPIO

# Accessing the Webcam
import cv2

# Accessing the Microphone
import sounddevice as sd
import queue
import wave

# Submit a POST request
import requests
from contextlib import ExitStack

# GPIO Constants
GPIO_PIR = 5
WHITE_LED = 12
TRIG_PIN = 6
ECHO_PIN = 16
GREEN_LED = 24
RED_LED = 23

IMAGE_FOLDER = "images"
AUDIO_FOLDER = "audio"

audio_queue = queue.Queue()

OBJECT_PRESENT_DISTANCE = 30
OBJECT_GONE_DISTANCE = 35
PICTURE_COOLDOWN = 1.0
MIN_RECORD_SEC = 10  # used as the post-buffer for audio

def audio_callback(indata, frames, t, status):
    if status:
        print("Sounddevice status:", status)
    audio_queue.put(indata.copy())

def record_audio(filename, samplerate=44100, channels=1, sampwidth=2, stop_event=None):
    wf = wave.open(filename, 'wb') #https://docs.python.org/3/library/wave.html
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(samplerate)

    with sd.InputStream(samplerate=samplerate, channels=channels, dtype='int16', callback=audio_callback):
        print(f"Recording audio to {filename}")
        while not (stop_event and stop_event.is_set()):
            try:
                data = audio_queue.get(timeout=0.1)
                if data.dtype != np.int16 and sampwidth == 2:
                    data = (data * 32767).astype(np.int16)
                wf.writeframes(data.tobytes())
            except queue.Empty:
                continue

    wf.close()
    print(f"Stopped the audio recording : {filename}")

def distance_sensor(timeout=0.02):
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.02)

    # trigger
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    pulse_start = None
    pulse_end = None

    start_time = time.time()
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()
        if (pulse_start - start_time) > timeout:
            return None

    start_time = time.time()
    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()
        if (pulse_end - start_time) > timeout:
            return None

    if pulse_start is None or pulse_end is None:
        return None

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance

# camera capture
def take_picture(cap):
    GPIO.output(WHITE_LED, True)
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = os.path.join(IMAGE_FOLDER, f"{timestamp}.jpg")
    cv2.imwrite(path, frame)
    print(f"Image saved: {path}")
    GPIO.output(WHITE_LED, False)
    return path

def motion_status():
    current_state = GPIO.input(GPIO_PIR)
    return current_state == 1

def sync_with_backend(ip: str, images_written: list[str], audio_path: str) -> None:
    url = f"http://{ip}:8000/rpi_upload"

    with ExitStack() as stack:
        files = [
            ("images", (path, stack.enter_context(open(path, "rb")), "image/jpeg"))
            for path in images_written
        ]

        audio_f = stack.enter_context(open(audio_path, "rb"))
        files.append(("audio_file", (audio_path, audio_f, "audio/wav")))

        response = requests.post(url, files=files)

def clear_folder(folder: str) -> None:
    if os.path.exists(folder):
        shutil.rmtree(folder)

    os.makedirs(folder)


def start_logging(ip: str) -> None:
    cap = cv2.VideoCapture("/dev/video0", cv2.CAP_V4L2)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    if not cap.isOpened():
        print("Camera not found")
        return

    stop_audio_event = threading.Event()
    audio_thread = None
    motion_active = False
    last_motion_time = None
    last_picture_time = None

    object_present = False
    picture_taken = False

    images_written = []
    audio_file = ""

    try:
        while True:
            now = datetime.now()
            pir = motion_status()

            dist = distance_sensor()
            if dist is None:
                dist = 500.0
            else:
                print(f"Distance: {dist} cm")

            if dist is not None:
                if not object_present and dist <= OBJECT_PRESENT_DISTANCE:
                    object_present = True
                    picture_taken = False  # reset for new object
                elif object_present and dist >= OBJECT_GONE_DISTANCE:
                    object_present = False
                    picture_taken = False  # ready for next object

            if object_present and not picture_taken:
                now_ts = time.time()
                if (last_picture_time is None) or ((now_ts - last_picture_time) >= PICTURE_COOLDOWN):
                    print("Object entered range -> taking picture")
                    path = take_picture(cap)
                    if path:
                        last_picture_time = now_ts
                        picture_taken = True
                        images_written.append(path)

            if pir:
                print("PIR DETECTED")
                last_motion_time = now
                if not motion_active:
                    # start audio
                    timestamp = now.strftime("%Y%m%d_%H%M%S")
                    audio_file = os.path.join(AUDIO_FOLDER, f"{timestamp}.wav")

                    stop_audio_event.clear()
                    try:
                        while True:
                            audio_queue.get_nowait()
                    except queue.Empty:
                        pass

                    audio_thread = threading.Thread(
                        target=record_audio,
                        args=(audio_file,),
                        kwargs={
                            'samplerate': 44100,
                            'channels': 1,
                            'sampwidth': 2,
                            'stop_event': stop_audio_event
                        },
                        daemon=True
                    )
                    audio_thread.start()
                    motion_active = True
                    GPIO.output(GREEN_LED, True)
                    GPIO.output(RED_LED, False)
                    print("Recording started (PIR)")


            if motion_active and last_motion_time is not None:
                elapsed = (now - last_motion_time).total_seconds()
                if elapsed >= MIN_RECORD_SEC:
                    stop_audio_event.set()
                    if audio_thread:
                        audio_thread.join(timeout=5)
                    audio_thread = None
                    motion_active = False
                    GPIO.output(GREEN_LED, False)
                    GPIO.output(RED_LED, True)
                    print(f"No motion for {MIN_RECORD_SEC}s -> stopped recording")
                    
                    sync_with_backend(ip, images_written, audio_file)
                    clear_folder(IMAGE_FOLDER)
                    clear_folder(AUDIO_FOLDER)

            time.sleep(0.15)

    except KeyboardInterrupt:
        print("Exiting (KeyboardInterrupt)")
    finally:
        if motion_active:
            stop_audio_event.set()
            if audio_thread:
                audio_thread.join(timeout=5)
        cap.release()
        GPIO.cleanup()
        print("Clean up")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python3 {sys.argv[0]} <BACKEND LAPTOP IP>")
        exit()
   
    ip = sys.argv[1]

    # Setup GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
   
    # Establish pin mode for pins
    GPIO.setup(WHITE_LED, GPIO.OUT)
    GPIO.setup(GPIO_PIR, GPIO.IN)
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)
    GPIO.setup(GREEN_LED, GPIO.OUT)
    GPIO.setup(RED_LED, GPIO.OUT)

    # Create image and audio directories
    os.makedirs(IMAGE_FOLDER, exist_ok=True)
    os.makedirs(AUDIO_FOLDER, exist_ok=True)
    print("Starting motion detection...")
    
    start_logging(ip)
