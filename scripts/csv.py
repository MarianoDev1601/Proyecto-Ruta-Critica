import pandas as pd

from classes.graph import Graph
from classes.node import Node


def getNodesData(graph: Graph):
    # Leer el archivo de Excel
    data_frame = pd.read_excel("data/nodeData.xlsx")

    # Iterar sobre cada fila
    for index, row in data_frame.iterrows():
        # Acceder a los valores de cada columna
        continue


def getEdgesData(graph: Graph):
    # Leer el archivo de Excel
    data_frame = pd.read_excel("data/edgesData.xlsx")

    # Iterar sobre cada fila
    for index, row in data_frame.iterrows():
        # Acceder a los valores de cada columna
        continue
