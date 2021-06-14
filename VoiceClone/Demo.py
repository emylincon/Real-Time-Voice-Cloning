from VoiceClone.encoder.params_model import model_embedding_size as speaker_embedding_size
from VoiceClone.utils.argutils import print_args
from VoiceClone.utils.modelutils import check_model_paths
from VoiceClone.synthesizer.inference import Synthesizer
from VoiceClone.encoder import inference as encoder
from VoiceClone.vocoder import inference as vocoder
from pathlib import Path
import numpy as np
import soundfile as sf
import librosa
import torch
import sys
import os
from audioread.exceptions import NoBackendError


os.environ["CUDA_VISIBLE_DEVICES"] = ""


class Clone:
    def __init__(self, location=""):
        if location != "":
            location = 'VoiceClone/'
            self.output_folder = f'static/temp'
        else:
            self.output_folder = f"{location}output"
        self.encoder_path = Path(f"{location}pretrained/encoder/saved_models/pretrained.pt")
        self.vocoder_path = Path(f"{location}pretrained/vocoder/saved_models/pretrained/pretrained.pt")
        self.synthesizer_path = Path(f"{location}pretrained/synthesizer/saved_models/pretrained/pretrained.pt")
        encoder.load_model(self.encoder_path)
        self.synthesizer = Synthesizer(self.synthesizer_path)
        vocoder.load_model(self.vocoder_path)
        self.num_generated = 0

    def clone_voice(self, embed, message):
        try:
            # The synthesizer works in batch, so you need to put your data in a list or numpy array
            texts = [message]
            embeds = [embed]
            # If you know what the attention layer alignments are, you can retrieve them here by
            # passing return_alignments=True
            specs = self.synthesizer.synthesize_spectrograms(texts, embeds)
            spec = specs[0]
            print("Created the mel spectrogram")

            ## Generating the waveform
            print("Synthesizing the waveform:")

            # If seed is specified, reset torch seed and reload vocoder

            # Synthesizing the waveform is fairly straightforward. Remember that the longer the
            # spectrogram, the more time-efficient the vocoder.
            generated_wav = vocoder.infer_waveform(spec)

            ## Post-generation
            # There's a bug with sounddevice that makes the audio cut one second earlier, so we
            # pad it.
            generated_wav = np.pad(generated_wav, (0, self.synthesizer.sample_rate), mode="constant")

            # Trim excess silences to compensate for gaps in spectrograms (issue #53)
            generated_wav = encoder.preprocess_wav(generated_wav)

            # Save it on the disk
            filename = f"{self.output_folder}/demo_output_{self.num_generated:03}.wav"
            print(generated_wav.dtype)
            sf.write(filename, generated_wav.astype(np.float32), self.synthesizer.sample_rate)
            self.num_generated += 1
            print("\nSaved output as %s\n\n" % filename)
            return filename

        except Exception as e:
            print("Caught exception: %s" % repr(e))

    @staticmethod
    def process_voice(voice):
        voice = Path(voice)
        ## Computing the embedding
        # First, we load the wav using the function that the speaker encoder provides. This is
        # important: there is preprocessing that must be applied.
        # The following two methods are equivalent:
        # - Directly load from the filepath:
        preprocessed_wav = encoder.preprocess_wav(voice)
        # - If the wav is already loaded:
        original_wav, sampling_rate = librosa.load(str(voice))
        preprocessed_wav = encoder.preprocess_wav(original_wav, sampling_rate)
        print("Loaded file succesfully")
        # Then we derive the embedding. There are many functions and parameters that the
        # speaker encoder interfaces. These are mostly for in-depth research. You will typically
        # only use this function (with its default parameters):
        embed = encoder.embed_utterance(preprocessed_wav)
        print("Created the embedding")
        return embed

    def voice_clone_audio(self, audio, message):
        embed = self.process_voice(audio)
        self.clone_voice(embed, message)


if __name__ == "__main__":
    Clone().voice_clone_audio('nano.weba', "Hello world")
    # Clone().voice_clone_audio('voice.mp3',"Hello world")