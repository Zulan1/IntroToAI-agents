# import re
# from game_classes import Game, Package
# FILE_NAME = 'init_file.txt' #enter file name

# def create_game_object(description, game):
#     first = description[0]
#     match first :
#         case 'X':
#             x = int(description[1])    
#             game.set_rows(x)        
#             print(f'Length is {x}')                    
#         case 'Y':
#             y = int(description[1])
#             game.set_cols(y)
#             print(f'Width is {y}')            
#         case 'P':
#             pickup_loc = (int(description[1]) , int(description[2]))
#             pickup_time = int(description[3])
#             dropoff_loc = (int(description[5]) , int(description[6]))
#             dropoff_time = int(description[7])        
#             print(f'Pacakge is at {pickup_loc} on {pickup_time} sec and dropoff is at {dropoff_loc} on {dropoff_time} sec')
#         case 'B':
#             start_point = (int(description[1]) , int(description[2]))
#             end_point = (int(description[3]) , int(description[4]))
#             edge = (start_point, end_point)
#             game.set_edge_color(edge, 'red')
#             print(f'Block road from {start_point} to {end_point}')     
#         case _:
#             print("somthing went wrong\n")
            
            
# def init_game(filename):
#     x, y = 0, []
#     mygame = Game()
#     with open(filename, 'r') as f:
#         for line in f:
#             if line == '\n':
#                 continue
#             x = list(filter(None, re.split('#| ', line)))
#             if x == []:
#                 continue
#             temp = int(x.index(';')) if ';' in x else -1 #if x.index(';') == -1 else x.index('\n')
#             y.append([w for w, i in zip(x, range(len(x))) if i < temp])
#             create_game_object(y[-1], mygame)
#             print(mygame.get_edges(), mygame.get_edges_colors(), "\n\n")
           
#     return mygame

# if __name__ == "__main__":
#     print(init_game(FILE_NAME))    