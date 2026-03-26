from faster_whisper import WhisperModel

# Force CPU usage (fixes CUDA error)
model = WhisperModel("base", device="cpu", compute_type="int8")

def transcribe_audio(file_path):
    segments, _ = model.transcribe(file_path)

    text = ""
    for segment in segments:
        text += segment.text + " "

    return text.strip()