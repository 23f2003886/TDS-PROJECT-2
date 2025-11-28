from langchain.tools import tool
import speech_recognition as sr
import os
import warnings
import shutil

# Suppress SyntaxWarning raised by pydub's regex literals at import-time
# by filtering SyntaxWarning coming from the pydub.utils module.
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pydub.utils")

# Try to locate ffmpeg/avconv. If found, set pydub's AudioSegment.converter
# before importing AudioSegment to avoid RuntimeWarning and ensure conversions work.
ffmpeg_path = os.getenv("FFMPEG_BINARY") or shutil.which("ffmpeg") or shutil.which("ffmpeg.exe") or shutil.which("avconv")
if ffmpeg_path:
    try:
        from pydub import AudioSegment
        AudioSegment.converter = ffmpeg_path
    except Exception:
        # If pydub import still fails for some reason, fall back to importing normally
        from pydub import AudioSegment
else:
    # No ffmpeg found: suppress the specific pydub RuntimeWarning about missing ffmpeg
    warnings.filterwarnings("ignore", category=RuntimeWarning, module="pydub.utils")
    from pydub import AudioSegment

@tool
def transcribe_audio(file_path: str) -> str:
    """
    Transcribe an MP3 or WAV audio file into text using Google's Web Speech API.

    Args:
        file_path (str): Path to the input audio file (.mp3 or .wav).

    Returns:
        str: The transcribed text from the audio.

    Notes:
        - MP3 files are automatically converted to WAV.
        - Requires `pydub` and `speech_recognition` packages.
        - Uses Google's free recognize_google() API (requires internet).
    """
    try:
        # Convert MP3 → WAV if needed
        file_path = os.path.join("LLMFiles", file_path)
        final_path = file_path
        if file_path.lower().endswith(".mp3"):
            sound = AudioSegment.from_mp3(file_path)
            final_path = file_path.replace(".mp3", ".wav")
            sound.export(final_path, format="wav")

        # Speech recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(final_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)

        # If we converted the file, remove temp wav
        if final_path != file_path and os.path.exists(final_path):
            os.remove(final_path)

        return text
    except Exception as e:
        return f"Error occurred: {e}"