#!/usr/bin/env python3

import librosa
import numpy as np

def preprocess(wav):
  """
  Preprocess a single audio file:
  - Remove pauses
  """

  # Remove pauses
  """
  Borrowed from code I wrote for CS 224S HW1
  """

  print("wav len: ", len(wav))
  speech_intervals = librosa.effects.split(wav)
  wav = np.concatenate([
    wav[start_i:end_i] for (start_i, end_i) in speech_intervals
  ])
  print("pp wav len: ", len(wav))

  return wav #, len(speech_intervals)
