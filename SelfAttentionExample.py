import torch
import torch.nn as nn
import torch.nn.functional as F

class SelfAttention(nn.Module):
    def __init__(self, hidden_size):
        super(SelfAttention, self).__init__()
        self.query_linear = nn.Linear(hidden_size, hidden_size)
        self.key_linear = nn.Linear(hidden_size, hidden_size)
        self.value_linear = nn.Linear(hidden_size, hidden_size)
        self.softmax = nn.Softmax(dim=-1)

    def forward(self, x):
        query = self.query_linear(x)
        key = self.key_linear(x)
        value = self.value_linear(x)

        attention = self.softmax(torch.matmul(query, key.transpose(-1, -2)))

        output = torch.matmul(attention, value)

        return output

def main():
    hidden_size = 10
    x = torch.randn(1, 3, hidden_size)
    attention = SelfAttention(hidden_size)
    output = attention(x)
    print(output)

if __name__ == "__main__":
    main()
