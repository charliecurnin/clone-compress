#!/usr/bin/env python3

import librosa

def get_clip(wav_path):
  
  audio_ex, sr = librosa.load(wav_path)
  
  # Naive clipping method: Take first 10 seconds
  clip_duration_seconds = min(10, sr * len(audio_ex))
  n_frames = clip_duration_seconds * sr
  audio_clip = audio_ex[:n_frames]
  return audio_clip

def get_transcript(wav_path):
  return ""

def compress(wav_path):
  """
  Compress a single audio file:

  Input:
  - audio, preprocessed by `preprocess`
  Output: 
  - A clip of the original audio
  - A transcript
  """

  clip = get_clip(wav_path)
  transcript = get_transcript(wav_path)

  return clip, transcript
