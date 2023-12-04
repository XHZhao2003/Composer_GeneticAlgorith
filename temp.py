import torch
from src.Dataset import MelodyDataset
from torch.utils.data import DataLoader


model = torch.load('src/CNN/model.pt')
lossFn = torch.nn.CrossEntropyLoss()

trainDataSet = MelodyDataset()
trainDataLoader = DataLoader(dataset=trainDataSet,
                             batch_size=1, 
                             drop_last=True)
for melodybatch, labelbatch in trainDataLoader:
    logit = model(melodybatch)
    loss = lossFn(logit, labelbatch)
    print(loss.item())

