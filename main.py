from interface.interface import start
from classes.activity import Activity
from classes.graph import Graph
from scripts.csv import delete_activity, getActivitiesData, save_activity
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


def drawGraph(graph):
    g = nx.DiGraph()
    for node,neighbors in graph.graph.items():
        g.add_node(node)
        for neighbor in neighbors:
            g.add_edge(node, neighbor.number)
                
    nx.draw(g, with_labels=True)
    plt.show()

def main():
    # print("----- Programa para calcular la ruta crítica -----")

    graph:Graph = Graph()
    
    getActivitiesData(graph)

    drawGraph(graph)
    # start(graph)
    
    # while True:
    #     option = input('''
    #         1. Añadir actividad
    #         2. Encontrar ruta crítica
    #         3. Eliminar actividad
    #         4. Ver actividades
    #         5. Salir
    #         >>> ''')

    #     if (option == '1'):
    #         activity:Activity = create_activity()
    #         graph.add_activity(activity)
    #         save_activity(activity)
    #     elif (option == '2'):
    #         crit_path, min_execution_time = graph.find_critical_path()
    #         path = ''
    #         if (len(crit_path) > 0):
    #             for node in crit_path:
    #                 path += node.number + ' > '
    #             print(f'Critical path: {path}')
    #             print(f'Mínimo tiempo de ejecución: {min_execution_time}')
    #         else:
    #             print('No hay ruta crítica')
    #         graph.print_graph()
    #     elif (option == '3'):
    #         activity_num = input('Ingrese el número de la actividad a eliminar: ')
    #         graph.remove_activity(activity_num)
    #         delete_activity(activity_num)
    #     elif (option == '4'):
    #         graph.print_graph()
        
    #     else:
    #         break





if __name__ == '__main__':
    main()
