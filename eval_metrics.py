#!/usr/bin/env python3

def audio_qual(decompressed_audio):
  pass

def compression_ratio(input_wav, compress_wav, transcript, audio_sr):
  pass

def _compression_ratio(original_duration, compressed_duration, audio_sr):
  
  bit_depth = 16 
  channels = 2 # stereo
  return (audio_sr * (bit_depth/8) * channels * (compressed_duration/original_duration))
