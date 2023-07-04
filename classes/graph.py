from classes.activity import Activity


class Graph:
    def __init__(self):
        self.graph:dict = {}
        self.nodes:dict = {}
        self.init_activity:Activity = None
        self.final_activity:Activity = None

    def add_activity(self, act:Activity):
        if act.number in self.nodes:
            raise Exception(f"Disculpe, ya existe la actividad número {act.number}")

        self.graph[act.number] = []
        self.nodes[act.number] = act

        for predecessor in act.predecessors:
            if predecessor not in self.graph:
                self.graph[predecessor] = []
            self.graph[predecessor].append(act)
            pred:Activity = self.nodes[predecessor]
            pred.add_successor(act.number)
        
    def remove_activity(self, act_number:str):
        if (act_number not in self.nodes):
            raise Exception(f"Disculpe, no se encontró la actividad número {act_number}")
        act:Activity = self.nodes[act_number]
        for predecessor in act.predecessors:
            pred:Activity = self.nodes[predecessor]
            neighbors:list = self.graph[pred.number]
            neighbors.remove(act)
            pred.remove_successor(act_number)
        for successor in act.successors:
            suc:Activity = self.nodes[successor]
            suc.remove_predecessor(act_number)
        self.nodes.pop(act_number)
        self.graph.pop(act_number)

    def find_critical_path(self):
        #Limpiamos la data almacenada de las actividades
        self.restart_activities()
        #Obtenemos la actividad origen y final
        self.final_activity = self.find_final_activities()
        self.init_activity = self.find_initial_activities()

        # Realizar cálculo de fechas tempranas
        self.calculate_early_dates()
        # Realizar cálculo de fechas tardías
        self.calculate_late_dates()

        # Encontrar actividades en la ruta crítica
        critical_path = []
        min_execution_time = 0
        for activity in self.nodes.values():
            if activity.duration > 0 and activity.get_holgura() == 0:
                min_execution_time += activity.duration
                critical_path.append(activity)

        return critical_path, min_execution_time

    def calculate_early_dates(self):
        initial_activity = self.init_activity
        initial_activity.update_early_dates(0)
        self.calculate_early_dates_recursive(initial_activity)

    def calculate_early_dates_recursive(self, activity):
        for successor in activity.successors:
            successor_activity = self.nodes[successor]
            if successor_activity.esd is None or successor_activity.esd < activity.efd:
                successor_activity.update_early_dates(activity.efd)
                self.nodes[successor_activity.number] = successor_activity
                self.calculate_early_dates_recursive(successor_activity)

    def calculate_late_dates(self):
        final_activity = self.final_activity
        final_activity.update_late_dates(final_activity.efd)
        self.calculate_late_dates_recursive(final_activity)

    def calculate_late_dates_recursive(self, activity):
        for predecessor in activity.predecessors:
            predecessor_activity = self.nodes[predecessor]
            if predecessor_activity.lfd is None or predecessor_activity.lfd > activity.lsd:
                predecessor_activity.update_late_dates(activity.lsd)
                self.nodes[predecessor_activity.number] = predecessor_activity
                self.calculate_late_dates_recursive(predecessor_activity)

    def find_initial_activities(self):
        initial_activities = []
        if '0' in self.nodes:
                self.remove_activity('0')
        for activity in self.nodes.values():
            if not activity.predecessors:
                initial_activities.append(activity)
        if len(initial_activities) == 0:
            # No se encontró ningún nodo sin predecesores
            raise Exception("No se encontró ninguna actividad inicial.")
        elif len(initial_activities) > 1:
            # Crear una actividad adicional como nodo inicial
            initial_activity = Activity("0", "Nodo Inicial", 0, predecessors=[])
            neighbors = []
            for activity in initial_activities:
                initial_activity.add_successor(activity.number)
                activity.add_predecessor(initial_activity.number)
                neighbors.append(activity)
            self.nodes[initial_activity.number] = initial_activity
            self.graph[initial_activity.number] = neighbors
            return initial_activity
        else:
            return initial_activities[0]

    def find_final_activities(self):
        final_activities = []

        if '999' in self.nodes:
                self.remove_activity('999')

        for activity in self.nodes.values():
            if not activity.successors:
                final_activities.append(activity)
        if len(final_activities) == 0:
            # No se encontró ningún nodo sin sucesores
            raise Exception("No se encontró ninguna actividad final.")
        elif len(final_activities) > 1:
            # Crear una actividad adicional como nodo final
            final_activity = Activity("999", "Nodo Final", 0, predecessors=[])
            for activity in final_activities:
                final_activity.add_predecessor(activity.number)
            self.add_activity(final_activity)
            return final_activity
        else:
            return final_activities[0]

    def restart_activities(self):
        self.init_activity = None
        self.final_activity = None
        for act in self.nodes.values():
            act.reset()

    def print_graph(self):
            for activity in self.nodes.values():
                print(f"Activity: {activity.number}")
                print(f"Description: {activity.description}")
                print(f"Duration: {activity.duration}")
                print("Predecessors:", activity.predecessors)
                print("Successors:", activity.successors)
                print(f"ESD: {activity.esd}")
                print(f"EFD: {activity.efd}")
                print(f"LSD: {activity.lsd}")
                print(f"LFD: {activity.lfd}")
                print("Holgura:", activity.get_holgura())
                print("-----------------------")

    def write_graph(self):
        activities = []
        for activity in self.nodes.values():
            text = ""
            text += f"Número: {activity.number}" + "\n"
            text += f"Descripción: {activity.description}" + " | "
            text += f"Duración: {activity.duration}" + " | "
            text += f"ESD: {activity.esd}" + " | "
            text += f"EFD: {activity.efd}" + " | "
            text += f"LSD: {activity.lsd}" + " | "
            text += f"LFD: {activity.lfd}" + " | "
            text +="Holgura:" + str(activity.get_holgura()) + "\n\n\n"
            #activitys +="-----------------------------------------------------------------------------------------\n"
            activities.append(text)
        return activities