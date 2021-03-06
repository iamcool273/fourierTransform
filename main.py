import cmath
import math
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
	
	def draw_spline(self, window, num_lines):
		points = []
		for i in range(num_lines + 1):
			points.append(self.get_coord(i / num_lines))
		self.undraw_spline()
		for i in range(num_lines):
			self.lines.append(Line(convert_point(points[i]), convert_point(points[i + 1])))
			self.lines[-1].draw(window)
			
	def undraw_spline(self):
		for line in self.lines:
			line.undraw()
		self.lines = []
	
	def print_data(self):
		print(f"x coefficients: {self.xCoefficients}\ny coefficients: {self.yCoefficients}")


def multiply_tuple(t, s):
	return tuple(int(s * i) for i in t)


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
		#complex(r.random() * 200 - 100, r.random() * 200 - 100)
		complex(0, 0)
	]
	for i in range(amount):
		real = (r.random() - 0.5) * size * 2
		imag = (r.random() - 0.5) * size * 2
		coefficients.append(complex(real, imag))
		real = (r.random() - 0.5) * size * 2
		imag = (r.random() - 0.5) * size * 2
		coefficients.append(complex(real, imag))
		size /= 1
	return coefficients


def init_drawings(win, points, lines, draw_points):
	graphic_points = [convert_point(t) for t in points]
	draw_points_new = [Circle(graphic_points[i], 2) for i in range(len(points))]
	
	lines_new = [Line(graphic_points[i], graphic_points[(i + 1) % len(points)]) for i in range(len(points))]

	for i in range(len(points)):
		draw_points.append(draw_points_new[i])
		draw_points[i].setFill("black")
		draw_points[i].draw(win)
		lines.append(lines_new[i])
		lines[i].draw(win)


def render_drawing(win, points, lines, draw_points, update_index):
	lines[update_index].undraw()
	lines[update_index - 1].undraw()
	lines[update_index] = Line(
		convert_point(points[update_index]),
		convert_point(points[(update_index + 1) % len(points)])
	)
	lines[update_index - 1] = Line(
		convert_point(points[update_index]),
		convert_point(points[update_index - 1])
	)
	lines[update_index].draw(win)
	lines[update_index - 1].draw(win)
	
	draw_points[update_index].undraw()
	draw_points[update_index] = Circle(convert_point(points[update_index]), 5)
	draw_points[update_index].setFill("black")
	draw_points[update_index].draw(win)
	
	
def find_closest_point(point, points):
	distances = [math.hypot(point[0] - points[i][0], point[1] - points[i][1]) for i in range(len(points))]
	return distances.index(min(distances))


def swap_with_next(ls, index):
	temp = ls[index]
	ls[index] = ls[index + 1]
	ls[index + 1] = temp
	
	
def get_sample_points(points, samples_per_line):
	complex_points = [complex(p[0], p[1]) for p in points]
	sample_points = []
	for i in range(len(points)):
		points_on_line = []
		for j in range(samples_per_line):
			ratio = j / samples_per_line
			sample_point = (complex_points[i] - complex_points[i - 1]) * ratio + complex_points[i - 1]
			points_on_line.append(sample_point)
		sample_points.extend(points_on_line)
	return sample_points


def calculate_average_point(sample_points):
	acc = complex(0, 0)
	for point in sample_points:
		acc += point
	acc /= len(sample_points)
	return acc


def complex_fourier_transform(sample_points, num_terms):
	coefficients = []
	for i in range(num_terms + 1):
		points = []
		rotation_speed = i
		for j in range(len(sample_points)):
			point = sample_points[j] * cmath.exp(complex(0, -2 * math.pi * rotation_speed * (j / len(sample_points))))
			points.append(point)
		coefficients.append(calculate_average_point(points))
		
		points = []
		rotation_speed = -i
		for j in range(len(sample_points)):
			point = sample_points[j] * cmath.exp(complex(0, -2 * math.pi * rotation_speed * (j / len(sample_points))))
			points.append(point)
		coefficients.append(calculate_average_point(points))
		
	coefficients.pop(0)
	return coefficients
	
	
def calculate_coefficients(points, samples_per_line, num_terms):
	sample_points = get_sample_points(points, samples_per_line)
	return complex_fourier_transform(sample_points, num_terms)


def main():
	window = GraphWin("Main Window", screen_width, screen_height, autoflush=False)
	
	points = [
		(0, 0),
		(0, 100),
		(100, 100),
		(100, 0)
	]
	lines = []
	draw_points = []
	init_drawings(window, points, lines, draw_points)
	index = None
	while window.isOpen():
		click = window.checkMouse()
		if click is not None:
			click = convert_point_to_tuple(click)
			if index is None:
				index = find_closest_point(click, points)
			else:
				if points[index] is not None:
					points[index] = click
				else:
					temp = find_closest_point(click, [points[index - 1], points[index + 1]])
					points[index] = click
					if temp == 1:
						swap_with_next(points, index)
						swap_with_next(lines, index)
						swap_with_next(draw_points, index)
						index += 1
			render_drawing(window, points, lines, draw_points, index)
		key = window.checkKey()
		if key is not None and index is not None:
			if key == "Shift_L":
				draw_points[index].undraw()
				draw_points[index] = Circle(convert_point(points[index]), 2)
				draw_points[index].setFill("black")
				draw_points[index].draw(window)
				points.insert(index, None)
				draw_points.insert(index, Circle(Point(0, 0), 0))
				lines.insert(index, Line(Point(0, 0), Point(0, 0)))
			if key == "f":
				if len(points) < 3:
					continue
				points.pop(index)
				lines[index].undraw()
				lines.pop(index)
				draw_points[index].undraw()
				draw_points.pop(index)
				render_drawing(window, points, lines, draw_points, index)
				key = "space"
			if key == "space":
				draw_points[index].undraw()
				draw_points[index] = Circle(convert_point(points[index]), 2)
				draw_points[index].setFill("black")
				draw_points[index].draw(window)
				index = None
		if key == "Return":
			break
		update(50)
	
	coefficients = calculate_coefficients(points, 10, 20)
	coefficients = generate_random_coefficients(3)
	rotations(window, coefficients)


if __name__ == '__main__':
	main()
