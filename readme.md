# GA(Genetic Algorithm) Composition

北京大学2023秋季《音乐与数学》课程作业

## 1. 运行环境
建议使用conda配置环境

- python=3.12.0
- numpy=1.26.0
- musicpy=6.89
- pytorch=2.1.0

## 2. 目录结构

- /output 下为最终生成结果，我们使用传统适应度的遗传算法，以及添加CNN的版本各进行了50次遗传算法实验，挑选了具有代表性的结果
- /src 下为项目实现的主要源码
- /tutorial 下包含关于musicpy调试的相关信息
- main.py文件是运行遗传算法的入口文件

## 3. 执行命令
在根目录下执行 ``python main.py > result.txt ``将执行遗传算法，结果将输出到result.txt中
``python Checkdata.py source.txt dest.txt`` 将Rawdata文本文件（以音名标注）检查并转换为可读取数据文件
``python CNNtrain.py  > result.txt`` 训练一个CNN分类器
``python CNNtest.py > result.txt `` 在测试集上测试分类的准确性