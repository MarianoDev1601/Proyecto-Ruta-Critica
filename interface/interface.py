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
          
    plt.clf()  
    # Dibujar el grafo
    nx.draw(g, with_labels=True, node_color='lightblue', node_size=500, font_size=10, edge_color='gray', width=1, alpha=0.7)

    # Etiquetas de las aristas
    labels = nx.get_edge_attributes(g, 'duration')
    nx.draw_networkx_edge_labels(g, pos=nx.spring_layout(g, seed=900), edge_labels=labels)

    # Agregar el canvas al lado derecho
    canvas = FigureCanvasTkAgg(plt.gcf(), master = right_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    return
    # graph.graph['1'][0].description
    
def drawGraph(graph):
    g = nx.DiGraph()
    for node,neighbors in graph.graph.items():
        g.add_node(node)
        for neighbor in neighbors:
            g.add_edge(node, neighbor.number)
                
    plt.clf()
    nx.draw(g, with_labels=True)
    
    # Agregar el canvas al lado derecho
    canvas = FigureCanvasTkAgg(plt.gcf(), master = right_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

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

    # Define the label text and positions
    labels = {}
    
    for node, neighbors in graph.graph.items():
        
        activity = graph.nodes[node]    
        esd_values = ", ".join([f"{activity.esd}"])
        efd_values = ", ".join([f"{activity.efd}"])
        lsd_values = ", ".join([f"{activity.lsd}"])
        lfd_values = ", ".join([f"{activity.lfd}"])
        labels[node] = f"ESD: {esd_values}\nEFD: {efd_values}\nLSD: {lsd_values}\nLFD: {lfd_values}\n"

        if activity in criticalPath:
            node_colors_criticalPath[node] = 'red'
            # Se verifica si el nodo que se está revisando es el último para poder setear correctamente el nodo origen y destino
        else:
            node_colors_criticalPath[node] = "gray"
            node_colors_criticalEdge[node] = 'gray'
            continue
        # En caso de que node se encuentre en el camino critico, se pinta de rojo su arista y se coloca su peso para ser visualizado
        # node_colors_criticalEdge[(origNode, destNode)] = 'red'
        # node_colors_criticalEdge[(destNode, origNode)] = 'red'
        
    first_node = graph.init_activity.number
    last_node = graph.final_activity.number

    node_colors_criticalPath[first_node] = "green"
    print(first_node)
    node_colors_criticalPath[last_node] = "purple"

    colors_criticalPath = [node_colors_criticalPath[node] 
                            for node in g.nodes()]
    colors_criticalEdge = [node_colors_criticalEdge.get(
    edge, 'gray') for edge in g.edges()]
    # ESD: {node.esd}, EFD: {node.efd}, LSD: {node.lsd}, LFD: {node.lfd}
    
    plt.clf()
    # Dibujar el grafo
    nx.draw(g, pos=posNX, with_labels=True, node_size=400, node_color=colors_criticalPath,
            font_size=10, edge_color=colors_criticalEdge, width=1, alpha=0.7)

    # Dibujar las etiquetas de los nodos
    nx.draw_networkx_labels(g, pos=posNX, labels=labels, horizontalalignment= 'right', verticalalignment= 'bottom', font_size=10, font_color='blue', font_family='Arial')
    # nx.draw_networkx_edge_labels(
    #     g, posNX, font_color='black', font_size=10, font_family='Arial')

    for widget in right_frame.winfo_children():
        widget.destroy()
    # Agregar el canvas al lado derecho
    canvas = FigureCanvasTkAgg(plt.gcf(), master=right_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

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
    index = 1
    pathR, min = Graph.find_critical_path(graph)
    
    # for act in pathR: 
    #     if index <= len(pathR):
    #         pathT += str(act.number) + "--->"
    #         index += 1
    #     else:
    #         pathT += act
            
    # if pathT == "":
    #     path["text"] = "No existe."
    # else:
    #     path["text"] = pathT
    
    drawGraphNX(graph, pathR)

def addAc(graph: Graph, numberIn, descriptionIn, durationIn, predecessorsList):
    nodeList = []
    for activity in graph.nodes.values():
        nodeList.append(activity.number)
    if (numberIn.get() not in nodeList):
        if (descriptionIn.get() != ""):
            try:
                act = Activity(numberIn.get(), descriptionIn.get(), float(durationIn.get()), predecessorsList)
                print(numberIn.get())
                Graph.add_activity(graph, act)
                upgradePredecessors(graph)
                removeIn['values']=activityList
                removeIn.set("")
                activityInterface.destroy()
                save_activity(act)
                upgradePath(graph)
                
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
        #delete_activity(act.get())
        upgradePath(graph)
    else:
        messagebox.showerror("Error", "Seleccione la actividad a eliminar.")
        
def write(graph:Graph):
    writeInterface = tk.Tk()
    writeInterface.title("Información de los Nodos")
    writeInterface.configure(bg="orange")
    
    # Crear un Frame para contener el widget de texto desplazable y el Scrollbar
    frame = ttk.Frame(writeInterface)
    frame.pack(fill=tk.BOTH, expand=True)
    
    # Crear el Scrollbar vertical
    scrollbar = ttk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Crear el widget de texto desplazable
    text = tk.Text(frame, yscrollcommand=scrollbar.set, bg="orange", font=("Arial", 20))
    text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Configurar la relación entre el Scrollbar y el widget de texto desplazable
    scrollbar.config(command=text.yview)
    
    # Obtener el contenido a mostrar en el widget de texto desplazable
    activities = Graph.write_graph(graph)
    text_content = '\n'.join(activities)
    
    # Insertar el contenido en el widget de texto desplazable
    text.insert(tk.END, text_content)
    
    writeInterface.mainloop()

def addActivity(graph: Graph):
    global activityInterface, predecessorsIn
    upgradePredecessors(graph)
    
    # Crear ventana para añadir actividades
    activityInterface = tk.Tk()
    activityInterface.title("Añadir actividad")
    activityInterface.configure(bg="orange")
    separator = ttk.Label(activityInterface, text= "", background="orange")
    separator.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")
    
    # Construcción de la ventana   
    number = ttk.Label(activityInterface, text="Número:", style="TLabel", font=("Arial", 18), background="orange")
    number.grid(row=1, column=0, padx=10)
    numberIn= ttk.Spinbox(activityInterface, from_=1, to=998, font=("Arial", 18))
    numberIn.grid(row=2, column=0, padx=10, pady=(5,25))
     
    description = ttk.Label(activityInterface, text="Descripción:", style="TLabel", font=("Arial", 18), background="orange")
    description.grid(row=1, column=1, padx=10)
    descriptionIn = ttk.Entry(activityInterface, font=("Arial", 18))
    descriptionIn.grid(row=2, column=1, padx=10, pady=(5,25))
    descriptionIn.configure(font=("Arial", 18))
    
    duration = ttk.Label(activityInterface, text="Duración:", style="TLabel", font=("Arial", 18), background="orange")
    duration.grid(row=3, column=0, padx=10)
    durationIn= ttk.Spinbox(activityInterface, from_=1, to=998, font=("Arial", 18))
    durationIn.grid(row=4, column=0, padx=10, pady=(5,25))
    
    predecessors = []
    
    predecessorsL = ttk.Label(activityInterface, text="Predecesores:", style="TLabel", font=("Arial", 18), background="orange")
    predecessorsL.grid(row=3, column=1, padx=10)
    predecessorsIn = ttk.Combobox(activityInterface, values=activityList, font=("Arial", 18))
    predecessorsIn.grid(row=4, column=1, padx=(10,5), pady=(5,25), sticky="ew")
    addPredecessorB = ttk.Button(activityInterface, text="+", style="TButton", command=lambda:addPredecessor(predecessors, predecessorsIn))
    addPredecessorB.grid(row=4, column=2, pady=(5,25), padx=(5,10))
    addPredecessorB.configure(width = 3)
    
    add = ttk.Button(activityInterface, text="Añadir Tarea", style="TButton", command=lambda:addAc(graph, numberIn, descriptionIn, durationIn, predecessors))
    add.grid(row=5, column=0, pady=30, columnspan=3)
    
    
    activityInterface.mainloop()

def start(graph: Graph):
    global interface, right_frame, left_frame, removeIn, path
    upgradePredecessors(graph)
   
   # Crear la ventana principal
    interface = tk.Tk()
    interface.title("MetroCrítico")
    interface.configure(bg="orange")

    style = ttk.Style()
    style.configure("TLabel", font=("Arial", 16), background="orange")
    style.configure("TButton", font=("Arial", 18), bg= "orange")
    style.configure("TFrame", background="orange")
    style.configure("TSeparator", background="orange")

    # Lado izquierdo
    left_frame = ttk.Frame(interface, style="TFrame")
    left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Título centrado
    title = ttk.Label(left_frame, text="Bienvenido a MetroCrítico",font=("Arial", 20), background="orange")
    title.grid(row=0, column=0, columnspan=4, pady=10)
    
    # Lado derecho
    right_frame = ttk.Frame(interface, style="TFrame")
    right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    interface.columnconfigure(1, weight=1) 
    interface.rowconfigure(0, weight=1)
    
    # Configuración de expansión de filas y columnas
    interface.grid_rowconfigure(0, weight=1)
    interface.grid_columnconfigure(1, weight=1)

    #Construcción lado izquierdo
    add = ttk.Button(left_frame, text="Añadir nueva tarea", style="TButton", command=lambda: addActivity(graph))
    add.grid(row=1, column=0, pady=(10,30), columnspan=2, sticky="ew")
    
    removeIn = ttk.Combobox(left_frame, values=activityList)
    removeIn.grid(row=2, column=0, padx=(10,5), pady=(5, 30))
    remove = ttk.Button(left_frame, text="Eliminar tarea", style="TButton", command=lambda: removeAc(graph, removeIn))
    remove.grid(row=2, column=1, pady=(5, 30))
    
    print = ttk.Button(left_frame, text="Ver información de los nodos", style="TButton", command=lambda: write(graph))
    print.grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)
    
    pathL = ttk.Label(left_frame, text="Leyenda:", style="TLabel", anchor='w')
    pathL.grid(row=4, column=0, pady=10)
    
    path = ttk.Label(left_frame, text="Nodo verde: Actividad Inicial\nNodo Mordado: Actividad Final\nNodo Rojo: Pertenece a la Ruta Crítica", style="TLabel")
    path.grid(row=5, column=0, columnspan=2)
    
    
    upgradePath(graph)
    
    interface.mainloop()