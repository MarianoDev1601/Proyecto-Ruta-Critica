
from classes.activity import Activity
from classes.graph import Graph
from scripts.csv import delete_activity, getActivitiesData, save_activity


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
    print("----- Programa para calcular la ruta crítica -----")

    graph = Graph()
    
    getActivitiesData(graph)

    while True:
        option = input('''
            1. Añadir actividad
            2. Encontrar ruta crítica
            3. Eliminar actividad
            4. Ver actividades
            5. Salir
            >>> ''')

        if (option == '1'):
            activity:Activity = create_activity()
            graph.add_activity(activity)
            save_activity(activity)
        elif (option == '2'):
            crit_path = graph.find_critical_path()
            path = ''
            for node in crit_path:
                path += node.number + ' > '
            print(f'Critical path: {path}')
            graph.print_graph()
        elif (option == '3'):
            activity_num = input('Ingrese el número de la actividad a eliminar: ')
            graph.remove_activity(activity_num)
            delete_activity(activity_num)
        elif (option == '4'):
            graph.print_graph()
        
        else:
            break





if __name__ == '__main__':
    main()
