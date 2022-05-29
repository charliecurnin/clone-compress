#!/usr/bin/env python3

import asyncio
import io
import librosa
import os

from google.oauth2 import service_account

"""
-------- CLIP OPTIONS --------
Which bit of audio to preserve to clone from?
"""

def get_clip_first10(wav_path):
  """
  Take first 10 seconds of audio
  """
  
  audio_ex, sr = librosa.load(wav_path)
  clip_duration_seconds = min(10, sr * len(audio_ex))
  n_frames = clip_duration_seconds * sr
  return audio_ex[:n_frames], sr

def get_clip_first30(wav_path):
  """
  Take first 30 seconds of audio
  """
  
  audio_ex, sr = librosa.load(wav_path)
  clip_duration_seconds = min(30, sr * len(audio_ex))
  n_frames = clip_duration_seconds * sr
  return audio_ex[:n_frames], sr

def get_clip_all(wav_path):
  return librosa.load(wav_path)

CLIP_OPTIONS = {
  "first10" : get_clip_first10,
  "first30" : get_clip_first30,
  "all" : get_clip_all
}

"""
-------- TRANSCRIPT OPTIONS --------
How to generate a transcript of the input audio? 
"""

def get_transcript_gcp(wav_path, credentials=None):
  """
  Use GCP Speech-to-Text API to transcribe audio
  Following example here: https://cloud.google.com/speech-to-text/docs/samples/
    speech-transcribe-sync#speech_transcribe_sync-python
  """

  if credentials is None:
    # Set up credentials (from https://stackoverflow.com/a/65453693)
    _credentials = service_account.Credentials.from_service_account_file(gcp_creds_path)
    credentials = _credentials.with_scopes(["https://www.googleapis.com/auth/cloud-platform"])

  from google.cloud import speech
  client = speech.SpeechClient(credentials=credentials)

  gcs_uri = upload_to_gcp(wav_path, credentials)

  # Prepare audio data
  with io.open(wav_path, "rb") as audio_f:
    content = audio_f.read()

  # Prepare request
  audio = speech.RecognitionAudio(uri=gcs_uri)
  config = speech.RecognitionConfig(language_code="en-US")

  # Await response
  operation = client.long_running_recognize(config=config, audio=audio)
  response = operation.result(timeout=90)

  # Parse response
  transcript = " ".join(result.alternatives[0].transcript for result in response.results)

  return transcript

def get_transcript_deepgram(wav_path, _):

  from deepgram import Deepgram
  DEEPGRAM_SECRET = "0b0bc22e55c888ff90a98aec70e8b41a5a7d2b09"

  async def transcribe():
    """
    Adapted from Deepgram instructional materials
    """
    client = Deepgram(DEEPGRAM_SECRET)
    with open(wav_path, 'rb') as audio:
      source = {'buffer': audio, 'mimetype': 'audio/wav'}
      options = {'punctuate': True, 'language': 'en', 'model': 'general-enhanced'}
      response = await client.transcription.prerecorded(source, options)
      transcript = response['results']['channels'][0]['alternatives'][0]['transcript']
      return transcript

  return asyncio.run(transcribe())

TRANSCRIPT_OPTIONS = {
  'gcp': get_transcript_gcp,
  'deepgram': get_transcript_deepgram,
}

def compress(wav_path, gcp_creds_path, clip_option, transcript_options):
  """
  Compress a single audio file:

  Input:
  - audio, preprocessed by `preprocess`
  Output: 
  - A clip of the original audio
  - A transcript
  """

  # Set up credentials (from https://stackoverflow.com/a/65453693)
  credentials = service_account.Credentials.from_service_account_file(gcp_creds_path)
  scoped_credentials = credentials.with_scopes(["https://www.googleapis.com/auth/cloud-platform"])

  # Generate clip
  assert clip_option in CLIP_OPTIONS, f"Unknown clip option: {clip_option}"
  clip = CLIP_OPTIONS[clip_option](wav_path)

  # Generate transcript
  assert transcript_option in TRANSCRIPT_OPTIONS, f"Unknown transcript_option: {transcript_option}"
  transcript = TRANSCRIPT_OPTIONS[transcript_option](wav_path, credentials)

  return clip, transcript
