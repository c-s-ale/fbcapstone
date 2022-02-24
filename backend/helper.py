import pickle
import Levenshtein as lvdist
from typing import Tuple

#TODO: Add more descriptive function comments

def get_common_words_list() -> list:
    with open('common_words.pickle', 'rb') as f:
            common_words = pickle.load(f)
    return common_words

def get_wakeword(trasncript: str) -> str:
    wakeword = trasncript.split('|')[0]
    print('Wakeword:', wakeword)
    return wakeword

def parse_command(transcript: str, wakeword: str) -> Tuple[str, bool]:
    detected = False
    command = []

    for word in transcript.split('|'):
        if detected:
            command.append(word)
        if word == wakeword:
            detected = True
    return " ".join(command), detected

def score_word(wakeword: str, common_words: list) -> int:
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


if __name__ == '__main__':
    pass