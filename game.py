import numpy as np
import logging

class Game:

	def __init__(self):		
		self.currentPlayer = 1
		self.State = GameState(np.array([0,0,0,0,0,0,0,0,0], dtype=np.int), self.currentPlayer)
		self.actionSpace = np.array([0,0,0,0,0,0,0,0,0], dtype=np.int)
		self.pieces = {'1':'X', '0': '-', '-1':'O'}
		self.grid_shape = (3,3)
		self.input_shape = (2,3,3)
		self.name = 'tictac'
		self.state_size = 18
		self.action_size = 9

	def reset(self):
		self.currentPlayer = 1
		self.gameState = GameState(np.array([0,0,0,0,0,0,0,0,0], dtype=np.int), self.currentPlayer)
		return self.gameState

	def step(self, action):
		next_state, value, done = self.gameState.takeAction(action)
		self.gameState = next_state
		self.currentPlayer = -self.currentPlayer
		return ((next_state, value, done))

	def identities(self, state, actionValues):
		identities = [(state,actionValues)]

		currentBoard = state.board
		currentAV = actionValues

		currentBoard = np.array(state.board)

		currentAV = np.array(actionValues)

		identities.append((GameState(currentBoard, state.player), currentAV))

		return identities


class GameState():
	def __init__(self, board, player):
		self.board = board
		self.pieces = {'1':'X', '0': '-', '-1':'O'}
		self.winners = [
			[0,1,2],
			[3,4,5],
			[6,7,8],
			[2,5,8],
			[1,4,7],
			[0,3,6],
			[2,4,6],
			[0,4,8]
			]
		self.player = player
		self.binary = self._binary()
		self.id = self._convertStateToId()
		self.allowedActions = self._allowedActions()
		self.value = self._getValue()
		self.isEndGame = self._checkForEndGame()
		self.score = self._getScore()

	def _allowedActions(self):
		allowed = [a for a in self.board if a!=0]

		return allowed

	def _binary(self):

		currentplayer_position = np.zeros(len(self.board), dtype=np.int)
		currentplayer_position[self.board==self.player] = 1

		other_position = np.zeros(len(self.board), dtype=np.int)
		other_position[self.board==-self.player] = 1

		position = np.append(currentplayer_position,other_position)

		return (position)	

	def _convertStateToId(self):

		id = ''.join(map(str,self.binary))

		return id

	def _checkForEndGame(self):
		if np.count_nonzero(self.board) == 9:
			return 1


		return self.value[2]

	def _getValue(self):
		# This is the value of the state for the current player
		# i.e. if the previous player played a winning move, you lose
		for x,y,z in self.winners:
			if (self.board[x] + self.board[y] + self.board[z] == 3 * -self.player):
				return (-1, -1, 1)
		return (0, 0, 0)


	def _getScore(self):
		tmp = self.value
		return (tmp[1], tmp[2])




	def takeAction(self, action):
		newBoard = np.array(self.board)
		newBoard[action]=self.player
		
		newState = GameState(newBoard, -self.player)

		value = 0
		done = 0

		if newState.isEndGame:
			value = newState.value[0]
			done = 1

		return (newState, value, done) 




	def render(self, logger):
		for r in range(3):
			logger.info([self.pieces[str(x)] for x in self.board[3*r : (3*r + 3)]])
		logger.info('--------------')