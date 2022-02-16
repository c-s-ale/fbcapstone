import json
from flask import Flask, request
from flask_cors import CORS
import torch
import torchaudio

app = Flask(__name__)
CORS(app)


class Wakeword:
    def __init__(self, wakeword):
        self.wakeword = wakeword
    
    def get_wakeword(self):
        return self.wakeword
    
    def set_wakeword(self, wakeword):
        self.wakeword = wakeword

class GreedyCTCDecoder(torch.nn.Module):
    def __init__(self, labels, blank=0):
        super().__init__()
        self.labels = labels
        self.blank = blank

    def forward(self, emission: torch.Tensor) -> str:
        """Given a sequence emission over labels, get the best path string
        Args:
          emission (Tensor): Logit tensors. Shape `[num_seq, num_label]`.

        Returns:
          str: The resulting transcript
        """
        indices = torch.argmax(emission, dim=-1)  # [num_seq,]
        indices = torch.unique_consecutive(indices, dim=-1)
        indices = [i for i in indices if i != self.blank]
        return "".join([self.labels[i] for i in indices])


@app.before_first_request
def before_first_request():
    global device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Using device: {device}')
    global bundle
    bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
    print(f'Using bundle: {bundle}')
    global model
    model = bundle.get_model().to(device)
    global wakeword_class
    wakeword_class = Wakeword('')

def get_new_tensor(filename, skip_model = False):
        wakeword_sig, wakeword_sf = torchaudio.load(filename)
        wakeword_wav = torch.tensor(wakeword_sig[0])[None,:]
        wakeword_wav = wakeword_wav.to(device)
        if wakeword_sf != bundle.sample_rate:
            wakeword_wav = torchaudio.functional.resample(wakeword_wav, wakeword_sf, bundle.sample_rate)
        if skip_model:
            return wakeword_wav

        with torch.inference_mode():
            wakeword_emission, _ = model(wakeword_wav)
        return wakeword_emission[0]

def check_transcript_for_wakeword(transcript, wakeword):
    command_set = False
    command = []
    for word in transcript:
        if command_set:
            command.append(word)
        if word.lower() == wakeword.lower():
            command_set = True
    return " ".join(command)

@app.route('/')
def home():
    return "ok"

@app.route('/api/wakeword', methods=['POST'])
def wakeword():
    print('here')
    if 'file' in request.files:
        audio_file = request.files['file']
        audio_file.save(f'./wav/wakeword.wav')
    else:
        return {'transcript' : 'No file uploaded',
                'success' : False}
    wakeword_tensor = get_new_tensor(f'./wav/wakeword.wav')
    decoder = GreedyCTCDecoder(labels=bundle.get_labels())
    transcript = decoder(wakeword_tensor)
    transcript_split = transcript.split('|')
    wakeword_class.set_wakeword(transcript_split[0])
    print('Wakeword:', wakeword_class.get_wakeword())
    if wakeword_class.get_wakeword() != "":
        return {'transcript' : wakeword_class.get_wakeword(),
                'success' : True}
    else:
        return {'transcript' : "No wakeword detected",
                'success' : False}

@app.route('/api/command', methods=['POST'])
def command():

    if 'file' in request.files:
        audio_file = request.files['file']
        audio_file.save(f'./wav/command.wav')
    else:
        return {'transcript' : 'No audio file found',
                'success' : False}
    
    command_tensor = get_new_tensor(f'./wav/command.wav')
    decoder = GreedyCTCDecoder(labels=bundle.get_labels())
    transcript = decoder(command_tensor)
    transcript_list = transcript.split('|')
    if wakeword_class.get_wakeword() != "":
        new_command = check_transcript_for_wakeword(transcript_list, wakeword_class.get_wakeword())
    else:
        return {'transcript' : "Please set a wake word first!",
                'success' : False}

    if new_command != "":
        return {'transcript': new_command,
                'success' : True}
    else:
        return {'transcript' : "No command detected",
                'success' : False}

if __name__ == '__main__':
    app.run(port=8080)

