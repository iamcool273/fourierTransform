import cmath
import random as r

from graphics import *

screen_width = 800
screen_height = 600


class SplineCurve:
	xCoefficients = (0, 0, 0, 0)
	yCoefficients = (0, 0, 0, 0)
	lines = []
	
	def __init__(self, point_a, tangent_a, point_b, tangent_b):
		x_start = point_a[0]
		x_end = point_b[0]
		x_start_slope = tangent_a[0]
		x_end_slope = tangent_b[0]
		x_polynomial = multiply_tuple((2, -3, 0, 1), x_start)
		x_polynomial = add_tuples(x_polynomial, multiply_tuple((-2, 3, 0, 0), x_end))
		x_polynomial = add_tuples(x_polynomial, multiply_tuple((1, -2, 1, 0), x_start_slope))
		self.xCoefficients = add_tuples(x_polynomial, multiply_tuple((1, -1, 0, 0), x_end_slope))
		
		y_start = point_a[1]
		y_end = point_b[1]
		y_start_slope = tangent_a[1]
		y_end_slope = tangent_b[1]
		y_polynomial = multiply_tuple((2, -3, 0, 1), y_start)
		y_polynomial = add_tuples(y_polynomial, multiply_tuple((-2, 3, 0, 0), y_end))
		y_polynomial = add_tuples(y_polynomial, multiply_tuple((1, -2, 1, 0), y_start_slope))
		self.yCoefficients = add_tuples(y_polynomial, multiply_tuple((1, -1, 0, 0), y_end_slope))
	
	def get_coord(self, u):
		x = pow(u, 3) * self.xCoefficients[0] + pow(u, 2) * self.xCoefficients[1] + \
			u * self.xCoefficients[2] + self.xCoefficients[3]
		y = pow(u, 3) * self.yCoefficients[0] + pow(u, 2) * self.yCoefficients[1] + \
			u * self.yCoefficients[2] + self.yCoefficients[3]
		return x, y
	
	def draw_spline(self, window, num_points):
		points = []
		for i in range(num_points):
			points.append(self.get_coord(i / num_points))
		self.undraw_spline()
		for i in range(num_points - 1):
			self.lines.append(Line(convert_point(points[i]), convert_point(points[i + 1])))
			self.lines[-1].draw(window)
			
	def undraw_spline(self):
		for line in self.lines:
			line.undraw()
		self.lines = []
	
	def print_data(self):
		print(f"x coefficients: {self.xCoefficients}\ny coefficients: {self.yCoefficients}")


def multiply_tuple(t, s):
	return tuple(s * i for i in t)


def add_tuples(a, b):
	return tuple(a[i] + b[i] for i in range(len(a)))


def convert_point(t):
	return make_point(t[0], t[1])


def make_point(x, y):
	return Point(int(x) + screen_width // 2, screen_height // 2 - int(y))


def convert_point_to_tuple(point):
	return point.x - screen_width // 2, screen_height // 2 - point.y


def clear(win):
	for item in win.items[:]:
		item.undraw()


def draw_line(window, start, coefficient, step):
	end = start + coefficient * cmath.exp(complex(0, cmath.pi * 2 * step))
	start_point = make_point(start.real, start.imag)
	end_point = make_point(end.real, end.imag)
	line = Line(start_point, end_point)
	line.draw(window)
	return end, line


def get_rotation_speed(index):
	index += 1
	speed = index // 2
	speed *= 1 - (index % 2) * 2
	return speed


def draw_lines(window, coefficients, step):
	next_start = complex(0, 0)
	lines = []
	for i, coefficient in enumerate(coefficients):
		next_start, line = draw_line(window, next_start, coefficient, step * get_rotation_speed(i))
		lines.append(line)
	return next_start, lines


def draw_shape(window, points):
	for i in range(len(points) - 1):
		line = Line(points[i], points[i + 1])
		line.draw(window)
	line = Line(points[-1], points[0])
	line.draw(window)


def rotations(window, coefficients):
	step = 0
	points = []
	while step < 1:
		point, _ = draw_lines(window, coefficients, step)
		point = make_point(point.real, point.imag)
		points.append(point)
		step += 0.002
	step = 0
	clear(window)
	draw_shape(window, points)
	lines = []
	point = Point(0, 0)
	point.draw(window)
	while window.isOpen():
		if step >= 1:
			step = 0
		else:
			step += 0.002
		for line in lines:
			line.undraw()
		point.undraw()
		point, lines = draw_lines(window, coefficients, step)
		point = make_point(point.real, point.imag)
		point = Circle(point, 2)
		point.setFill("black")
		point.draw(window)
		update(50)


def generate_random_coefficients(amount):
	size = 100
	coefficients = [
		complex(0, 0)
	]
	for i in range(amount):
		real = (r.random() - 0.5) * size * 2
		imag = (r.random() - 0.5) * size * 2
		coefficients.append(complex(real, imag))
		real = (r.random() - 0.5) * size * 2
		imag = (r.random() - 0.5) * size * 2
		coefficients.append(complex(real, imag))
		size /= 1.35
	return coefficients


def main():
	window = GraphWin("Main Window", screen_width, screen_height, autoflush=False)
	#"""
	coefficients = generate_random_coefficients(10)
	rotations(window, coefficients)
	"""
	points = [
		(-100, 0),
		(100, 0)
	]
	tangents = [
		(0, -100),
		(0, 100)
	]
	splines = [
		SplineCurve(points[-1], tangents[-1], points[0], tangents[0]),
		SplineCurve(points[0], tangents[0], points[1], tangents[1])
	]
	while window.isOpen():
		point = window.checkMouse()
		if isinstance(point, Point):
			key = window.checkKey()
			point = convert_point_to_tuple(point)
			update(50)
#"""


if __name__ == '__main__':
	main()
