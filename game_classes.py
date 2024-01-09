# import networkx as nx
# import matplotlib as plt
# edge_colors = {0: 'green', 1: 'gray', 2: 'red'}
# class Package:
#     def __init__(self, pickup_loc, dropoff_loc, pickup_time, dropoff_maxtime):
#         self.pickup_loc = pickup_loc
#         self.dropoff_loc = dropoff_loc
#         self.pickup_time = pickup_time
#         self.dropoff_maxtime = dropoff_maxtime
#         self.status = "not picked up"

#     def get_pickup_loc(self):
#         return self.pickup_loc

#     def get_dropoff_loc(self):
#         return self.dropoff_loc

#     def get_pickup_time(self):
#         return self.pickup_time

#     def get_dropoff_maxtime(self):
#         return self.dropoff_maxtime

#     def get_status(self):
#         return self.status

#     def pickup(self):
#         if self.status == "not picked up":
#             self.status = "picked up"
#             print("Package has been picked up.")
#         else:
#             print("Package is already picked up.")

#     def dropoff(self):
#         if self.status == "picked up":
#             self.status = "dropped off"
#             print("Package has been dropped off.")
#         elif self.status == "not picked up":
#             print("Cannot drop off. Package has not been picked up yet.")
#         else:
#             print("Package has already been dropped off.")
            
# class Game:
    
#     def __init__(self):
#         self.size = (0,0)
#         self.nodes = [(i,j) for i in range(self.size[0]) for j in range(self.size[1])]
#         self.edges = [((i, j), (i, j + 1)) for i in range(self.size[0]) for j in range(self.size[1] - 1)]
#         self.edges += [((i, j), (i + 1, j)) for i in range(self.size[0] - 1) for j in range(self.size[1])]
#         self.nodes_colors = ["gray" for _ in range(len(self.nodes))]
#         self.edges_colors = ["green" for _ in range(len(self.edges))]
#         self.graph = nx.Graph()
#         self.packages = []        
        
#     def update_board(self):
#         if self.size[0] != 0 and self.size[1] != 0:
#             self.nodes = [(i,j) for i in range(self.size[0]) for j in range(self.size[1])]
#             self.edges = [((i, j), (i, j + 1)) for i in range(self.size[0]) for j in range(self.size[1])]
#             self.edges += [((i, j), (i + 1, j)) for i in range(self.size[0]) for j in range(self.size[1])]
#             self.nodes_colors = ["gray" for _ in range(len(self.nodes))]
#             self.edges_colors = ["green" for _ in range(len(self.edges))]
#     def color_packages(self):
#         for p in self.packages:
#             match p.get_status():
#                 case "not picked up":
#                     pass
#                 case "picked up":
#                     pass
#                 case "dropped off":
#                     pass                
#                 case _:
#                     print("Somthing went wrong")
#     #Get Methods  
#     def get_size(self):
#         return self.size

#     def get_nodes(self):
#         return self.nodes

#     def get_edges(self):
#         return self.edges
    
#     def get_nodes_colors(self):
#         return self.nodes_colors
    
#     def get_edges_colors(self):
#         return self.edges_colors
    
#     def get_package(self, package):
#         return self.packages

#     #Set Methods
#     def set_rows(self, rows):
#         self.size = (rows, self.size[1])
#         if self.size[1] != 0:
#             self.update_board()
    
#     def set_cols(self, cols):
#         self.size = (self.size[0], cols)
#         if self.size[0] != 0:
#             self.update_board()
    
#     def set_size(self, rows, cols):
#         self.size = (rows, cols)
#         self.update_board()

#     def set_node_color(self, node, color):
#         if 0 <= node < len(self.nodes_colors):
#             self.nodes_colors[node] = color

#     def set_edge_color(self, edge, color):
#         if edge in self.edges:
#             index = self.edges.index(edge)
#             self.edges_colors[index] = color
#         else:
#             print("Edge does not exist")
            
#     def set_edge_color_code(self, edge, color_code):
#         if edge in self.edges:
#             index = self.edges.index(edge)
#             self.edges_colors[index] = edge_colors[color_code]
#         else:
#             print("Edge does not exist")
#     def add_package(self, package):
#         self.packages.append(package)
#         color_packages(self)
        
    
       
#     #doesnt work   
#     def draw(self):
#         pos = {node: (node[1], -node[0]) for node in self.nodes}

#         # Draw nodes
#         nx.draw_networkx_nodes(self.graph, pos, node_color=self.nodes_colors, node_size=700)

#         # Draw edges
#         nx.draw_networkx_edges(self.graph, pos, edgelist=self.edges, edge_color=self.edges_colors)

#         # Draw labels (optional)
#         labels = {node: str(node) for node in self.nodes}
#         nx.draw_networkx_labels(self.graph, pos, labels)

#         # Display the plot
#         plt.show()     
        
        
        
        
        