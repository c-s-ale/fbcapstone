import torch
import torchaudio

class Wav2Vec2:
    def __init__(self):
        self.device = "cpu"
        print(f"Using device: {self.device}")
        self.bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
        self.model = self.bundle.get_model().to(self.device)
        self.wakeword = None

    def encode(self, file):
        sig, sr = torchaudio.load(file)
        input = torch.tensor(sig[0])[None,:]

        if sr != self.bundle.sample_rate: 
            input = torchaudio.functional.resample(input, sr, self.bundle.sample_rate)                    
        input.to(self.device)
        encoding, _ = self.model(input)        
        return encoding[0]

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

if __name__ == '__main__':
    pass

