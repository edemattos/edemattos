#!/usr/bin/env python

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
from scipy.io import wavfile


def parse_args(args: list | None = None) -> argparse.Namespace:

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", type=Path)
    parser.add_argument("--start", type=float, default=0.0, help="start time (seconds)")
    parser.add_argument("--end", type=float, default=-1.0, help="end time (seconds)")
    parser.add_argument("--outfile", type=Path, default="waveform.svg")
    parser.add_argument("--aspect_ratio", type=int, nargs=2, help="width height")
    return parser.parse_args(args)


def trim_audio(audio: array, sample_rate: int, start: float, end: float) -> array:

    # convert seconds to samples
    start = int(start * sample_rate)
    end = int(end * sample_rate)
    return audio[start:end]


def normalize_samples(audio: array) -> array:

    norm = max(abs(max(audio)), abs(min(audio)))
    return audio / norm


def plot_waveform(audio: array, filename: Path, aspect_ratio: Tuple[int, int] | None = None) -> None:

    plt.figure(figsize=aspect_ratio)
    plt.plot(audio, linewidth=0.33, color="grey")
    plt.axis("off")
    plt.ylim((-0.33, 0.33))
    plt.margins(x=0, y=0)
    plt.tight_layout()
    plt.savefig(filename, bbox_inches="tight", transparent=True)


def main():

    args = parse_args()

    # load audio as a numpy array
    sample_rate, audio = wavfile.read(args.filename)

    # pre-process
    audio = normalize_samples(audio)
    audio = trim_audio(audio, sample_rate, args.start, args.end)

    plot_waveform(audio, args.outfile, args.aspect_ratio)


if __name__ == "__main__":
    main()
