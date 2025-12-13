import speech_recognition as sr
import os
import warnings
import shutil
import subprocess

# Suppress SyntaxWarning raised by pydub's regex literals at import-time
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pydub.utils")

# Try to locate ffmpeg/avconv
ffmpeg_path = os.getenv("FFMPEG_BINARY") or shutil.which("ffmpeg") or shutil.which("ffmpeg.exe") or shutil.which("avconv")
if ffmpeg_path:
    try:
        from pydub import AudioSegment
        AudioSegment.converter = ffmpeg_path
    except Exception:
        from pydub import AudioSegment
else:
    warnings.filterwarnings("ignore", category=RuntimeWarning, module="pydub.utils")
    from pydub import AudioSegment

def transcribe_audio(file_path: str) -> str:
    """
    Transcribe an audio file (MP3, WAV, OPUS, etc.) into text.

    Args:
        file_path (str): Path to the input audio file.

    Returns:
        str: The transcribed text from the audio.
    """
    try:
        # Handle path - check both LLMFiles and current directory
        if not os.path.isabs(file_path):
            if os.path.exists(os.path.join("LLMFiles", file_path)):
                file_path = os.path.join("LLMFiles", file_path)
            elif not os.path.exists(file_path):
                file_path = os.path.join("LLMFiles", file_path)
        
        final_path = file_path
        
        # Convert non-WAV formats to WAV using ffmpeg
        if not file_path.lower().endswith(".wav"):
            final_path = file_path.rsplit(".", 1)[0] + ".wav"
            # Use ffmpeg for any format (MP3, OPUS, OGG, etc.)
            cmd = ["ffmpeg", "-y", "-i", file_path, "-ar", "16000", "-ac", "1", final_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                return f"FFmpeg conversion failed: {result.stderr}"

        # Speech recognition using Google's free API
        recognizer = sr.Recognizer()
        with sr.AudioFile(final_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)

        # Clean up temp wav if we created it
        if final_path != file_path and os.path.exists(final_path):
            os.remove(final_path)

        return text
    except sr.UnknownValueError:
        return "Error: Could not understand audio"
    except sr.RequestError as e:
        return f"Error: Speech recognition service error - {e}"
    except Exception as e:
        return f"Error occurred: {e}"