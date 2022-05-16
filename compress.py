#!/usr/bin/env python3

import io
import librosa

from google.cloud import speech
from google.oauth2 import service_account


def get_clip(wav_path):
  
  audio_ex, sr = librosa.load(wav_path)
  
  # Naive clipping method: Take first 10 seconds
  clip_duration_seconds = min(10, sr * len(audio_ex))
  n_frames = clip_duration_seconds * sr
  audio_clip = audio_ex[:n_frames]
  return audio_clip

def get_transcript(wav_path, gcp_creds_path):
  """
  Use GCP Speech-to-Text API to transcribe audio
  Following example here: https://cloud.google.com/speech-to-text/docs/samples/
    speech-transcribe-sync#speech_transcribe_sync-python
  """

  # Set up credentials (from https://stackoverflow.com/a/65453693)
  credentials = service_account.Credentials.from_service_account_file(gcp_creds_path)
  scoped_credentials = credentials.with_scopes(["https://www.googleapis.com/auth/cloud-platform"])
  client = speech.SpeechClient(credentials=credentials)

  # Prepare audio data
  with io.open(wav_path, "rb") as audio_f:
    content = audio_f.read()

  # Prepare request
  audio = speech.RecognitionAudio(content=content)
  config = speech.RecognitionConfig(language_code="en-US")

  # Await response
  operation = client.long_running_recognize(config=config, audio=audio)
  response = operation.result(timeout=90)

  # Parse response
  transcript = " ".join(result.alternatives[0].transcript for result in response.results)

  return transcript

def compress(wav_path, gcp_creds_path):
  """
  Compress a single audio file:

  Input:
  - audio, preprocessed by `preprocess`
  Output: 
  - A clip of the original audio
  - A transcript
  """

  clip = get_clip(wav_path)
  transcript = get_transcript(wav_path, gcp_creds_path)

  return clip, transcript
