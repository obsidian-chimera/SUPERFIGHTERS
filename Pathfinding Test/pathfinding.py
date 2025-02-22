import pygame
import pytmx
import math
import heapq

def load_navmesh(filename):
    tmx_data = pytmx.TiledMap(filename)
    nodes = {}  # {id: (x, y)}
    edges = []  # [(node1, node2, cost)]
    node_counter = 1  # Generate node IDs dynamically

    for obj in tmx_data.objects:
        if obj.name == "navedge":  # Extract polylines
            points = obj.polyline  # List of (x, y) points
            
            if len(points) >= 2:
                prev_node = None
                for point in points:
                    existing_node = None
                    for n, pos in nodes.items():
                        if pos == point:
                            existing_node = n
                            break
                    
                    if existing_node:
                        node_id = existing_node
                    else:
                        node_id = node_counter
                        nodes[node_id] = point
                        node_counter += 1
                    
                    # Connect nodes sequentially along the polyline
                    if prev_node is not None:
                        cost = math.dist(nodes[prev_node], nodes[node_id])  # Euclidean distance
                        edges.append((prev_node, node_id, cost))
                    
                    prev_node = node_id  # Update last node for next connection
    print(nodes)
    print(edges)
    return nodes, edges

class Graph:
    def __init__(self, nodes, edges):
        self.nodes = nodes  # {id: (x, y)}
        self.edges = {}
        for node in nodes:
            self.edges[node] = []
            print(self.edges)
        
        for node1, node2, cost in edges:
            self.edges[node1].append((node2, cost))
            self.edges[node2].append((node1, cost))  # Bidirectional movement

    def heuristic(self, node1, node2):
        """Heuristic function: Euclidean distance"""
        x1, y1 = self.nodes[node1]
        x2, y2 = self.nodes[node2]
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def astar(self, start, goal):
        """A* Algorithm"""
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {}
        f_score = {}
        for node in self.nodes:
            g_score[node] = float('inf')
            f_score[node] = float('inf')
        g_score[start] = 0
        f_score[start] = self.heuristic(start, goal)

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]  # Reverse path

            for neighbor, cost in self.edges[current]:
                tentative_g_score = g_score[current] + cost
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None  # No path found

    def draw_graph(self, screen):
        """Visualize the graph using pygame"""
        for node, position in self.nodes.items():
            pygame.draw.circle(screen, (0, 255, 0), position, 5)
        for node, neighbors in self.edges.items():
            for neighbor, _ in neighbors:
                pygame.draw.line(screen, (255, 255, 255), self.nodes[node], self.nodes[neighbor], 2)

# Load navigation mesh from Tiled
nodes, edges = load_navmesh("./maps/world.tmx")

# Create graph for pathfinding
graph = Graph(nodes, edges)

# Pick two random nodes as start and goal
start_node = list(nodes.keys())[0]  # First node
goal_node = list(nodes.keys())[-1]  # Last node

# Find a path
path = graph.astar(start=start_node, goal=goal_node)
print("Path:", path)  # Example: [1, 3, 5, 8]

# Visualize using pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

running = True
while running:
    screen.fill((0, 0, 0))  # Clear screen
    graph.draw_graph(screen)  # Draw graph
    
    if path:
        for i in range(len(path) - 1):
            pygame.draw.line(screen, (255, 0, 0), nodes[path[i]], nodes[path[i+1]], 3)
    
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    clock.tick(60)

pygame.quit()