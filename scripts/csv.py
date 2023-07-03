import pandas as pd

from classes.graph import Graph
from classes.activity import Activity


def getActivitiesData(graph: Graph):
    # Leer el archivo de Excel
    data_frame = pd.read_excel("data/activitiesData.xlsx", header=0,converters={'number':str,'description':str,'duration':float,'predecessors':str})
    # Iterar sobre cada fila
    for index, row in data_frame.iterrows():
        # Acceder a los valores de cada columna
        number:str = row['number']
        description:str = row['description']
        duration:float = float(row['duration'])
        predecessors:str = str(row['predecessors'])
        if predecessors is not None and predecessors != '' and predecessors != 'nan':
            predList = predecessors.split(',')
        else:
            predList = []
        graph.add_activity(Activity(number, description, duration, predList))

# def save_activity(activity):
#     pd.