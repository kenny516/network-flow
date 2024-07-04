class Edge:
    def __init__(self, name: str):
        self.name = name
        self.neighbors = {}  # Use a dictionary to store neighbors and their capacities

    def add_neighbor(self, neighbor: "Edge", capacity: int) -> "Edge":
        if neighbor in self.neighbors:
            raise ValueError(
                f"Ajout de voisin impossible car les noeuds \"{self.name}\" et "
                f"\"{neighbor.name}\" le sont déjà"
            )

        self.neighbors[neighbor] = capacity
        neighbor.neighbors[self] = 0  # Reverse edge with 0 initial capacity

        return self

    def __str__(self):
        return f"{self.name}: {', '.join([f'{neighbor.name}({cap})' for neighbor, cap in self.neighbors.items()])}"


class Graph:
    def __init__(self, source: Edge, sink: Edge, edges: list[Edge]):
        self.source = source
        self.sink = sink
        self.edges = edges

    def bfs(self, parent: dict) -> bool:
        visited = {edge: False for edge in self.edges}
        queue = [self.source]
        visited[self.source] = True

        while queue:
            u = queue.pop(0)

            for v, capacity in u.neighbors.items():
                if not visited[v] and capacity > 0:
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u  # Record the parent of v
                    if v == self.sink:
                        return True
        return False

    def ford_fulkerson(self) -> int:
        parent = {}  # This dictionary will store the parent of each node in the path
        max_flow = 0
        step = 0  # To count the steps

        while self.bfs(parent):  # While there is a path from source to sink
            path_flow = float("Inf")
            s = self.sink

            while s != self.source:  # Traverse the path in reverse to find the minimum capacity
                path_flow = min(path_flow, parent[s].neighbors[s])
                s = parent[s]

            max_flow += path_flow  # Add path flow to overall flow

            # Logging the path found
            v = self.sink
            path = []
            while v != self.source:
                path.append(v.name)
                v = parent[v]
            path.append(self.source.name)
            path.reverse()
            print(f"Étape {step}: Chemin trouvé :  {' -> '.join(path)} avec flot = {path_flow}")

            # Update capacities of the edges and reverse edges
            v = self.sink
            while v != self.source:
                u = parent[v]
                u.neighbors[v] -= path_flow
                v.neighbors[u] += path_flow
                v = parent[v]

            # Print the graph state after each augmentation
            print("\nÉtat de la graphe après l'étape", step)
            for edge in self.edges:
                print(edge)

            print("\n" + "=" * 50 + "\n")
            step += 1

        return max_flow


if __name__ == '__main__':
    source = Edge("s")
    sink = Edge("t")
    e_1 = Edge("1")
    e_2 = Edge("2")
    e_3 = Edge("3")
    e_4 = Edge("4")
    e_5 = Edge("5")
    e_6 = Edge("6")

    source.add_neighbor(e_1, 7).add_neighbor(e_3, 4).add_neighbor(e_4, 3)
    e_1.add_neighbor(e_2, 7)
    e_2.add_neighbor(e_5, 8).add_neighbor(e_3, 3)
    e_3.add_neighbor(e_1, 3).add_neighbor(e_4, 1).add_neighbor(e_6, 2).add_neighbor(e_5, 1)
    e_4.add_neighbor(e_6, 3)
    e_5.add_neighbor(sink, 12)
    e_6.add_neighbor(e_5, 4).add_neighbor(sink, 5)

    edges = [source, sink, e_1, e_2, e_3, e_4, e_5, e_6]

    graph = Graph(source, sink, edges)
    max_flow = graph.ford_fulkerson()
    print(f"Le flot maximal est: {max_flow}")
