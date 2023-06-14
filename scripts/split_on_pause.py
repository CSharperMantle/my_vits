# Copyright (c) 2023 Rong Bao <baorong2005@126.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import librosa as r
import soundfile as sf
import os

INPUT_WAV_FILE_PATH: str = R"[YOUR_FILE_PATH]"
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
