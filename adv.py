from room import Room
from player import Player
from world import World
import random
from ast import literal_eval


# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

# traversal_path = []
# reverse_path = []
# rooms = {}
# reverse_directions = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}

# rooms[0] = player.current_room.get_exits()

# while len(rooms) < len(room_graph) - 1:
#     if player.current_room.id not in rooms:
#         rooms[player.current_room.id] = player.current_room.get_exits()
#         last_room = reverse_path[-1]
#         rooms[player.current_room.id].remove(last_room)

#     while len(rooms[player.current_room.id]) < 1:
#         reverse = reverse_path.pop()
#         traversal_path.append(reverse)
#         player.travel(reverse)

#     exit_dir = rooms[player.current_room.id].pop(0)
#     traversal_path.append(exit_dir)
#     reverse_path.append(reverse_directions[exit_dir])
#     player.travel(exit_dir)

# Fill this out with directions, traversal_path = ['n', 'n']
traversal_path = []
# Graph of traversed rooms 
traversal_graph = {}
# Path for backtracking
current_path = []
# opposite directions set with key and value for backtracking
reverse_dir = {'n': 's', 's': 'n', 'w': 'e', 'e': 'w'}


# create function to pick a direction that returns None if there aren't more directions to travel 
def get_next_dir(current_room):
    # loop through the directions in the room
    for key, val in current_room.items():
        # check for '?' value
        if val is '?':
            # return the key for the direction
            return key
    # if no '?' return None
    return None

# create while loop to traverse all unexplored rooms 
while len(traversal_graph) < len(world.rooms):
    # get the current room
    curr_room = player.current_room
    # get the id of the room pf the curent room the player is in
    curr_room_id = player.current_room.id
    # setup ref to prev room
    prev_room_id = None

    # if current room is not in the traversal graph
    if curr_room_id not in traversal_graph:
        # check for ? in all the possible directions
        traversal_graph[curr_room_id] = {direction: '?' for direction in player.current_room.get_exits()}

    # call get_next_dir() to find a new direction to travel in
    direction = get_next_dir(traversal_graph[curr_room_id])

    # direction is None, nowhere to go, create new path with 
    if direction is None:
        new_path = current_path.pop()
        player.travel(reverse_dir[new_path])
        traversal_path.append(reverse_dir[new_path])
        continue

    # set prev_room to current room before traverse
    prev_room_id = player.current_room.id
    # move to the next room
    player.travel(direction)
    # append move to traversal path
    traversal_path.append(direction)
    # append to the current_path for reverse/back tracking
    current_path.append(direction)
    # set variable curr_room to the new current_room
    curr_room = player.current_room
    # change/update the id
    curr_room_id = player.current_room.id

    # check if the new room is in the traversal graph
    if curr_room_id not in traversal_graph:
        # get the possible directions from the new room
        traversal_graph[curr_room_id] = {direction: '?' for direction in player.current_room.get_exits()}
    # connect the rooms together while there is an unchecked/? room
    while traversal_graph[curr_room_id][reverse_dir[direction]] == '?':
        # Graph connection
        traversal_graph[curr_room_id][reverse_dir[direction]] = prev_room_id
        traversal_graph[prev_room_id][direction] = curr_room_id



# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
