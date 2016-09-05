#!/usr/bin/env python
#coding:utf-8

from random import randint
from BaseAI import BaseAI
import time
import sys
import math
from Grid import Grid

#Tree node class
class TreeNode:
	def __init__(self, grid, parent, children):
		self.grid = grid
		self.children = children
		self.parent = parent

	def getValue(self):
		emptyCells = len(self.grid.getAvailableCells())
		#print emptyCells

		smoothWeight = 1
		monoWeight = 1.5
		emptyWeight = 1
		maxWeight = 1

		vertical1, horizontal1 = self.getMonotonicity1()
		vertical2, horizontal2 = self.getMonotonicity2()
		vertical3, horizontal3 = self.getMonotonicity3()
		vertical4, horizontal4 = self.getMonotonicity4()

		monoValue = max(vertical1,horizontal1,vertical2,horizontal2,vertical3,horizontal3, vertical4, horizontal4)
		smoothnessValue = self.getSmoothness() * smoothWeight
		emptyValue = math.log(emptyCells) * emptyWeight if emptyCells > 0 else 0
		maxTileValue = self.grid.getMaxTile() * maxWeight

		value = smoothnessValue + monoValue + emptyValue + maxTileValue

		# value = smoothnessValue
		# value = monoValue
		# value = emptyValue
		# value = maxTileValue

		return value

	def getSmoothness(self):
		smoothness = 0

		for i in range(4):
			for j in range(4):
				cell = {'x': i, 'y': j}
				if self.grid.map[i][j] != 0:
					value = math.log(self.grid.map[i][j], 2)
					for move in range(1, 3):
						vector = self.getVector(move)
						targetCell = self.getTargetCell(cell, vector)['next']
						if targetCell != None:
							targetValue = math.log(self.grid.map[targetCell['x']][targetCell['y']], 2) 
							smoothness -= math.fabs(value - targetValue)

		return smoothness

	def getVector(self, move):
		if(move == 1):
			return {'x': 1, 'y': 0}
		else:
			return {'x': 0, 'y': 1}

	def getTargetCell(self, cell, vector):
		previous = None

		while True:
			previous = cell.copy()
			#print 'previous:', previous
			#print 'cell:', cell
			cell['x'] = previous['x'] + vector['x']
			cell['y'] = previous['y'] + vector['y']
			if self.grid.crossBound((cell['x'], cell['y'])):
				#print 'crossbound'
				return {'target': previous, 'next': None} 
			if self.grid.getCellValue((cell['x'], cell['y'])) != 0:
				#print 'noCell'
				return {'target': previous, 'next': cell}

	def getMonotonicity1(self, initPosition = (0, 0)):
		ratio = 0.03125
		weight = 1
		vertical = 0
		horizontal = 0
		for i in range(4):
			for j in range(4):
				if i % 2 == 0:
					vertical += self.grid.getCellValue((i, j)) * weight
					weight *= ratio
				else:
					vertical += self.grid.getCellValue((i, j)) * weight
					weight *= ratio

			ratio = 0.03125
			weight = 1.0
			for j in range(4):
				for i in range(4):
					if j % 2 == 0:
						horizontal += self.grid.getCellValue((i, j)) * weight
						weight *= ratio
					else:
						horizontal += self.grid.getCellValue((i, j)) * weight
						weight *= ratio

		return vertical, horizontal

	def getMonotonicity2(self, initPosition = (3, 0)):
		ratio = 0.03125
		weight = 1
		vertical = 0
		horizontal = 0

		for i in range(4):
			for j in range(4):
				if i % 2 == 0:
					vertical += self.grid.getCellValue((3 - i, j)) * weight
					weight *= ratio
				else:
					vertical += self.grid.getCellValue((3 - i, 3 - j)) * weight
					weight *= ratio

		ratio = 0.03125
		weight = 1.0

		for j in range(4):
			for i in range(4):
				if j % 2 == 0:
					horizontal += self.grid.getCellValue((3 - i, j)) * weight
					weight *= ratio
				else:
					horizontal += self.grid.getCellValue((i, j)) * weight
					weight *= ratio

		return vertical, horizontal

	def getMonotonicity3(self, initPosition = (0, 3)):
		ratio = 0.03125
		weight = 1
		vertical = 0
		horizontal = 0

		for i in range(4):
			for j in range(4):
				if i % 2 == 0:
					vertical += self.grid.getCellValue((i, 3 - j)) * weight
					weight *= ratio
				else:
					vertical += self.grid.getCellValue((i, j)) * weight
					weight *= ratio

		ratio = 0.03125
		weight = 1.0

		for j in range(4):
			for i in range(4):
				if j % 2 == 0:
					#print x, 3-y
					horizontal += self.grid.getCellValue((i, 3 - j)) * weight
					weight *= ratio
					#print value2
				else:
					#print 3- x, 3-y
					horizontal += self.grid.getCellValue((3 - i, 3 - j)) *weight
					weight *= ratio

		return vertical, horizontal

	def getMonotonicity4(self, initPosition = (3, 3)):
		ratio = 0.03125
		weight = 1
		vertical = 0
		horizontal = 0

		for i in range(4):
			for j in range(4):
				if i % 2 == 0:
					vertical += self.grid.getCellValue((3 - i, 3 - j)) * weight
					weight *= ratio
				else:
					vertical += self.grid.getCellValue((3 - i, j)) * weight
					weight *= ratio

		ratio = 0.03125
		weight = 1.0

		for j in range(4):
			for i in range(4):
				if j % 2 == 0:
					horizontal += self.grid.getCellValue((3 - i, 3 - j)) * weight
					weight *= ratio
				else:
					horizontal += self.grid.getCellValue((i, 3 - j)) * weight
					weight *= ratio

		return vertical, horizontal

class PlayerAI(BaseAI):
	def getMove(self, grid):
		# I'm too naive, please change me!

		timeout = time.time() + 1
		root = TreeNode(grid, None, [])
		depthLimit = 1
		result = {'move': None, 'value': None}
		alpha = -sys.maxint
		beta = sys.maxint
		# while depthLimit < sys.maxint and time.time() < timeout:
		# 	# print 'timeout is:', timeout
		# 	# print 'time is', time.time()
		# 	#print 'depthLimit is:', depthLimit
		# 	bestMove = result['move']
		# 	bestValue = result['value']
		# 	#result = self.minimax(root, depthLimit, True, timeout)
		# 	result = self.alphaBetaPrunning(root, depthLimit, alpha, beta, True, timeout)
		# 	depthLimit += 1

		#result = self.minimax(root, 5, True, timeout)

		result = self.alphaBetaPrunning(root, 5, alpha, beta, True, timeout)

		bestMove = result['move']
		bestValue = result['value']
		
		return bestMove

		# moves = grid.getAvailableMoves()
		# return moves[randint(0, len(moves) - 1)] if moves else None

	def alphaBetaPrunning(self, root, depth, alpha, beta, playerTurn, timeout):
		#print 'current depth is:', depth

		if(time.time() > timeout):
			#print 'time out'
			return {"move": None, "value": root.getValue()}

		bestValue = -sys.maxint if playerTurn else sys.maxint
		bestMove = None
		result = None
		
		if playerTurn:
			if depth == 0:
				return {"move": None, "value": root.getValue()}
			
			moves = root.grid.getAvailableMoves()

			for move in moves:
				newGrid = root.grid.clone()
				if(newGrid.move(move)):
					childNode = TreeNode(newGrid, root, [])
					root.children.append(childNode)
					result = self.alphaBetaPrunning(childNode, depth - 1, alpha, beta, False, timeout)
					if result['value'] > bestValue:
						bestValue = result['value']
						bestMove = move
					#print 'max:', depth, bestValue, bestMove, alpha, beta
					alpha = max(alpha, bestValue)
					if alpha > beta:
						#print 'cutoff, return to depth', depth + 1
						return {'move': bestMove, 'value': alpha}

		else:
			if depth == 0:
				return {"move": None, "value": root.getValue()}

			childList = self.getChildNode(root)
			root.children = childList
		
			for childNode in root.children:
				result = self.alphaBetaPrunning(childNode, depth - 1, alpha, beta, True, timeout)
				if result['value'] < bestValue:
					bestValue = result['value']
					bestMove = result['move']
				#print 'min:', depth, bestValue, bestMove, alpha, beta
				beta = min(beta, bestValue)
				if beta < alpha:
					#print 'cutoff, return to depth', depth + 1
					return {'move': None, 'value': beta}
				
		#print 'return to depth', depth + 1
		return {'move': bestMove, 'value': bestValue}

	def minimax(self, root, depth, playerTurn, timeout): 
		#print depth, time.time()
		if(time.time() > timeout):
			#print 'time out'
			return {"move": None, "value": root.getValue()}

		bestValue = -sys.maxint if playerTurn else sys.maxint
		bestMove = None
		result = None
		
		if playerTurn:
			if depth == 0:
				return {"move": None, "value": root.getValue()}
			
			moves = root.grid.getAvailableMoves()

			for move in moves:
				newGrid = root.grid.clone()
				if(newGrid.move(move)):
					childNode = TreeNode(newGrid, root, [])
					root.children.append(childNode)
					result = self.minimax(childNode, depth - 1, False, timeout)
					if result['value'] > bestValue:
						bestValue = result['value']
						bestMove = move

		else:
			if depth == 0:
				return {"move": None, "value": root.getValue()}

			childList = self.getChildNode(root)
			root.children = childList
		
			for childNode in root.children:
				result = self.minimax(childNode, depth - 1, True, timeout)
				if result['value'] < bestValue:
					bestValue = result['value']
					bestMove = result['move']

		return {'move': bestMove, 'value': bestValue}

	def getChildNode(self, root):
		childList = []
		emptyPosition = root.grid.getAvailableCells()

		for position in emptyPosition:
			newGrid1 = root.grid.clone()
			newGrid1.insertTile(position, 2)
			childNode1 = TreeNode(newGrid1, root, [])
			newGrid2 = root.grid.clone()
			newGrid2.insertTile(position, 4)
			childNode2 = TreeNode(newGrid2, root, [])
			childList.append(childNode1)
			childList.append(childNode2)

		return childList


if __name__ == '__main__':
	map = [[0, 0, 4, 4], [4, 0, 16, 8], [0, 0, 2, 32], [0, 4, 2, 4]]
	map2 = [[1024, 512, 256, 128], [512, 256, 64, 16], [256, 64, 32, 0], [128, 128, 16, 0]]
	map3 = [[0, 2, 2, 4], [64, 32, 16, 8], [128, 256, 512, 1024], [8192, 8192, 4096, 2048]]
	map4 = [[2, 2, 4, 4], [4, 8, 16, 32], [2, 2, 4, 8], [8, 16, 32, 64]]
	grid = Grid(4)
	grid.setMap(map)
	node = TreeNode(grid, None, [])
	cell = {'x': 1, 'y': 0}
	vector = {'x': 0, 'y': 1}

	ai = PlayerAI()

	print node.getMonotonicity()













		

