from IPython.display import Audio
from IPython.utils import io
from synthesizer.inference import Synthesizer
from encoder import inference as encoder
from vocoder import inference as vocoder
from pathlib import Path
import numpy as np
import librosa

"""
Adapted from https://colab.research.google.com/drive/1SWvpwlJH95_i-zjsro0m_Zw9I8sSqbLE?authuser=1#scrollTo=6NpQBkN_22Gi
"""

def decompress(original_wav, sampling_rate, text):
    encoder_weights = Path("encoder/saved_models/pretrained.pt")
    vocoder_weights = Path("vocoder/saved_models/pretrained/pretrained.pt")
    syn_dir = Path("synthesizer/saved_models/logs-pretrained/taco_pretrained")
    encoder.load_model(encoder_weights)
    synthesizer = Synthesizer(syn_dir)
    vocoder.load_model(vocoder_weights)
    
    preprocessed_wav = encoder.preprocess_wav(original_wav, sampling_rate)
    embed = encoder.embed_utterance(preprocessed_wav)
    with io.capture_output() as captured:
        specs = synthesizer.synthesize_spectrograms([text], [embed])
    generated_wav = vocoder.infer_waveform(specs[0])
    generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")
    return (generated_wav, synthesizer.sample_rate)

    
def _decompress(agent_audio_file, text):
    encoder_weights = Path("encoder/saved_models/pretrained.pt")
    vocoder_weights = Path("vocoder/saved_models/pretrained/pretrained.pt")
    syn_dir = Path("synthesizer/saved_models/logs-pretrained/taco_pretrained")
    encoder.load_model(encoder_weights)
    synthesizer = Synthesizer(syn_dir)
    vocoder.load_model(vocoder_weights)
    
    original_wav, sampling_rate = librosa.load(agent_audio_file)
    preprocessed_wav = encoder.preprocess_wav(original_wav, sampling_rate)
    embed = encoder.embed_utterance(preprocessed_wav)
    with io.capture_output() as captured:
        specs = synthesizer.synthesize_spectrograms([text], [embed])
    generated_wav = vocoder.infer_waveform(specs[0])
    generated_wav = np.pad(generated_wav, (0, synthesizer.sample_rate), mode="constant")
    return (generated_wav, synthesizer.sample_rate)   
