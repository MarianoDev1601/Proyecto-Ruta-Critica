from classes.graph import Graph
from classes.activity import Activity
from scripts.csv import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def drawGraphNXa(graph: Graph):
    g = nx.Graph()
    
    for node, predecessors in graph.graph.items():
        for predecessor in predecessors:
            g.add_edge(node, predecessor)
    # Dibujar el grafo
    nx.draw(g, with_labels=True, node_color='lightblue', node_size=500,
            font_size=10, edge_color='gray', width=1, alpha=0.7)

    # Etiquetas de las aristas
    labels = nx.get_edge_attributes(g, 'duration')
    nx.draw_networkx_edge_labels(
        g, pos=nx.spring_layout(g, seed=900), edge_labels=labels)

    # Mostrar el gráfico
    plt.show()
    return
    # graph.graph['1'][0].description
def drawGraph(graph):
    g = nx.DiGraph()
    for node,neighbors in graph.graph.items():
        g.add_node(node)
        for neighbor in neighbors:
            g.add_edge(node, neighbor.number)
                
    nx.draw(g, with_labels=True)
    plt.show()

def drawGraphNX(graph: Graph, criticalPath: list):
    g = nx.DiGraph()

    # Agregar nodos y aristas al grafo
    for node, neighbors in graph.graph.items():
        for neighbor in neighbors:
            g.add_edge(node, neighbor.number)

    # Crear un layout para el grafo
    posNX = nx.spring_layout(g, seed=900)
    
    # Diccionario para elegir el color del path tomado para el camino mas corto
    node_colors_criticalPath = {}

    # Diccionario para elegir el color de los edges tomados para el camino mas corto
    node_colors_criticalEdge = {}

    # Diccionario para agregarle le peso al camino usado
    edge_labels = {}

    for node, neighbors in graph.graph.items():
        origNode = ''
        destNode = ''
        for neighbor in neighbors:
            edge_labels[(node, neighbor.number)] = str(neighbor.esd)+', ' +str(neighbor.efd)+', ' +str(neighbor.lsd)+', ' +str(neighbor.lfd)
        if node in criticalPath:
            node_colors_criticalPath[node] = 'red'
            pos = criticalPath.index(node)
            if (pos == 0):
                node_colors_criticalPath[node] = "green"
                # Se verifica si el nodo que se está revisando es el último para poder setear correctamente el nodo origen y destino
            if (pos == len(criticalPath) - 1):
                origNode = criticalPath[pos - 1]
                destNode = criticalPath[pos]
            else:
                origNode = criticalPath[pos]
                destNode = criticalPath[pos + 1] 
        else:
            node_colors_criticalPath[node] = "gray"
            node_colors_criticalEdge[node] = 'gray'
            continue
        # En caso de que node se encuentre en el camino critico, se pinta de rojo su arista y se coloca su peso para ser visualizado
        node_colors_criticalEdge[(origNode, destNode)] = 'red'
        node_colors_criticalEdge[(destNode, origNode)] = 'red'
        
    colors_criticalPath = [node_colors_criticalPath[node] 
                            for node in g.nodes()]
    colors_criticalEdge = [node_colors_criticalEdge.get(
    edge, 'gray') for edge in g.edges()]
    # ESD: {node.esd}, EFD: {node.efd}, LSD: {node.lsd}, LFD: {node.lfd}
    
    plt.clf()
    # Dibujar el grafo
    nx.draw(g, pos=posNX, with_labels=True, node_size=600, node_color=colors_criticalPath,
            font_size=10, edge_color=colors_criticalEdge, width=1, alpha=0.7)

    # Dibujar las etiquetas de las aristas
    nx.draw_networkx_edge_labels(
        g, posNX, edge_labels=edge_labels, font_color='black', font_size=10, font_family='Arial')
    plt.show()
    # Agregar el canvas al lado derecho
    # canvas = FigureCanvasTkAgg(plt.gcf(), master=right_frame)
    # canvas.draw()
    # canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def addPredecessor(predecessors, predecessor):
    if (predecessor.get() != ""):
        predecessors.append(predecessor.get())
        activityList.remove(predecessor.get())
        predecessorsIn['values']=activityList
        predecessorsIn.set("")
    else:
        messagebox.showerror("Error", "Asegurese de seleccionar una actividad.")

def upgradePredecessors(graph: Graph):
    global activityList
    activityList = []
    for activity in graph.nodes.values():
        activityList.append(activity.number)
    
def upgradePath(graph:Graph):
    pathT = ""
    index = 0
    pathR, min = Graph.find_critical_path(graph)
    for act in pathR: 
        if index < pathR.count():
            pathT += act + "--->"
            index += 1
        else:
            pathT += act
    path["text"] = pathT

def addAc(graph: Graph, numberIn, descriptionIn, durationIn, predecessorsList):
    nodeList = []
    for activity in graph.nodes.values():
        nodeList.append(activity.number)
    if (numberIn.get() not in nodeList):
        if (descriptionIn.get() != ""):
            try:
                Graph.add_activity(graph, Activity(numberIn.get(), descriptionIn.get(), float(durationIn.get()), predecessorsList))
                upgradePredecessors(graph)
                removeIn['values']=activityList
                removeIn.set("")
                activityInterface.destroy()
                save_activity(Activity(numberIn.get(), descriptionIn.get(), float(durationIn.get()), predecessorsList))
                upgradePath(path)
            except ValueError:
                messagebox.showerror("Error", "Indique la duración de la actividad")
        else:
            messagebox.showerror("Error", "Indique la descripción de la actividad")
    else:
        messagebox.showerror("Error", "Ese número de actividad no está disponible")
        
def removeAc(graph:Graph, act):
    if (act.get() != ""):
        Graph.remove_activity(graph, act.get())
        upgradePredecessors(graph)
        removeIn['values']=activityList
        removeIn.set("")
        delete_activity(act.get())
        upgradePath(path)
    else:
        messagebox.showerror("Error", "Seleccione la actividad a eliminar.")

def addActivity(graph: Graph):
    global activityInterface, predecessorsIn
    upgradePredecessors(graph)
    
    # Crear ventana para añadir actividades
    activityInterface = tk.Tk()
    activityInterface.title("Añadir actividad")
    # addActivity.configure(bg="gray")
    
    # Construcción de la ventana   
    number = ttk.Label(activityInterface, text="Número:", style="TLabel")
    number.grid(row=0, column=0, padx=10)
    numberIn= ttk.Spinbox(activityInterface, from_=1, to=1000)
    numberIn.grid(row=1, column=0, padx=10, pady=(5,15))
     
    description = ttk.Label(activityInterface, text="Descripción:", style="TLabel")
    description.grid(row=0, column=1, padx=10)
    descriptionIn = ttk.Entry(activityInterface)
    descriptionIn.grid(row=1, column=1, padx=10, pady=(5,15))
    
    duration = ttk.Label(activityInterface, text="Duración:", style="TLabel")
    duration.grid(row=2, column=0, padx=10)
    durationIn= ttk.Spinbox(activityInterface, from_=1, to=1000)
    durationIn.grid(row=3, column=0, padx=10, pady=(5,15))
    
    predecessors = []
    
    predecessorsL = ttk.Label(activityInterface, text="Predecesores:", style="TLabel")
    predecessorsL.grid(row=2, column=1, padx=10)
    predecessorsIn = ttk.Combobox(activityInterface, values=activityList)
    predecessorsIn.grid(row=3, column=1, padx=(10,5), pady=(5,15))
    addPredecessorB = ttk.Button(activityInterface, text="Añadir", style="TButton", command=lambda:addPredecessor(predecessors, predecessorsIn))
    addPredecessorB.grid(row=3, column=2, pady=(5,15))
    
    add = ttk.Button(activityInterface, text="Añadir", style="TButton", command=lambda:addAc(graph, numberIn, descriptionIn, durationIn, predecessors))
    add.grid(row=4, column=0, pady=10, columnspan=3)
    
    
    activityInterface.mainloop()

def start(graph: Graph):
    global interface, right_frame, left_frame, removeIn, path
    upgradePredecessors(graph)
   
   # Crear la ventana principal
    interface = tk.Tk()
    interface.title("MetroCrítico")
    interface.configure(bg="orange")

    style = ttk.Style()
    style.configure("TLabel", font=("Arial", 12), background="orange")
    style.configure("TButton", font=("Arial", 12))
    style.configure("TFrame", background="orange")

    # Lado izquierdo
    left_frame = ttk.Frame(interface, style="TFrame")
    left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Título centrado
    title = ttk.Label(left_frame, text="Bienvenido a MetroCrítico",font=("Arial", 20), background="orange")
    title.grid(row=0, column=0, columnspan=4, pady=10)
    
    # Lado derecho
    right_frame = ttk.Frame(interface)
    right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    
    #Construcción lado izquierdo
    add = ttk.Button(left_frame, text="Añadir nueva tarea", style="TButton", command=lambda: addActivity(graph))
    add.grid(row=1, column=0, pady=10, columnspan=2,)
    
    removeIn = ttk.Combobox(left_frame, values=activityList)
    removeIn.grid(row=2, column=0, padx=(10,5))
    remove = ttk.Button(left_frame, text="Eliminar tarea", style="TButton", command=lambda: removeAc(graph, removeIn))
    remove.grid(row=2, column=1,)
    
    pathL = ttk.Label(left_frame, text="Ruta Crítica:", style="TLabel")
    pathL.grid(row=3, column=0, columnspan=4, pady=10)
    
    path = ttk.Label(left_frame, text="No encontrada.", style="TLabel")
    path.grid(row=4, column=0, columnspan=4, pady=10)
    
    upgradePath(graph)
    
    interface.mainloop()