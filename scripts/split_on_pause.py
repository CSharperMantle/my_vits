import librosa as r
import soundfile as sf
import os

INPUT_WAV_FILE_PATH: str = R"local\dataset\12月20日化学课录屏.wav"
WINDOW_LENGTH_SECONDS: float = 1
SILENCE_THRESHOLD: int = 50

if not os.path.isfile(INPUT_WAV_FILE_PATH):
    raise ValueError(f"{INPUT_WAV_FILE_PATH}: not a file")

audio_file_folder = os.path.split(INPUT_WAV_FILE_PATH)[0]
audio_file_base = os.path.splitext(os.path.basename(INPUT_WAV_FILE_PATH))[0]

audio_buffer, sample_rate = r.core.load(INPUT_WAV_FILE_PATH, sr=None)
print(f"File length: {audio_buffer.shape[0] / sample_rate * 1000.0}ms, SR {sample_rate}")

os.mkdir(os.path.join(audio_file_folder, audio_file_base))

for i, clip_range in enumerate(
        r.effects.split(
            y=audio_buffer,
            top_db=SILENCE_THRESHOLD,
            frame_length=int(sample_rate * WINDOW_LENGTH_SECONDS),
        )
):
    print(f"Chunk # {i}: {clip_range[0]} to {clip_range[1]}")
    chunk = audio_buffer[clip_range[0]: clip_range[1]]
    output_file_path = os.path.join(
        audio_file_folder, audio_file_base, f"{audio_file_base}-{i}#.wav"
    )
    sf.write(output_file_path, chunk, int(sample_rate))
    print(f"Chunk # {i}: exported")
