import vrplib
import random


class VehicleRoutingProblem():

    def __init__(self, ants) -> None:
        self.numberOfAnts = ants
        self.population = []
        self.costs = []
        vrplib.download_instance("A-n32-k5", "actual.vrp")
        self.instance = vrplib.read_instance("actual.vrp")
        # print(self.instance)
        self.distances = self.instance['edge_weight']
        self.customers = self.instance['dimension']
        self.demands = self.instance['demand']
        self.capacity = self.instance['capacity']
        self.depot = list(self.instance['depot']).pop()
        self.tau = []

    def populate(self):

        for ant in range(self.numberOfAnts):
            route = [self.depot]
            visited = [self.depot]
            capacity = self.capacity
            demands = list(self.demands)
            demands.pop(self.depot)

            while len(visited) < self.customers:
                potentialCustomer = random.choice(list(set([x for x in range(1, self.customers)]) - set(visited)))
                demand = self.demands[potentialCustomer]

                if capacity >= demand:
                    route.append(potentialCustomer)
                    visited.append(potentialCustomer)
                    capacity = capacity - demand
                    demands.remove(demand)

                elif capacity < demand:
                    demands.sort()

                    if capacity >= demands[0]:
                        potentialCustomer = random.choice(list(set([x for x in range(1, self.customers)]) - set(visited)))
                        demand = self.demands[potentialCustomer]

                        while (capacity < demand):
                            potentialCustomer = random.choice(list(set([x for x in range(1, self.customers)]) - set(visited)))
                            demand = self.demands[potentialCustomer]
                        route.append(potentialCustomer)
                        visited.append(potentialCustomer)
                        capacity = capacity - demand
                        demands.remove(demand)

                    elif capacity < demands[0]:
                        route.append(self.depot)
                        capacity = self.capacity

            self.population.append([0,route])

        print(self.population)
    
    def calculateCosts(self):

        for ant in self.population:
            cost = 0
            route = ant[1]

            for customerIndex in range(len(route)-1):
                customer = route[customerIndex]
                nextCustomer = route[customerIndex+1]
                cost += self.distances[customer][nextCustomer]
            self.costs.append(cost)
            ant[0] = cost
            
        print(self.costs)
        print(self.population)

    def calculateTau(self):

        pass



numberOfAnts = 10

T = VehicleRoutingProblem(numberOfAnts)
T.populate()
T.calculateCosts()