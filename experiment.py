#!/usr/bin/env python3

import preprocess from preprocess
import compress from compress
import decompress from decompress
import compression_ratio, audio_qual from eval_metrics

GCP_CREDS_PATH = None

def experiment(input_wav):

  # Preprocess
  pp_wav = preprocess(input_wav)

  # Compress
  clip, transcript = compress(wav_path, GCP_CREDS_PATH)

  # Decompress
  decompress_wav = decompress(clip, transcript)

  # Calc metrics
  audio_sr = None # TODO
  cr = compression_ratio(input_wav, clip, transcript, audio_sr)
  qual = None # TODO

  return {
    "cr": cr,
    "qual": qual,
  }
