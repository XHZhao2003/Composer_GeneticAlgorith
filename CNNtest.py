from src.CNN.CNNModel import CNNModel
from src.Dataset import MelodyDataset
from torch.utils.data import DataLoader
from torch import Tensor, optim, nn
import torch
from tqdm import tqdm

testDataSet = MelodyDataset("data/test/")
testDataLoader = DataLoader(dataset=testDataSet,
                             batch_size=1,
                             drop_last=True)
model = torch.load("src/CNN/model.pt")

softmax = nn.Softmax(dim=1)
cnt = 0
total = 0
for melody, label in testDataLoader:
    logits = model(melody)
    pred = softmax(logits)[0]
    predPos = pred[0].item()
    predNeg = pred[1].item()
    label = label[0]
    score = label[0]*predPos + label[1]*predNeg
    print(pred, label)
    if score > 0.5:
        cnt += 1
    total += 1
print("Total %d, Hit %d, Accuracy %f" % (total, cnt, cnt/total))