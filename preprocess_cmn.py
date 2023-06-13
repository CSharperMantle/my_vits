import argparse
from os import path

import text
from utils import load_filepaths_and_text

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--text_index", default=1, type=int)
    parser.add_argument("-f", "--filelists", nargs="+", required=True)
    parser.add_argument(
        "-c", "--text_cleaners", nargs="+", default=["mandarin_cleaners"]
    )
    parser.add_argument("-p", "--postfix", default="cleaned")

    args = parser.parse_args()

    for filelist in args.filelists:
        print(f"START: {filelist}")
        filepaths_and_text = load_filepaths_and_text(filelist)
        for i in range(len(filepaths_and_text)):
            original_text = filepaths_and_text[i][args.text_index]
            cleaned_text = text._clean_text(original_text, args.text_cleaners)
            filepaths_and_text[i][args.text_index] = cleaned_text

        filelist_base, filelist_ext = path.splitext(filelist)

        new_filelist = filelist_base + f".{args.postfix}." + filelist_ext
        with open(new_filelist, "w", encoding="utf-8") as f:
            f.writelines(["|".join(x) + "\n" for x in filepaths_and_text])
