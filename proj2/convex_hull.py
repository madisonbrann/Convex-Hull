from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF, QObject
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))



import time
import math


# Some global color constants that might be useful
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# Global variable that controls the speed of the recursion automation, in seconds
#
PAUSE = 0.25

#
# This is the class you have to complete.
#
class ConvexHullSolver(QObject):

# Class constructor
	def __init__( self):
		super().__init__()
		self.pause = False
		
# Some helper methods that make calls to the GUI, allowing us to send updates
# to be displayed.

	def showTangent(self, line, color):
		self.view.addLines(line,color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseTangent(self, line):
		self.view.clearLines(line)

	def blinkTangent(self,line,color):
		self.showTangent(line,color)
		self.eraseTangent(line)

	def showHull(self, polygon, color):
		self.view.addLines(polygon,color)
		if self.pause:
			time.sleep(PAUSE)
		
	def eraseHull(self,polygon):
		self.view.clearLines(polygon)
		
	def showText(self,text):
		self.view.displayStatusText(text)
	
	def mySort(self, points, l_index, r_index):
		if l_index < r_index:
			res = math.floor((l_index + r_index)/2)
			self.mySort(points,l_index,res)
			self.mySort(points, res + 1, r_index)
			self.mergeSort(points,l_index,res,r_index)

	def mergeSort(self, points,l_index,mid_index,r_index):
		l_arr_size = mid_index - l_index + 1
		r_arr_size = r_index - mid_index
		print(l_arr_size)
		left_arr = []
		right_arr = []
		for ini in range(0,l_arr_size):
			left_arr.append(0)
		for ini in range(0,r_arr_size):
			right_arr.append(0)

		for i in range(0, l_arr_size):
			left_arr[i] = points[l_index + i]
		for j in range(0,r_arr_size):
			right_arr[j] = points[mid_index + j + 1]
		
		i = 0
		j = 0
		k = l_index

		while i < l_arr_size and j < r_arr_size:
			if left_arr[i].x() < right_arr[j].x():
				points[k] = left_arr[i]
				i+= 1
			elif left_arr[i].x() > right_arr[j].x():
				points[k] = right_arr[j]
				j +=1
			else:
				if left_arr[i].y() < right_arr[j].y():
					points[k] = left_arr[i]
					i += 1
				else:
					points[k] = right_arr[j]
					j += 1
			k+=1
		while i < l_arr_size:
			points[k] = left_arr[i]
			i+=1
			k+=1
		while j < r_arr_size:
			points[k] = right_arr[j]
			j+=1
			k+=1

	def divide_and_conquer(self, points):
		if (len(points) == 1):
			return points
		
		l_half = self.divide_and_conquer(points[0: math.floor(len(points) / 2)])
		r_half= self.divide_and_conquer(points[math.floor(len(points) / 2):])

		return self.merge(l_half,r_half)
	
	def merge(self,l_half,r_half):
		print("yooo")
		if (len(l_half) + len(r_half) < 4):
			x,y = self.get_center(l_half + r_half)

	def get_center(self, points):
		x = [point.x() for point in points]
		y = [point.y for point in points]
		x = sum(x)/len(points)
		y = sum(y)/len(points)
		print("YOOO")
		return x,y




# This is the method that gets called by the GUI and actually executes
# the finding of the hull
	def compute_hull( self, points, pause, view):
		self.pause = pause
		self.view = view
		assert( type(points) == list and type(points[0]) == QPointF )

		t1 = time.time()
	
		# TODO: SORT THE POINTS BY INCREASING X-VALUE
		print(points)
		self.mySort(points, 0, len(points) - 1)
		print("sorted")
		print(points)
		t2 = time.time()

		t3 = time.time()
		# this is a dummy polygon of the first 3 unsorted points
		polygon = self.divide_and_conquer(points)
		# TODO: REPLACE THE LINE ABOVE WITH A CALL TO YOUR DIVIDE-AND-CONQUER CONVEX HULL SOLVER
		t4 = time.time()

		# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# object can be created with two QPointF objects corresponding to the endpoints
		self.showHull(polygon,RED)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))



