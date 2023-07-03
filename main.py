
from classes.activity import Activity
from classes.graph import Graph



def print_critical_path(duracion_minima, critical_activities):
    print("\nDuración mínima del proyecto: ", duracion_minima)
    print("Actividades críticas:")
    for actividad in critical_activities:
        print("Número:", actividad.number)
        print("Descripción:", actividad.description)
        print("Duración:", actividad.duration)
        print()

def create_activity():
    number:str = input('Número de actividad: ')
    desc:str = input('Descripción de actividad: ')
    duration:float = float(input('Duración de actividad: '))
    predecessors:str = input('Predecesores separados por coma: ')

    predList = [p.strip() for p in predecessors if p.strip()]

    return Activity(number=number, description=desc, duration=duration, predecessors=predList)

def main():
    print("----- Programa para calcular la ruta crítica -----")

    graph = Graph()
    
    while True:
        option = input('''
            1. Añadir actividad
            2. Encontrar ruta crítica
            3. Salir
            >>> ''')

        if (option == '1'):
            graph.add_activity(create_activity())
        elif (option == '2'):
            crit_path = graph.find_critical_path()
            path = ''
            for node in crit_path:
                path += node + ' > '
            print(path)
        else:
            break





if __name__ == '__main__':
    main()
