from torch.utils.data import Dataset
from torch.nn import functional as F
from torch import Tensor
import torch
from .Melody import Melody

class MelodyDataset(Dataset):
    def __init__(self, datapath='data/train/') -> None:
        super().__init__()
        self.datapath = datapath
        self.max_length = 32
        self.melodies = []          # 每个元素是长为32的list
        self.labels = []            # Ground Truth 标签
        self.length = 0             # 元素个数
        self.positiveLength = 0
        self.negativeLength = 0
        self.ReadRawData()
        
    def ReadRawData(self):
        positiveDataPath = self.datapath + 'positive.txt'
        negativeDataPath = self.datapath + 'negative.txt'
        with open(positiveDataPath, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                notes = line.split()
                notes = [int(x) for x in notes]
                self.melodies.append(notes)
                self.labels.append([1, 0])
                self.positiveLength += 1
                self.length += 1
        print("Read %d positive samples into dataset" % self.positiveLength)
                
        with open(negativeDataPath, 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                notes = line.split()
                notes = [int(x) for x in notes]
                self.melodies.append(notes)
                self.labels.append([0, 1])
                self.negativeLength += 1
                self.length += 1
        print("Read %d negative samples into dataset" % self.negativeLength)
        
    def __len__(self):
        return self.length
    
    def __getitem__(self, index):
        return Tensor([self.melodies[index]]), Tensor(self.labels[index])
                
        
    