from settings import *
import pygame
import pytmx
import math
import heapq

def load_navmesh(filename):
    tmx_data = pytmx.TiledMap(filename)
    nodes = {}  # {id: (x, y)}
    edges = []  # [(node1, node2, cost)]
    node_counter = 1  # Generate node IDs dynamically


    map_width = tmx_data.width * tmx_data.tilewidth
    map_height = tmx_data.height * tmx_data.tileheight
    screen_width, screen_height = resolution
    scale_factor = min(screen_width / map_width, screen_height / map_height)

    for obj in tmx_data.objects:
        if obj.name == "navedge":  # Extract polylines
            points = obj.points  # List of (x, y) points

            if len(points) >= 2:
                prev_node = None
                for point in points:
                    # Apply scale factor to (x, y) coordinates
                    scaled_point = (round(point[0] * scale_factor), round(point[1] * scale_factor))

                    existing_node = None
                    for n, pos in nodes.items():
                        if pos == scaled_point:
                            existing_node = n
                            break

                    if existing_node:
                        node_id = existing_node
                    else:
                        node_id = node_counter
                        nodes[node_id] = scaled_point
                        node_counter += 1

                    # Connect nodes sequentially along the polyline
                    if prev_node is not None:
                        cost = math.dist(nodes[prev_node], nodes[node_id])  # Euclidean distance
                        edges.append((prev_node, node_id, cost))

                    prev_node = node_id  # Update last node for next connection

    # Auto-connect nodes if they are close but not connected
    THRESHOLD = 100  # Adjust based on map scale

    for node1 in nodes:
        for node2 in nodes:
            if node1 != node2:
                dist = math.dist(nodes[node1], nodes[node2])
                if dist < THRESHOLD and (node1, node2, dist) not in edges and (node2, node1, dist) not in edges:
                    edges.append((node1, node2, dist))
                    # print(f"🔗 Auto-Connected {node1} <-> {node2} (Dist: {dist})")


    # After loading nodes and edges:
    # for node in nodes:
    #     if node not in [edge[0] for edge in edges] and node not in [edge[1] for edge in edges]:
    #         print(f"⚠️ Warning: Node {node} at {nodes[node]} has NO connections!")
   
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
            # print(f"Edge Added: {node1} <-> {node2} (Cost: {cost})")  # Debugging

        # print("Nodes:", nodes)
        # print("Edges:", edges)
        # for node, neighbors in graph.edges.items():
        #     print(f"Node {node} connects to {neighbors}")

            

    def heuristic(self, node1, node2):
        """Calculates Euclidean distance between two nodes."""
        x1, y1 = self.nodes[node1]
        x2, y2 = self.nodes[node2]
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5  

    def astar(self, start, goal):
        """A* pathfinding algorithm"""
        
        path = []
        open_set = []
        heapq.heappush(open_set, (0, start))  

        came_from = {}  
        g_score = {node: float('inf') for node in self.nodes}  
        f_score = {node: float('inf') for node in self.nodes}  

        g_score[start] = 0  
        f_score[start] = self.heuristic(start, goal)  

        while len(open_set) > 0:  
            _, current = heapq.heappop(open_set)  

            if current == goal:  
                path = []
                while current in came_from:  
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]  

            for neighbor, cost in self.edges[current]:
                new_g_score = g_score[current] + cost  
                if new_g_score < g_score[neighbor]:  
                    came_from[neighbor] = current  
                    g_score[neighbor] = new_g_score
                    f_score[neighbor] = new_g_score + self.heuristic(neighbor, goal)  

                    if (f_score[neighbor], neighbor) not in open_set:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

        print(path)
        return None  # No path found


    def draw(self, screen):
        """Visualize the graph using pygame"""
        for node, position in self.nodes.items():
            pygame.draw.circle(screen, RED, position, 5)
        for node, neighbors in self.edges.items():
            for neighbor, _ in neighbors:
                pygame.draw.line(screen, BLACK, self.nodes[node], self.nodes[neighbor], 2)

# # Load navigation mesh from Tiled
# nodes, edges = load_navmesh("./maps/world.tmx")

# # Create graph for pathfinding
# graph = Graph(nodes, edges)

# # Pick two random nodes as start and goal
# start_node = list(nodes.keys())[0]  # First node
# goal_node = list(nodes.keys())[-1]  # Last node

# # Find a path
# path = graph.astar(start=start_node, goal=goal_node)
# print("Path:", path)  # Example: [1, 3, 5, 8]

# # Visualize using pygame
# pygame.init()
# screen = pygame.display.set_mode((1920, 1080))
# clock = pygame.time.Clock()

# running = True
# while running:
#     screen.fill((0, 0, 0))  # Clear screen
#     graph.draw_graph(screen)  # Draw graph
    
#     if path:
#         for i in range(len(path) - 1):
#             pygame.draw.line(screen, (255, 0, 0), nodes[path[i]], nodes[path[i+1]], 3)
    
#     pygame.display.flip()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#     clock.tick(60)

# pygame.quit()
