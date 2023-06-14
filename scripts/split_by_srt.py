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
import math
import os

import librosa as r
import soundfile as sf
import srt

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--path", required=True)
parser.add_argument("-s", "--srt", required=True)
args = parser.parse_args()

in_wav_path = args.path
in_srt_path = args.srt

if not os.path.isfile(in_wav_path):
    raise ValueError(f"{in_wav_path}: not a file")
if not os.path.isfile(in_srt_path):
    raise ValueError(f"{in_srt_path}: not a file")

with open(in_srt_path, "r", encoding="utf-8") as srt_file:
    srt_obj = srt.parse(srt_file.read())

audio_file_folder = os.path.split(in_wav_path)[0]
audio_file_base = os.path.splitext(os.path.basename(in_wav_path))[0]

audio_buffer, sample_rate = r.core.load(in_wav_path, sr=None)
print(f"File length: {audio_buffer.shape[0] / sample_rate}s, SR {sample_rate}")

os.mkdir(os.path.join(audio_file_folder, audio_file_base))

for i, subtitle in enumerate(srt_obj):
    out_path_noext = os.path.join(
        audio_file_folder, audio_file_base, f"{audio_file_base}-{i}#"
    )

    start_sample = math.floor(subtitle.start.total_seconds() * sample_rate)
    end_sample = math.ceil(subtitle.end.total_seconds() * sample_rate)

    print(f"Chunk # {i}: {start_sample} to {end_sample}")

    audio_slice = audio_buffer[start_sample : end_sample + 1]
    sf.write(out_path_noext + ".wav", audio_slice, int(sample_rate))
    with open(out_path_noext + ".txt", "w", encoding="utf-8") as f:
        f.write(subtitle.content)

    print(f"Chunk # {i}: exported")
