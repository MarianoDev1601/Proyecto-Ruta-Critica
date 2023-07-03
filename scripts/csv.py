import pandas as pd
from classes.activity import Activity
from classes.graph import Graph


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

def save_activity(activity: Activity):
    # Leer el archivo de Excel existente
    data_frame = pd.read_excel("data/activitiesData.xlsx", header=0, converters={'number': str, 'description': str, 'duration': float, 'predecessors': str})

    # Crear un nuevo DataFrame con los datos de la actividad
    new_data = pd.DataFrame({
        'number': [activity.number],
        'description': [activity.description],
        'duration': [activity.duration],
        'predecessors': [','.join(activity.predecessors)]
    })

    # Combinar los datos existentes con los nuevos datos
    updated_data_frame = pd.concat([data_frame, new_data], ignore_index=True)

    # Guardar el DataFrame actualizado en el archivo Excel
    updated_data_frame.to_excel("data/activitiesData.xlsx", index=False)








