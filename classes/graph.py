from classes.activity import Activity


class Graph:
    def __init__(self):
        self.graph:dict = {}
        self.nodes:dict = {}
        self.init_activity:Activity = None
        self.final_activity:Activity = None

    def add_activity(self, act:Activity):
        if act.number in self.nodes:
            return
        
        self.graph[act.number] = []
        self.nodes[act.number] = act

        for predecessor in act.predecessors:
            if predecessor not in self.graph:
                self.graph[predecessor] = []
            self.graph[predecessor].append(act)
            self.nodes[predecessor]:Activity.add_successor(act)
        print(self.nodes)
        
    def remove_activity(self, act_number:str):
        act:Activity = self.nodes[act_number]
        for predecessor in act.predecessors:
            self.nodes[predecessor]:Activity.remove_successor(act_number)
        for successor in act.successors:
            self.nodes[successor]:Activity.remove_predecessor(act_number)
        self.nodes.pop(act_number)
        self.graph.pop(act_number)

    def find_critical_path(self):
        # Realizar cálculo de fechas tempranas
        self.calculate_early_dates()

        # Realizar cálculo de fechas tardías
        self.calculate_late_dates()

        # Encontrar actividades en la ruta crítica
        critical_path = []
        for activity in self.nodes.values():
            if activity.get_holgura() == 0:
                critical_path.append(activity)

        return critical_path

    def calculate_early_dates(self):
        initial_activity = self.find_initial_activity()
        initial_activity.update_early_dates(0)
        self.calculate_early_dates_recursive(initial_activity)

    def calculate_early_dates_recursive(self, activity):
        for successor in activity.successors:
            successor_activity = self.nodes[successor]
            if successor_activity.esd is None or successor_activity.esd < activity.efd:
                successor_activity.update_early_dates(activity.efd)
                self.calculate_early_dates_recursive(successor_activity)

    def calculate_late_dates(self):
        final_activity = self.find_final_activity()
        final_activity.update_late_dates(final_activity.efd)
        self.calculate_late_dates_recursive(final_activity)

    def calculate_late_dates_recursive(self, activity):
        for predecessor in activity.predecessors:
            predecessor_activity = self.nodes[predecessor]
            if predecessor_activity.lfd is None or predecessor_activity.lfd > activity.lsd:
                predecessor_activity.update_late_dates(activity.lsd)
                self.calculate_late_dates_recursive(predecessor_activity)

    def find_initial_activity(self):
        for activity in self.nodes.values():
            if not activity.predecessors:
                self.init_activity = activity
                return activity

    def find_final_activity(self):
        for activity in self.nodes.values():
            if not activity.successors:
                self.final_activity = activity
                return activity


    # def find_critical_path(self):
    #     # Inicializar las fechas tempranas de inicio y finalización de las actividades
    #     for node in self.nodes.values():
    #         node.update_early_dates(0.0)

    #     # Calcular la duración mínima del proyecto
    #     duration_min = 0.0
    #     for node in self.nodes.values():
    #         if node.successors:
    #             for successor_num in node.successors:
    #                 successor:Activity = self.nodes[successor_num]
    #                 if successor.esd is None or successor.esd < node.efd:
    #                     successor.update_early_dates(node.efd)
    #                     self.nodes[successor_num] = successor
    #             duration_min = max(duration_min, node.efd)

    #      # Inicializar las fechas tardías de inicio y finalización de las actividades
    #     for node in self.nodes.values():
    #         node.update_late_dates(duration_min - node.duration)

    #     # Calcular las fechas tardías de inicio y finalización de las actividades
    #     for node in reversed(list(self.nodes.values())):
    #         if node.successors:
    #             for successor_number in node.successors:
    #                 successor = self.nodes[successor_number]
    #                 if node.lfd is None:
    #                     node.update_late_dates(successor.lsd - node.duration)
    #                 else:
    #                     node.update_late_dates(min(node.lfd, successor.lsd - node.duration))

    #     # Encontrar las actividades críticas
    #     critical_activities = [node for node in self.nodes.values() if node.get_holgura() == 0]

    #     return duration_min, critical_activities