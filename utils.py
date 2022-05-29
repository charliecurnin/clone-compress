#!/usr/bin/env python3

from google.cloud import storage

DATA_BUCKET_NAME = "cs224s-audio-input"

def upload_to_gcp(wav_path, credentials):
  """
  Upload to GCP (since must upload files >60s anyway)
  """

  path_segments = wav_path.split(os.path.sep)
  speaker_role = path_segments[-2]
  wav_name = path_segments[-1]

  assert speaker_role in ["agent", "caller"]
  destination_name = f"{speaker_role}-{wav_name}"
  destination_uri = f"gs://{DATA_BUCKET_NAME}/{destination_name}"

  bucket = storage.Client(credentials=credentials).bucket(DATA_BUCKET_NAME)
  blob = bucket.blob(destination_name)
  blob.upload_from_filename(wav_path)
  
  return destination_uri 

