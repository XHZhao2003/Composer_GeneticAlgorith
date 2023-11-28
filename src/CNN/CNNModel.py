from torch import nn
import torch

class CNNMelodyModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.channels = [16, 64]
        self.kernelSize = [3, 3]
        self.linearDim = [256, 2]
        self.conv1 = nn.Sequential(
            nn.Conv1d(1, self.channels[0], self.kernelSize[0], padding=1, bias=True),
            nn.BatchNorm1d(self.channels[0]),
            nn.ReLU(True)            
        )
        self.conv2 = nn.Sequential(
            nn.Conv1d(self.channels[0], self.channels[1], self.kernelSize[1], padding=1, bias=True),
            nn.BatchNorm1d(self.channels[1]),
            nn.ReLU(True)            
        )
        self.pooling = nn.AvgPool1d(32, 32)
        self.linear = nn.Sequential(
            nn.Linear(self.channels[-1], self.linearDim[0]),
            nn.ReLU(True),
            nn.Linear(self.linearDim[0], self.linearDim[1])
        )
        
    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.pooling(x)
        x = torch.squeeze(x, dim=2)     # (batchsize, features, 1) => (batchsize, features)
        x = self.linear(x)
        return x
