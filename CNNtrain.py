from src.CNN.CNNModel import CNNModel
from src.Dataset import MelodyDataset
from torch.utils.data import DataLoader
from torch import Tensor, optim, nn
import torch
from tqdm import tqdm

batchsize = 10
epoch_num = 1
lrRate = 1e-3

trainDataSet = MelodyDataset()
trainDataLoader = DataLoader(dataset=trainDataSet,
                             batch_size=batchsize,
                             shuffle=True,
                             drop_last=True)
model = CNNModel()
optimizer = optim.Adam(model.parameters(), lr=lrRate)
lossFn = nn.CrossEntropyLoss(reduction='sum')

para_num = 0
for p in model.parameters():
    para_num += p.numel()   
print("Total number of parameters is %d" %(para_num))

for epoch in tqdm(range(1, epoch_num + 1), total=epoch_num, ncols=80):
    batch_loss = 0
    batch_id = 1
    batch_num = trainDataSet.__len__() // batchsize
    for melodyBatch, labelBatch in tqdm(trainDataLoader, ncols=80, total=batch_num):
        optimizer.zero_grad()
        logits = model(melodyBatch)
        loss = lossFn(logits, labelBatch)
        loss.backward()
        optimizer.step()
        batch_loss += loss.item()
        
        tqdm.write("Loss for batch {} is {}".format(batch_id, loss.item()))
        batch_id += 1
        
torch.save(model, 'src/CNN/model.pt')