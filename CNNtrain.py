from src.CNN.CNNModel import CNNModel
from src.Dataset import MelodyDataset
from torch.utils.data import DataLoader
from torch import Tensor, optim, nn
import torch
from tqdm import tqdm

batchsize = 16
epoch_num = 500
lrRate = 3e-5

trainDataSet = MelodyDataset()
trainDataLoader = DataLoader(dataset=trainDataSet,
                             batch_size=batchsize)
model = CNNModel()
optimizer = optim.Adam(model.parameters(), lr=lrRate)
lossFn = nn.CrossEntropyLoss()

para_num = 0
for p in model.parameters():
    para_num += p.numel()   
print("Total number of parameters is %d" %(para_num))

for epoch in tqdm(range(1, epoch_num + 1), total=epoch_num, ncols=80):
    epoch_loss = 0
    for melodyBatch, labelBatch in trainDataLoader:
        optimizer.zero_grad()
        logits = model(melodyBatch)
        loss = lossFn(logits, labelBatch)
        loss.backward()
        optimizer.step()
        epoch_loss += loss.item()
    print("Loss for epoch {} is {}".format(epoch, epoch_loss))
torch.save(model, 'src/CNN/model.pt')

