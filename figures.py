# standard modules
import abc
import math
import numbers
from tkinter import *

import descriptors as ds
# additional modules
from colors import *


# additional functions
def Point(x, y):
    return x, y


def Vector(length, angle):
    return length, angle


def apply_vector(point, vector):
    length, angle = vector
    return point[0] + math.cos(angle) * length, point[1] + math.sin(angle) * length


def transform_vector(point, move):
    return point[0] + move[0], point[1] + move[1]


class ConvexPolygon(abc.ABC):
    @abc.abstractmethod
    def __init__(self):
        self.fill_colour = Color.CYAN
        self.outline_colour = Color.BLACK
        self.window_width = 720
        self.window_height = 720

    @abc.abstractmethod
    def area(self):
        pass

    @abc.abstractmethod
    def perimeter(self):
        pass

    @abc.abstractmethod
    def draw(self):
        pass

    def open_window(self, vertices, area, perimeter):
        root = Tk()
        label = Label(root, text=f"Area: {round(area,5)} \tPerimeter: {round(perimeter, 2)}", font=("Arial", 24, "bold italic"))
        label.pack()

        canvas = Canvas(root, width=self.window_width, height=self.window_height)
        canvas.pack()
        canvas.create_polygon(vertices, fill=self.fill_colour, outline=self.outline_colour)

        mainloop()


class Triangle(ConvexPolygon):
    a = ds.TypeAndQuantity(numbers.Real)
    b = ds.TypeAndQuantity(numbers.Real)
    c = ds.TypeAndQuantity(numbers.Real)

    def __init__(self, a, b, c):
        super().__init__()
        self.a = a
        self.b = b
        self.c = c
        self.alpha = self._calculate_angle()

    @classmethod
    def user_input(cls):
        print("Triangle: enter the side lengths:")
        a = float(input('a: '))
        b = float(input('b: '))
        c = float(input('c: '))

        return cls(a, b, c)

    def _calculate_angle(self):
        # site: https://pl.numberempire.com/arbitrary_triangle_calculator.php
        return math.degrees(math.acos(math.radians((self.b ** 2 + self.c ** 2 - self.a ** 2) / (2 * self.b * self.c))))

    def perimeter(self):
        return self.a + self.b + self.c

    def area(self):
        # Heron's formula
        p = self.perimeter() / 2
        return math.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))

    def draw(self):
        p1 = (0, 0)
        angle = self.alpha
        p2 = apply_vector(p1, Vector(self.b, math.radians(270 + angle / 2)))
        p3 = apply_vector(p1, Vector(self.c, 0))

        q = ((p1[0] + p2[0] + p3[0]) / 3, (p1[1] + p2[1] + p3[1]) / 3)
        transform_value = (self.window_width / 2 - q[0], self.window_height / 2 - q[1])
        p1 = transform_vector(p1, transform_value)
        p2 = transform_vector(p2, transform_value)
        p3 = transform_vector(p3, transform_value)

        self.open_window([p1, p2, p3], self.area(), self.perimeter())


# site: http://bazywiedzy.com/czworokat-wypukly.html
class ConvexQuadrilateral(ConvexPolygon):
    # diagonals: d1->AC; d2->BD; S-> center
    d1 = ds.TypeAndQuantity(numbers.Real)
    d2 = ds.TypeAndQuantity(numbers.Real)

    angle = ds.Range(0, 91)

    d1_ratio = ds.Range(0, 1)
    d2_ratio = ds.Range(0, 1)

    def __init__(self, d1, d2, angle, d1_ratio, d2_ratio):
        super().__init__()
        self.d1 = d1
        self.d2 = d2
        self.angle = angle
        self.d1_ratio = d1_ratio
        self.d2_ratio = d2_ratio
        self._calculate_sides()

    @classmethod
    def user_input(cls):
        print("Convex Quadrilateral:\nenter diagonal lengths:")
        d1 = float(input("d1(AC): "))
        d2 = float(input("d2(BD): "))
        angle = float(input("enter the angle between diagonals: "))
        print("enter the intersection ratio:")
        d1_ratio = float(input("d1 wzgledem d2: "))
        d2_ratio = float(input("d2 wzgledem d1: "))
        return cls(d1, d2, angle, d1_ratio, d2_ratio)

    def _calculate_sides(self):
        self.AS = self.d1 * self.d1_ratio
        self.CS = self.d1 - self.AS

        self.BS = self.d2 * self.d2_ratio
        self.DS = self.d2 - self.BS

    def perimeter(self):
        # cosine theorem
        ab = math.sqrt(self.AS ** 2 + self.BS ** 2 - 2 * self.AS * self.BS * math.cos(math.radians(self.angle)))
        bc = math.sqrt(self.BS ** 2 + self.CS ** 2 - 2 * self.BS * self.CS * math.cos(math.radians(180 - self.angle)))
        cd = math.sqrt(self.CS ** 2 + self.DS ** 2 - 2 * self.CS * self.DS * math.cos(math.radians(self.angle)))
        da = math.sqrt(self.DS ** 2 + self.AS ** 2 - 2 * self.DS * self.AS * math.cos(math.radians(180 - self.angle)))

        return ab + bc + cd + da

    def area(self):
        return (self.d1 * self.d2 * math.sin(math.radians(self.angle))) / 2

    def draw(self):
        s = Point(self.window_width / 2, self.window_height / 2)
        a = apply_vector(s, Vector(-self.AS, 0))
        b = apply_vector(s, Vector(self.BS, math.radians(360 - self.angle)))
        c = apply_vector(s, Vector(self.CS, 0))
        d = apply_vector(s, Vector(self.DS, math.radians(180 - self.angle)))

        self.open_window([a, b, c, d], self.area(), self.perimeter())


class RegularPolygon(ConvexPolygon):
    side = ds.TypeAndQuantity(numbers.Real)
    number_of_sides = ds.TypeAndQuantity(int, 2)

    def __init__(self, side, number_of_sides):
        super().__init__()
        self.side = side
        self.number_of_sides = number_of_sides

    @classmethod
    def user_input(cls):
        print("RegularPolygon:")
        number_of_sides = int(input("enter the number of sides: "))
        side = float(input("enter the side length: "))
        return cls(side, number_of_sides)

    def perimeter(self):
        return self.side * self.number_of_sides

    def area(self):
        # site: https://calcoolator.pl/obwod-pole-przekatne-wysokosc-wielkata-foremnego.html
        return (self.side ** 2 * self.number_of_sides) / (4 * math.tan(math.pi / self.number_of_sides))

    def draw(self):
        points = []
        point = Point(self.window_width / 2, self.window_height / 2)

        r = self.side / (2 * math.sin(math.pi / self.number_of_sides))
        angle = 360 / self.number_of_sides
        for i in range(self.number_of_sides):
            points.append(Point(
                point[0] + r * math.cos((i * angle + 270 if i * angle < 360 else i * angle) * math.pi / 180),
                point[1] + r * math.sin((i * angle + 270 if i * angle < 360 else i * angle) * math.pi / 180)))

        self.open_window(points, self.area(), self.perimeter())


class RegularPentagon(RegularPolygon):
    def __init__(self, side):
        super().__init__(side, 5)

    @classmethod
    def user_input(cls):
        print("RegularPentagon:")
        side = float(input("enter the side length: "))
        return cls(side)


class RegularHexagon(RegularPolygon):
    def __init__(self, side):
        super().__init__(side, 6)

    @classmethod
    def user_input(cls):
        print("RegularHexagon:")
        side = float(input("enter the side length: "))
        return cls(side)


# site: https://en.wikipedia.org/wiki/Octagon#Regular_octagon
class RegularOctagon(RegularPolygon):
    def __init__(self, side):
        super().__init__(side, 8)

    @classmethod
    def user_input(cls):
        print("RegularOctagon:")
        side = float(input("enter the side length: "))
        return cls(side)


class IsoscelesTriangle(Triangle):
    def __init__(self, base, sides):
        super().__init__(base, sides, sides)

    @classmethod
    def user_input(cls):
        print("IsoscelesTriangle: enter the length:")
        base = float(input('radix: '))
        sides = float(input('side: '))

        return cls(base, sides)


class EquilateralTriangle(Triangle):
    def __init__(self, sides):
        super().__init__(sides, sides, sides)

    @classmethod
    def user_input(cls):
        print("IsoscelesTriangle:")
        sides = float(input('enter the length of the sides: '))

        return cls(sides)


class Parallelogram(ConvexQuadrilateral):
    # diagonals: d1->AC; d2->BD
    d1 = ds.TypeAndQuantity(numbers.Real)
    d2 = ds.TypeAndQuantity(numbers.Real)

    angle = ds.Range(0, 91)

    def __init__(self, d1, d2, angle):
        super().__init__(d1, d2, angle, 0.5, 0.5)

    @classmethod
    def user_input(cls):
        print("Parallelogram:\nenter diagonal lengths:")
        d1 = float(input("d1(AC): "))
        d2 = float(input("d2(BD): "))
        angle = float(input("enter the angle between diagonals: "))
        return cls(d1, d2, angle)

    def perimeter(self):
        ab = math.sqrt(self.AS ** 2 + self.BS ** 2 - 2 * self.AS * self.BS * math.cos(math.radians(self.angle)))
        bc = math.sqrt(self.BS ** 2 + self.CS ** 2 - 2 * self.BS * self.CS * math.cos(math.radians(180 - self.angle)))

        return 2 * ab + 2 * bc

    def area(self):
        return (self.d1 * self.d2 * math.sin(math.radians(self.angle))) / 2


class Kite(ConvexQuadrilateral):
    # diagonals: d1->AC; d2->BD
    d1 = ds.TypeAndQuantity(numbers.Real)
    d2 = ds.TypeAndQuantity(numbers.Real)

    d2_ratio = ds.Range(0, 1)

    def __init__(self, d1, d2, d2_ratio):
        super().__init__(d1, d2, 90, 0.5, d2_ratio)

    @classmethod
    def user_input(cls):
        print("Kite:\nenter diagonal lengths:")
        d1 = float(input("d1(AC): "))
        d2 = float(input("d2(BD): "))
        d2_ratio = float(input("enter the intersection ratio d2 to d1: "))
        return cls(d1, d2, d2_ratio)

    def perimeter(self):
        ab = math.sqrt(self.AS ** 2 + self.BS ** 2 - 2 * self.AS * self.BS * math.cos(math.radians(self.angle)))
        bc = math.sqrt(self.BS ** 2 + self.CS ** 2 - 2 * self.BS * self.CS * math.cos(math.radians(180 - self.angle)))
        return 2 * ab + 2 * bc

    def area(self):
        return (self.d1 * self.d2) / 2


class Rhombus(Kite):
    d1 = ds.TypeAndQuantity(numbers.Real)
    d2 = ds.TypeAndQuantity(numbers.Real)

    def __init__(self, d1, d2):
        super().__init__(d1, d2, 0.5)

    @classmethod
    def user_input(cls):
        print("Rhombus:\nenter diagonal lengths:")
        d1 = float(input("d1(AC): "))
        d2 = float(input("d2(BD): "))
        return cls(d1, d2)

    def perimeter(self):
        ab = math.sqrt(self.AS ** 2 + self.BS ** 2 - 2 * self.AS * self.BS * math.cos(math.radians(self.angle)))
        return 4 * ab

    def area(self):
        return (self.d1 * self.d2) / 2


class Square(Rhombus):
    a = ds.TypeAndQuantity(numbers.Real)

    def __init__(self, a):
        super().__init__(a, a)

    @classmethod
    def user_input(cls):
        print("Square:")
        a = float(input("enter the side length: "))
        d = a * math.sqrt(2)
        return cls(d)

    def draw(self):
        s = Point(self.window_width / 2, self.window_height / 2)
        a = apply_vector(s, Vector(self.d1 / 2, math.radians(135)))
        b = apply_vector(s, Vector(self.d1 / 2, math.radians(225)))
        c = apply_vector(s, Vector(self.d1 / 2, math.radians(315)))
        d = apply_vector(s, Vector(self.d1 / 2, math.radians(45)))

        self.open_window([a, b, c, d], self.area(), self.perimeter())
