from interface.interface import start
from classes.activity import Activity
from classes.graph import Graph
from scripts.csv import getActivitiesData


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

    graph = Graph()
    
    getActivitiesData(graph)

    start(graph)
    
    # while True:
    #     option = input('''
    #         1. Añadir actividad
    #         2. Encontrar ruta crítica
    #         3. Ver actividades
    #         4. Salir
    #         >>> ''')

    #     if (option == '1'):
    #         graph.add_activity(create_activity())
    #     elif (option == '2'):
    #         crit_path = graph.find_critical_path()
    #         path = ''
    #         for node in crit_path:
    #             path += node.number + ' > '
    #         print(f'Critical path: {path}')
    #         graph.print_graph()
    #     elif (option == '3'):
    #         graph.print_graph()
    #     else:
    #         break





if __name__ == '__main__':
    main()
