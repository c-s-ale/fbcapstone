import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from model import Wav2Vec2, GreedyCTCDecoder
from helper import get_common_words_list, get_wakeword, parse_command, score_word
from glob import glob
import os


app = Flask(__name__)
CORS(app)

# Load model before first request:
#   Because our model is served through gunicorn, main is not called
#   this means we need to load the model here.
@app.before_first_request
def before_first_request():
    """
    Load the model and the wakeword, initialize the bundle,
    and load the corpus
    """
    # Set global variables for use in endpoints
    global model
    global decoder
    global common_words

    # Load the model
    model = Wav2Vec2()

    # Load the decoder
    decoder = GreedyCTCDecoder(labels=model.bundle.get_labels())

    # Load common words for calculating Levenshtein distance
    common_words = get_common_words_list()

# Health Check - Required for Deployment
@app.route('/')
def home():
    return "OK"

# Endpoint to get the wakeword
# TODO: Add proper reponse codes
@app.route('/api/wakeword', methods=['POST'])
def wakeword():
    """
        Endpoint to get the wakeword

        Parameters:
            file: The audio file to be analyzed
        Returns:
            wakeword: The wakeword
            success: True if the wakeword was detected, False otherwise
            strength: The Levenshtein Score of the detected wakeword
    """
    if 'file' in request.files:
        audio_file = request.files['file']
        wakeword_key = len(glob('/wav/wakeword/*.wav'))
        wav_file = f'./wav/wakeword/wakeword_{str(wakeword_key)}.wav'
        audio_file.save(wav_file)
        encoding = model.encode(wav_file)
        wakeword = get_wakeword(decoder(encoding))

        # Delete the file
        os.remove(wav_file)

        if wakeword != "":
            return jsonify({'wakeword': wakeword,
                            'success' : True,
                            'strength': score_word(wakeword, common_words)})
        else:
            return jsonify({'wakeword': 'ERROR: Wakeword not detected',
                            'success' : False,
                            'strength': None})
    else:
        return jsonify({'transcript' : 'ERROR: No file uploaded',
                        'success'    : False,
                        'strength'   : None})

# Endpoint to get the command
@app.route('/api/command', methods=['POST'])
def command():
    """
        Endpoint to detect the wakeword in a command

        Parameters:
            file: The audio file to be analyzed
        Returns:
            wakeword: The wakeword
            success: True if the wakeword was detected, False otherwise
            strength: The Levenshtein Score of the detected wakeword
    """
    if 'file' in request.files:
        audio_file = request.files['file']
        command_key = len(glob('/wav/command/*.wav'))
        command_file = f'./wav/command/command_{str(command_key)}.wav'
        audio_file.save(command_file)
        wakeword = request.form['wakeword']
        command, detected = parse_command(decoder(model.encode(command_file)), 
                                          wakeword)
    
        if detected:
            return jsonify({'command': command,
                            'success' : True,})
        else:
            return jsonify({'command': 'ERROR: Wakeword not detected',
                            'success' : False,})
    else:
        return jsonify({'command' : 'ERROR: No file uploaded',
                        'success'    : False,})
    

if __name__ == '__main__':
    app.run(port=5000, debug=True)

