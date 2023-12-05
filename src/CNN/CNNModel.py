from torch import nn
import torch

class CNNModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.channels = [16, 32]
        self.kernelSize = [3, 3]
        self.linearDim = [32, 256, 64, 2]
        self.dropout = 0.3
        self.conv1 = nn.Sequential(
            nn.Conv1d(1, self.channels[0], kernel_size=self.kernelSize[0], padding=1, bias=True),
            nn.ReLU(True)            
        )
        self.conv2 = nn.Sequential(
            nn.Conv1d(self.channels[0], self.channels[1], kernel_size=self.kernelSize[1], padding=1, bias=True),
            nn.ReLU(True)            
        )
        self.pooling = nn.AvgPool1d(32, 32)
        self.linear = nn.Sequential(
            nn.Linear(self.linearDim[0], self.linearDim[1]),
            nn.ReLU(True),
            nn.Dropout(self.dropout),
            nn.Linear(self.linearDim[1], self.linearDim[2]),
            nn.ReLU(True),
            nn.Dropout(self.dropout),
            nn.Linear(self.linearDim[2], self.linearDim[3])
        )
        
    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = self.pooling(x)
        x = torch.squeeze(x, dim=2)     # (batchsize, features, 1) => (batchsize, features)
        x = self.linear(x)
        return x

    def TrainMode(self):
        self.dropout = 0.3
    def TestMode(self):
        self.dropout = 0