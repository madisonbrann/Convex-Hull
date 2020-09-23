from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF, QObject
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))



import time
import math
from functools import partial


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
		
		l_half = self.divide_and_conquer(points[0: len(points) // 2])
		r_half= self.divide_and_conquer(points[len(points) // 2:])

		return self.merge(l_half,r_half)
	
	def merge(self,l_half,r_half):
		if (len(l_half) + len(r_half) < 4):
			x,y = self.get_center(l_half + r_half)
			output1 = sorted(l_half + r_half, key=partial(self.clockwise, x_point = x, y_point = y))
			return output1
		left_beg = self.closest_point(l_half,"l")
		right_beg = self.closest_point(r_half,"r")
		l_top_tan,r_top_tan = self.get_up_tan(left_beg,l_half,right_beg,r_half)
		r_bottom_tan,l_bottom_tan = self.get_up_tan(right_beg,r_half,left_beg,l_half)
		output2 = []
		output2.append(l_half[l_top_tan])
		index = r_top_tan
		while r_half[index % len(r_half)] != r_half[r_bottom_tan]:
			output2.append(r_half[index % len(r_half)])
			index += 1
		output2.append(r_half[r_bottom_tan])
		index = l_bottom_tan
		while l_half[index % len(l_half)] != l_half[l_top_tan]:
			output2.append(l_half[index % len(l_half)])
			index += 1
		return output2
		


	def get_up_tan(self, left_beg, l_half,right_beg,r_half):
		l_index = left_beg
		r_index = right_beg
		prev_tan = tuple([l_index,r_index])
		while True:

			slope = self.find_slope(l_half[(l_index - 1) % len(l_half)],r_half[r_index])
			left_decreasing = True
			while left_decreasing == True:
				slope2 = self.find_slope(l_half[(l_index - 1) % len(l_half)], r_half[r_index])

				if slope2 < slope:
					slope = slope2
					l_index -= 1
					if l_index < 0:
						l_index = len(l_half) - 1
					left_decreasing = True
				else:
					left_decreasing = False

			right_increasing = True
			while right_increasing == True:
				slope2 = self.find_slope(l_half[l_index],r_half[(r_index + 1) % len(r_half)])
				if slope2 > slope:
					slope = slope2
					r_index += 1
					if r_index >= len(r_half):
						r_index %= len(r_half)
					right_increasing = True
				else:
					right_increasing = False
			current_tan = tuple([l_index,r_index])
			if prev_tan == current_tan:
				break
			prev_tan = current_tan
		return l_index,r_index

	def find_slope(self,left, right):
		output = (right.y() - left.y())/(right.x() - left.x())
		return output

	def closest_point(self,points,side):
		index = 0
		if side == "l":
			for i, point in enumerate(points):
				if point.x() > points[index].x():
					index = i
		if side == "r":
			for i, point in enumerate(points):
				if point.x() < points[index].x():
					index = i
		return index
		
	def clockwise(self,point, x_point, y_point, anchor="ne"):
		output = math.atan2(point.x() - x_point, point.y() - y_point)
		return output
	def get_center(self, points):
		x = [point.x() for point in points]
		y = [point.y() for point in points]
		x = sum(x)/len(points)
		y = sum(y)/len(points)

		return x,y




# This is the method that gets called by the GUI and actually executes
# the finding of the hull
	def compute_hull( self, points, pause, view):
		self.pause = pause
		self.view = view
		assert( type(points) == list and type(points[0]) == QPointF )

		t1 = time.time()
	
		# TODO: SORT THE POINTS BY INCREASING X-VALUE
		self.mySort(points, 0, len(points) - 1)
		t2 = time.time()

		t3 = time.time()
		# this is a dummy polygon of the first 3 unsorted points
		polygon = self.divide_and_conquer(points)
		print("this happened")
		print(polygon)
		# TODO: REPLACE THE LINE ABOVE WITH A CALL TO YOUR DIVIDE-AND-CONQUER CONVEX HULL SOLVER
		t4 = time.time()

		# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# object can be created with two QPointF objects corresponding to the endpoints
		self.showHull(polygon,RED)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))



