import torch
import torch.nn as nn
import torch.nn.functional as F
import string

class AttentionHead(nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super(AttentionHead, self).__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        
        self.query = nn.Linear(input_dim, hidden_dim)
        self.key = nn.Linear(input_dim, hidden_dim)
        self.value = nn.Linear(input_dim, hidden_dim)
        
    def forward(self, x):
        q = self.query(x)
        k = self.key(x)
        v = self.value(x)
        
        # Compute attention scores
        attention_scores = torch.matmul(q, k.transpose(-2, -1))
        attention_scores = F.softmax(attention_scores, dim=-1)
        
        # Weighted sum using attention scores
        attended_values = torch.matmul(attention_scores, v)
        
        return attended_values, attention_scores

# Define vocabulary and word-to-index mapping
vocab = ["i", "am", "learning", "to", "code"]
word_to_idx = {word: idx for idx, word in enumerate(vocab)}

# Define index-to-word mapping
idx_to_word = {idx: word for word, idx in word_to_idx.items()}

# Create input embeddings (example embeddings)
embeddings = torch.randn(len(vocab), 160)

# Define input sentence
input_sentence = "I am learning to code."

# Preprocess input sentence (remove punctuation and convert to lowercase)
translator = str.maketrans('', '', string.punctuation)
input_sentence = input_sentence.translate(translator).lower()

# Convert input sentence to embeddings
input_idxs = [word_to_idx[word] for word in input_sentence.split()]
input_embed = embeddings[input_idxs]

# Create and apply the attention head
attention_head = AttentionHead(input_dim=160, hidden_dim=1600)
output, attention_scores = attention_head(input_embed)

# Find the index with the highest attention score for each embedding
output_idxs = [attention_scores[i].argmax().item() for i in range(len(attention_scores))]

# Translate the output indices back to words
output_words = [idx_to_word[idx] for idx in output_idxs]

print("Input Sentence:", input_sentence)
print("Translated Output:", " ".join(output_words))
