import vrplib
import random
import copy


class VehicleRoutingProblem():

    def __init__(self, ants, evaporationRate, alpha, beta) -> None:
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
        self.tauTable = []
        # self.routes = []
        self.evaporationRate = evaporationRate
        self.alpha = alpha
        self.beta = beta

    def populate(self):

        for ant in range(self.numberOfAnts):
            routes = []
            visited = [self.depot]
            # visited = []
            capacity = self.capacity
            demands = copy.deepcopy(list(self.demands))
            demands.pop(self.depot)
            route = [self.depot]

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
                        routes.append(route)
                        route = [self.depot]
                        capacity = self.capacity
            
            route.append(self.depot)
            routes.append(route)

            self.population.append([0,routes])

        # print(self.population)
    
    def calculateCosts(self):

        for ant in self.population:
            cost = 0
            routes = ant[1]

            for route in routes:
                routeCost = 0
                for customerIndex in range(len(route)-1):
                    customer = route[customerIndex]
                    nextCustomer = route[customerIndex+1]
                    routeCost += self.distances[customer][nextCustomer]
                cost += routeCost
            self.costs.append(cost)
            ant[0] = cost

        # print(self.costs)
        # print(self.population)


    def initializeTauTable(self):
        self.tauTable = [[1 for i in range(self.customers)] for j in range(self.customers)]
        # print(self.tauTable)


    def binarySearch(self, lst, low, high, elem):
        if high >= low:
            mid = low + (high-low)//2   
            if lst[mid] == elem:
                return mid
            elif lst[mid] > elem:
                return self.binarySearch(lst, low, mid-1, elem)
            else:
                return self.binarySearch(lst, mid+1, high, elem)
        else:
            return -1

    def calculateDeltaTau(self):
        deltaTau = [[0 for i in range(self.customers)] for j in range(self.customers)]
        for ant in self.population:
            for route in ant[1]:
                for customerIndex in range(0, len(route)-1):
                    deltaTau[route[customerIndex]][route[customerIndex+1]] += 1/ant[0]
        # print("DELTA TAU:")
        # print(deltaTau)
        return deltaTau

    def updateTauTable(self):

        deltaTau = self.calculateDeltaTau()
        for customer1 in range (self.customers):
            for customer2 in range (customer1, self.customers):
                previousValue = self.tauTable[customer1][customer2]
                newValue = (1-self.evaporationRate)*previousValue + deltaTau[customer1][customer2] + deltaTau[customer2][customer1]
                self.tauTable[customer1][customer2] = newValue
                self.tauTable[customer2][customer1] = newValue
        
        # print(self.tauTable)

    def calculateEta(self):

        self.EtaTable = [[0 for i in range(self.customers)] for j in range(self.customers)]
        for customer1 in range(self.customers):
            for customer2 in range(self.customers):
                if customer1 == customer2:
                    self.EtaTable[customer1][customer2] = 0
                else:
                    value = self.distances[customer1][customer2]
                    self.EtaTable[customer1][customer2] = 1/value

        # print(self.EtaTable)

    def calculateTransitionProbabilities(self, currentCustomer, visited, greaterDemand):
        probabilities = []
        normalisedProbabilities = []
        ranges = {}
        for customer in range(self.customers):
            if customer != currentCustomer and customer not in visited and customer not in greaterDemand:
                probability = ((self.tauTable[currentCustomer][customer])**self.alpha) * ((self.EtaTable[currentCustomer][customer])**self.beta)
                probabilities.append(probability)
            else:
                probabilities.append(0)
        for p in probabilities:
            if (sum(probabilities) == 0):
                normalisedProbabilities.append(0)
            else:
                normalisedProbabilities.append(p/sum(probabilities))

        pointer = 0
        for i in range(len(normalisedProbabilities)):
            if normalisedProbabilities[i] != 0:
                limits = [pointer, pointer+normalisedProbabilities[i]]
                ranges[i] = limits
                pointer += normalisedProbabilities[i]
        
        return ranges
            

    def getNextCustomer(self, currentCustomer, visited, capacity):
        # use transition probabilities and update them after every next customer is selected
        greaterDemand = []
        ranges = self.calculateTransitionProbabilities(currentCustomer, visited, greaterDemand)

        # FIRST APPROACH
        
        demands = []
        for key, value in ranges.items():
            demands.append(self.demands[key])
        
        demands.sort()

        if capacity >= demands[0]:
            demand = 10000000000000
            while demand > capacity:
                randomIndex = random.uniform(0,1)
                for key, value in ranges.items():
                    if randomIndex >= value[0] and randomIndex <= value[1]:
                        demand = self.demands[key]
                        break
            selectedCustomer = key

        elif capacity < demands[0]:
            selectedCustomer = self.depot

        return selectedCustomer

        # SECOND APPROACH

        # while (len(ranges) > 0):
        #     randomIndex = random.uniform(0,1)
        #     for key, value in ranges.items():
        #         if randomIndex >= value[0] and randomIndex <= value[1]:
        #             demand = self.demands[key]
        #             if demand <= capacity:
        #                 return key
        #             else:
        #                 greaterDemand.append(key)
        #                 ranges = self.calculateTransitionProbabilities(currentCustomer, visited, greaterDemand)
        # return self.depot


    def getNewRoute(self):
        routes = []
        visited = [self.depot]
        capacity = self.capacity

        route = [self.depot]
        while (len(visited) < self.customers):
            nextCustomer = self.getNextCustomer(route[-1], visited, capacity)
            if nextCustomer != self.depot:
                route.append(nextCustomer)
                visited.append(nextCustomer)
                demand = self.demands[nextCustomer]
                capacity = capacity - demand
            elif nextCustomer == 0:
                route.append(nextCustomer)
                routes.append(route)
                route = [self.depot]
                capacity = self.capacity
        
        route.append(self.depot)
        routes.append(route)

        return [0, routes]



def ACO(iterations, numberOfAnts, evaporationRate, alpha, beta):

    T = VehicleRoutingProblem(numberOfAnts, evaporationRate, alpha, beta)
    T.populate()
    T.calculateCosts()
    T.initializeTauTable()
    T.updateTauTable()
    T.calculateEta()
    # print(T.population)    

    for iteration in range(iterations):
        print("***** Iteration: " + str(iteration+1) + " *****")

        for i in range(numberOfAnts):
            newRoute = T.getNewRoute()
            T.population[i] = newRoute

        T.calculateCosts()
        T.updateTauTable()

        T.population.sort()
        print(T.population[0])


iterations = 10
numberOfAnts = 10
evaporationRate = 0.02
alpha = 2
beta = 2

ACO(iterations, numberOfAnts, evaporationRate, alpha, beta)

# T = VehicleRoutingProblem(numberOfAnts, evaporationRate, alpha, beta)
# T.populate()
# T.calculateCosts()
# T.initializeTauTable()
# T.updateTauTable()
# T.calculateEta()
# T.getNextCustomer(0, [3,4,5], 100)