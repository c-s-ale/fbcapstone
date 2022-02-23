import json
from flask import Flask, request
from flask_cors import CORS
import torch
import torchaudio
import pickle
import Levenshtein as lvdist


app = Flask(__name__)
CORS(app)

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
    """
    Load the model and the wakeword, initialize the bundle,
    and load the corpus
    """
    global device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Using device: {device}')
    global bundle
    bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
    print(f'Using bundle: {bundle}')
    global model
    model = bundle.get_model().to(device)
    global common_words
    with open('common_words.pickle', 'rb') as f:
        common_words = pickle.load(f)

def get_new_tensor(filename, skip_model = False):
    """
    Args:
        filename (str): The filename of the audio file
        skip_model (bool): Whether to skip the model
    Returns:
        tensor (Tensor): The tensor of the processed audio file
    """
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
    """
    Args:
        transcript (str): The transcript to check
        wakeword (str): The wakeword to check for
    Returns:
        command (str): The command to execute"""
    command_set = False
    command = []
    new_wake = ""
    for word in transcript:
        if command_set:
            command.append(word)
        if word.lower() == wakeword.lower():
            command_set = True
            new_wake = word
    return " ".join(command), new_wake

def score_wake_word(wakeword, corpus):
    '''
    Strength: 
    <2: Very Strong
    3-5: Strong
    6-10: Medium
    11-20: Weak
    21+: Awful
    '''
    ww = wakeword.lower()
    dists = [lvdist.distance(ww, x) for x in common_words]
    strength = sum([1 if d < 3 else 0 for d in dists])
    return strength

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
    wakeword = transcript_split[0]
    print('Wakeword:', wakeword)
    if wakeword != "":
        strength = score_wake_word(wakeword, common_words)
        return {'wakeword' : wakeword,
                'wakewordStrength': strength,
                'success' : True}
    else:
        return {'transcript' : "No wakeword detected",
                'wakewordStrength': 100,
                'success' : False}

@app.route('/api/command', methods=['POST'])
def command():

    if 'file' in request.files:
        audio_file = request.files['file']
        audio_file.save(f'./wav/command.wav')
        wakeword = request.form['wakeword']
        wakeword = wakeword.lower()
    else:
        return {'transcript' : 'No audio file found',
                'success' : False}
    
    command_tensor = get_new_tensor(f'./wav/command.wav')
    decoder = GreedyCTCDecoder(labels=bundle.get_labels())
    transcript = decoder(command_tensor)
    transcript_list = transcript.split('|')
    print('Transcript:', transcript)
    if wakeword != "":
        new_command, found_wake = check_transcript_for_wakeword(transcript_list, wakeword)
    else:
        return {'transcript' : "Please set a wake word first!",
                'success' : False}

    if found_wake != "":
        return {'transcript': new_command,
                'detect_wakeword': True,
                'success' : True,
                'wakeword': found_wake}
    else:
        return {'transcript' : "No command detected",
                'success' : False,
                'detect_wakeword': False,}

if __name__ == '__main__':
    app.run(port=5000, debug=True)

