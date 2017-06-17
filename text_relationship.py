# -*- coding: utf-8 -*-
from relationship import Relationship
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

#自定义节点词典（小说中人物角色）
dictpath = r'Keywords.txt'
#小说路径
datapath = r'Output.txt'
#程序运行生成的角色关系图保存地址
pic = r'关系图.png'
Re = Relationship(dictpath, datapath)
relation = Re.relationship()
graph = Re.network_digraph(relation, pic, ["广东", "云南", "山西", "山东", "广西", "京津唐", "河南"])

