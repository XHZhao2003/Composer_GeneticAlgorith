from src.Seed import Seed

# 随机生成模型的负样本
seed = Seed()
negativeDataPath = 'data/random.txt'
with open(negativeDataPath, 'w') as f:
    for i in range(2):
        seed.RandomMelody()
        for j in range(10):
            notes = [str(note) for note in seed.melodyseed[j].notes]
            notes = ' '.join(notes) + '\n'
            f.write(notes)

