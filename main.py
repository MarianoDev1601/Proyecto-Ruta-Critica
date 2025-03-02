from interface.interface import start
from classes.activity import Activity
from classes.graph import Graph
from scripts.csv import delete_activity, getActivitiesData, save_activity
from interface.interface import drawGraphNX, drawGraph


def create_activity():
    number:str = input('Número de actividad: ')
    desc:str = input('Descripción de actividad: ')
    duration:float = float(input('Duración de actividad: '))
    predecessors:str = input('Predecesores separados por coma: ')
    if predecessors is not None and predecessors != '':
            predList = predecessors.split(',')
    else:
        predList = []

    return Activity(number=number, description=desc, duration=duration, predecessors=predList)

def main():
    # print("----- Programa para calcular la ruta crítica -----")

    graph:Graph = Graph()
    
    getActivitiesData(graph)
    start(graph)





if __name__ == '__main__':
    main()
