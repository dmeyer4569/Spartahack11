import wave
import json
import librosa
import soundfile as sf
from vosk import Model, KaldiRecognizer

MODEL_PATH = "vosk-model-small-en-us-0.15"

def convert_khz(wavFile):
    converted_file = "converted_16k.wav"
    audio , sr = librosa.load(wavFile, sr=16000, mono=True)
    sf.write(converted_file, audio, 16000, subtype='PCM_16')

    print("Converted File to 16kHz mono WAV")
    return converted_file

def stt(AudioFile):
    model = Model(MODEL_PATH)

    converted_file = convert_khz(AudioFile)

    wf = wave.open(converted_file, "rb")

    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 16000:
        raise ValueError("Audio must be wav format mono PCM 16-bit 16kHz")
    
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    full_text = []

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break

        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            full_text.append(result.get("text", ""))

    final_result = json.loads(rec.FinalResult())
    full_text.append(final_result.get("text", ""))

    transcript = " ".join(full_text)

    return(transcript)