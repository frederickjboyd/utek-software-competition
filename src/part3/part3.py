from __future__ import print_function
import matplotlib.pyplot as plt
 
class AStarGraph(object):
	#Define a class board like grid with two barriers
 
	def __init__(self):
		self.barriers = []
		# self.barriers.append([(2,4),(2,5),(2,6),(3,6),(4,6),(5,6),(5,5),(5,4),(5,3),(5,2),(4,2),(3,2)])

	def set_barriers(self, lst):
		self.barriers.append(lst)
 
	def heuristic(self, start, goal):
		#Use Chebyshev distance heuristic if we can move one square either
		#adjacent or diagonal
		D = 1
		D2 = 1
		dx = abs(start[0] - goal[0])
		dy = abs(start[1] - goal[1])
		return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
 
	def get_vertex_neighbours(self, pos):
		n = []
		#Moves allow link a chess king
		for dx, dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]:
			x2 = pos[0] + dx
			y2 = pos[1] + dy
			if x2 < 0 or x2 > 99 or y2 < 0 or y2 > 99:
				continue
			n.append((x2, y2))
		return n
 
	def move_cost(self, a, b):
		for barrier in self.barriers:
			if b in barrier:
				return 10000 #Extremely high cost to enter barrier squares
		return 1 #Normal movement cost
 
def AStarSearch(start, end, graph):
 
	G = {} #Actual movement cost to each position from the start position
	F = {} #Estimated movement cost of start to end going via this position
 
	#Initialize starting values
	G[start] = 0 
	F[start] = graph.heuristic(start, end)
 
	closedVertices = set()
	openVertices = set([start])
	cameFrom = {}
 
	while len(openVertices) > 0:
		#Get the vertex in the open list with the lowest F score
		current = None
		currentFscore = None
		for pos in openVertices:
			if current is None or F[pos] < currentFscore:
				currentFscore = F[pos]
				current = pos
 
		#Check if we have reached the goal
		if current == end:
			#Retrace our route backward
			path = [current]
			while current in cameFrom:
				current = cameFrom[current]
				path.append(current)
			path.reverse()
			return path, F[end] #Done!
 
		#Mark the current vertex as closed
		openVertices.remove(current)
		closedVertices.add(current)
 
		#Update scores for vertices near the current position
		for neighbour in graph.get_vertex_neighbours(current):
			if neighbour in closedVertices: 
				continue #We have already processed this node exhaustively
			candidateG = G[current] + graph.move_cost(current, neighbour)
 
			if neighbour not in openVertices:
				openVertices.add(neighbour) #Discovered a new vertex
			elif candidateG >= G[neighbour]:
				continue #This G score is worse than previously found
 
			#Adopt this G score
			cameFrom[neighbour] = current
			G[neighbour] = candidateG
			H = graph.heuristic(neighbour, end)
			F[neighbour] = G[neighbour] + H
 
	raise RuntimeError("A* failed to find a solution")

def parse_input(lines):
    '''
    parses a header row: n_robots, n_items, n_obstacles
    items (x, y, product id, weight (in kg))
    followed by obstacles (x1, y1, x2, y2)
    '''
    header = next(lines)
    n_robots, n_items, n_obstacles = map(int, header.split(','))
    parsed_lines = [line.strip().strip('()').split(',') for line in lines]
    items = [(int(x), int(y), int(product_number), float(weight)) for x, y, product_number, weight in parsed_lines[:n_items]]
    obstacles = [[int(coord) for coord in line] for line in parsed_lines[n_items:]]

    return n_robots, items, obstacles
 
def findpath(init_x, init_y, final_x, final_y, graph):
	result, cost = AStarSearch((init_x, init_y), (final_x,final_y), graph)	
	#plt.plot([v[0] for v in result], [v[1] for v in result])
	#for barrier in graph.barriers:
	#	plt.plot([v[0] for v in barrier], [v[1] for v in barrier])
	#plt.xlim(-1,20)
	#plt.ylim(-1,20)
	#plt.show()
	return result, cost

def gen_points_in_rect(lx, ly, rx, ry):
    out = []
    for i in range (lx, rx+1):
        for j in range (ly, ry+1):
            out.append((i,j))
    return out

def convertCoordinateToIndex(x, y):
    return (y * 100) + x

def encode(items):
    out = []
    for i in range(10000):
        out.append([0,-1,0,False])
    for i in items:
    	idx = convertCoordinateToIndex(i[0], i[1])
    	out[idx][0] += 1
        out[idx][1] = i[2]
        out[idx][2] = i[3]
        out[idx][3] = False
    return out

def main(filename):
	moves = ''
	with open(filename) as data:
		n_robots, items, obstacles = parse_input(data)
	accum = []
	for i in obstacles:
		accum.append(gen_points_in_rect(i[0], i[1], i[2], i[3]))
	graph = AStarGraph()
	graph.set_barriers(accum[0])
	board = encode(items)
	print(items)
	for i in items:
		result, cost = findpath(0,0,i[0], i[1], graph)
		print(result)
		for j in result:
			moves += 'move' + ' '+ str(j[0]) + ' ' + str(j[1]) + '\n'
		moves += 'pick' + ' ' + str(i[2]) + '\n'
		result, cost = findpath(i[0], i[1], 0, 0, graph)
		for j in result:
			moves += 'move' + ' '+ str(j[0]) + ' ' + str(j[1]) + '\n'
		moves += 'drop' + ' ' + str(i[2]) + '\n'		
	#print(moves)
	f = open('3c.out', 'w')
	f.write(moves)
	
main('3c.in')
