class Vertex:
    def __init__(self, name):
        self.name = name
        self.edges = {}
        self.weight = 0

    # Este metodo funciona porque los edges provistos por el problema son simetricos,
    def add_edge(self, other: "Vertex"):
        self.edges[other.name] = other

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self)


class Bucket:
    def __init__(self, first_item: Vertex):
        self.items = [first_item]
        self.weight = first_item.weight

    def add_item(self, new_item: Vertex):
        if any(new_item in x.edges for x in self.items):
            return False
        self.items.append(new_item)
        if new_item.weight > self.weight:
            self.weight = new_item.weight
        return True

    def can_add(self, new_item: Vertex):
        if any(new_item.name in x.edges for x in self.items):
            return False
        return True

    def __str__(self):
        return str(self.items) + ", weight:" + str(self.weight)

    def __repr__(self):
        return str(self)

    def __contains__(self, key):
        return key in self.items


file = open("segundo_problema.txt", "r+")
graph = {}
for line in file:
    if line[0] == 'c':
        continue
    if line[0] == 'p':
        n = int(line.split(' ')[2])
        for i in range(n):
            graph[i + 1] = Vertex(i + 1)
    if line[0] == 'n':
        graph[int(line.split(' ')[1])].weight = int(line.split(' ')[2])
    if line[0] == 'e':
        graph[int(line.split(' ')[1])].add_edge(graph[int(line.split(' ')[2])])
        graph[int(line.split(' ')[2])].add_edge(graph[int(line.split(' ')[1])])

completes = []
for i in graph:
    for j in graph[i].edges:
        new_complete = [graph[i], graph[j]]
        for l in graph[j].edges:
            if all(l in graph[x.name].edges for x in new_complete):
                new_complete.append(graph[l])
        new_complete.sort(key=lambda x: x.name)
        if all(new_complete != old_complete for old_complete in completes):
            completes.append(new_complete)

for complete in completes:
    complete.sort(key=lambda x: x.weight, reverse=True)
completes.sort(key=len, reverse=True)

solutions = []
completes_longest = []
i = 0
current_solution_size = len(completes[i])
best_solution_size = current_solution_size
while i < len(completes):
    completes_longest.append([item for item in completes[i]])
    solutions.append([Bucket(item) for item in completes[i]])
    i += 1
    
for complete in completes_longest:
    complete.sort(key=lambda x: x.weight, reverse=True)
    complete.sort(key=lambda x: len(x.edges), reverse=True)
completes_longest.sort(key=lambda x: sum([y.weight for y in x]), reverse=True)
completes_longest.sort(key=lambda x: sum([len(y.edges) for y in x]), reverse=True)
completes_add = []
for complete in completes_longest:
    completes_add.extend(complete)
already_added = {}
add_list = []
for vertex in completes_add:
    if vertex not in already_added:
        already_added[vertex] = True
        add_list.append(vertex)


def add_to_solution(sol: list, new_item: Vertex):
    center = 0
    while center < len(sol) and sol[center].weight >= new_item.weight:
        center += 1
    index = center - 1
    while index > -1 and not sol[index].can_add(new_item):
        index -= 1
    if index == -1:
        index = center
        while index < len(sol) and not sol[index].can_add(new_item):
            index += 1
    if index >= len(sol) or not sol[index].add_item(new_item):
        sol.append(Bucket(new_item))


def calculate_solution(sol):
    total = 0
    for buc in sol:
        total += buc.weight
    return total


for solution in solutions:
    for x in add_list:
        if all(x not in buc for buc in solution):
            add_to_solution(solution, x)
            solution.sort(key=lambda x: len(x.items), reverse=True)
            solution.sort(key=lambda x: x.weight, reverse=True)

elements_to_add = [x for k, x in graph.items()]
elements_to_add.sort(key=lambda x: x.weight, reverse=True)
elements_to_add.sort(key=lambda x: len(x.edges), reverse=True)
for solution in solutions:
    for x in elements_to_add:
        if all(x not in buc for buc in solution):
            add_to_solution(solution, x)
            solution.sort(key=lambda x: len(x.items), reverse=True)
            solution.sort(key=lambda x: x.weight, reverse=True)

best_solution = solutions[0]
best_solution_weight = calculate_solution(best_solution)
for solution in solutions:
    if calculate_solution(solution) < best_solution_weight:
        best_solution = solution
        best_solution_weight = calculate_solution(best_solution)

primer_entrega = open("segunda_entrega.txt", "w+")
lavado = 1
for bucket in best_solution:
    for prenda in bucket.items:
        primer_entrega.write(f"{prenda.name} {lavado}\n")
    lavado += 1

print(calculate_solution(best_solution))
