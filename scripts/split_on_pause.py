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


import argparse
import os

import librosa as r
import soundfile as sf

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", required=True)
parser.add_argument("-w", "--win-len-sec", default=1.0, type=float)
parser.add_argument("-t", "--threshold", default=50, type=int)
args = parser.parse_args()

in_wav_path = args.path
in_threshold = args.threshold
in_win_len = args.win_len_sec

if not os.path.isfile(in_wav_path):
    raise ValueError(f"{in_wav_path}: not a file")

audio_file_folder = os.path.split(in_wav_path)[0]
audio_file_base = os.path.splitext(os.path.basename(in_wav_path))[0]

audio_buffer, sample_rate = r.core.load(in_wav_path, sr=None)
print(f"File length: {audio_buffer.shape[0] / sample_rate}s, SR {sample_rate}")
win_len = round(sample_rate * in_win_len)

os.mkdir(os.path.join(audio_file_folder, audio_file_base))


for i, clip_range in enumerate(
    r.effects.split(
        audio_buffer,
        top_db=in_threshold,
        frame_length=win_len,
    )
):
    print(f"Chunk # {i}: {clip_range[0]} to {clip_range[1]}")
    chunk = audio_buffer[clip_range[0] : clip_range[1]]
    chunk, _ = r.effects.trim(chunk, top_db=in_threshold, frame_length=win_len)
    output_file_path = os.path.join(
        audio_file_folder, audio_file_base, f"{audio_file_base}-{i}#.wav"
    )
    sf.write(output_file_path, chunk, int(sample_rate))
    print(f"Chunk # {i}: exported")
