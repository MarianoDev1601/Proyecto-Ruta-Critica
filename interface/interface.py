from classes.graph import Graph
from classes.activity import Activity
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def addPredecessor(predecessors, predecessor):
    predecessors.append(predecessor.get())
    activityList.remove(predecessor.get())
    predecessorsIn['values']=activityList
    predecessorsIn.set("")

def upgradePredecessors(graph: Graph):
    global activityList
    activityList = []
    for activity in graph.nodes.values():
        activityList.append(activity.number)

def addAc(graph: Graph, numberIn, descriptionIn, durationIn, predecessorsList):
    nodeList = []
    for activity in graph.nodes.values():
        nodeList.append(activity.number)
    if ((numberIn.get() not in nodeList) and descriptionIn.get() != "" and durationIn != ""):
        Graph.add_activity(graph, Activity(numberIn.get(), descriptionIn.get(), float(durationIn.get()), predecessorsList))
    else:
        messagebox.showerror("Error", "Asegurese de rellenar correctamente todos los campos.")
        
def removeAc(graph:Graph, act):
    Graph.remove_activity(graph, act.get())
    upgradePredecessors(graph)
    removeIn['values']=activityList
    removeIn.set("")

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
    global interface, right_frame, left_frame, removeIn
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
    removeIn.grid(row=2, column=0, padx=(10,5),)
    remove = ttk.Button(left_frame, text="Eliminar tarea", style="TButton", command=lambda: removeAc(graph, removeIn))
    remove.grid(row=2, column=1,)

    interface.mainloop()