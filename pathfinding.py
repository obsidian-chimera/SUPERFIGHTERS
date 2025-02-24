from settings import *
import pygame
import pytmx
import math
import heapq

def load_navmesh(file_name):
    # Loads the navigation mesh from a Tiled map.
    map_data = pytmx.TiledMap(file_name)
    points_map = {}  # Stores each node's position {id: (x, y)}
    links = []  # Stores connections between nodes [(node1, node2, cost)]
    node_count = 1  # Auto-increment node ID

    # Get map dimensions and scale it to fit screen
    map_width = map_data.width * map_data.tilewidth
    map_height = map_data.height * map_data.tileheight
    screen_width, screen_height = resolution
    scale = min(screen_width / map_width, screen_height / map_height)

    # Go through objects in the map and find navigation edges
    for obj in map_data.objects:
        if obj.name == "navedge":  # Looking for navigation paths
            path_points = obj.points  # List of (x, y) points
            
            if len(path_points) >= 2:
                last_point = None
                for point in path_points:
                    # Scale the coordinates
                    adjusted_point = (round(point[0] * scale), round(point[1] * scale))

                    existing_point = None
                    for node, pos in points_map.items():
                        if pos == adjusted_point:
                            existing_point = node
                            break
                    
                    if existing_point:
                        current_node = existing_point
                    else:
                        current_node = node_count
                        points_map[current_node] = adjusted_point
                        node_count += 1

                    # Connect nodes along the polyline
                    if last_point is not None:
                        cost = math.dist(points_map[last_point], points_map[current_node])
                        links.append((last_point, current_node, cost))
                    
                    last_point = current_node  # Move to the next point

    # Auto-connect close nodes that aren’t linked
    link_threshold = 100000  # Distance at which nodes should connect
    for node_a in points_map:
        for node_b in points_map:
            if node_a != node_b:
                distance = math.dist(points_map[node_a], points_map[node_b])
                if distance < link_threshold and (node_a, node_b, distance) not in links and (node_b, node_a, distance) not in links:
                    links.append((node_a, node_b, distance))

    return points_map, links

class Graph:
    def __init__(self, points, links):
        self.points = points  # {id: (x, y)}
        self.connections = {node: [] for node in points}  # {id: [(other_node, cost)]}
        
        for node_a, node_b, cost in links:
            self.connections[node_a].append((node_b, cost))
            self.connections[node_b].append((node_a, cost))  # Bi-directional movement

    def heuristic(self, node_a, node_b):
        # Estimates the distance between two nodes (Euclidean distance).
        x1, y1 = self.points[node_a]
        x2, y2 = self.points[node_b]
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5  

    def astar(self, start, end):
        # A* pathfinding algorithm to find the shortest path.
        path = []
        working_set = []
        heapq.heappush(working_set, (0, start))  # Start node with priority 0
        
        origin = {}  # Stores the best previous node in the path
        travel_cost = {}
        total_cost = {}

        # Initialize all nodes with infinite cost
        for node in self.points:
            travel_cost[node] = float('inf')  # Cost to reach each node
            total_cost[node] = float('inf')  # Estimated cost to goal

        # Start node has no travel cost, estimate total cost
        travel_cost[start] = 0
        total_cost[start] = self.heuristic(start, end)

        while len(working_set) > 0:  # Keep searching while there's something to check
            _, current = heapq.heappop(working_set)  # Get the node with lowest total cost

            if current == end:  # If we reached the goal, reconstruct the path
                while current in origin:
                    path.append(current)
                    current = origin[current]
                path.append(start)
                return path[::-1]  # Reverse the path to get the correct order

            for neighbor, cost in self.connections[current]:
                new_cost = travel_cost[current] + cost  # Cost to move to neighbor
                if new_cost < travel_cost[neighbor]:  # If it's a better route
                    origin[neighbor] = current  # Remember where we came from
                    travel_cost[neighbor] = new_cost
                    total_cost[neighbor] = new_cost + self.heuristic(neighbor, end)

                    if (total_cost[neighbor], neighbor) not in working_set:
                        heapq.heappush(working_set, (total_cost[neighbor], neighbor))

        return None  # No path found

    def draw(self, screen):
        # Draws the navigation graph using pygame.
        for node, position in self.points.items():
            pygame.draw.circle(screen, RED, position, 5)  # Draw nodes
        for node, neighbors in self.connections.items():
            for neighbor, _ in neighbors:
                pygame.draw.line(screen, BLACK, self.points[node], self.points[neighbor], 2)  # Draw links


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
