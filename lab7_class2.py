import math
# Задание 1. Иерархия и полиморфизм
class Shape:  # базовый класс
    def __init__(self, name, color):
        self.name = name  # название фигуры
        self.color = color  # цвет фигуры
    def get_area(self):
        print(f"{self.name}: площадь не определена")  # базовое сообщение

class Triangle(Shape):
    def __init__(self, name, color, a, b, c):
        super().__init__(name, color)  # общие атрибуты - в родителя
        self.a, self.b, self.c = a, b, c  # три стороны
    def get_area(self):  # переопределяем метод
        p = (self.a + self.b + self.c) / 2  # полупериметр
        area = math.sqrt(p * (p - self.a) * (p - self.b) * (p - self.c))  # формула Герона
        print(f"Треугольник '{self.name}': площадь = {area:.2f}")
        return area

class Circle(Shape):
    def __init__(self, name, color, radius):
        super().__init__(name, color)
        self.radius = radius  # радиус
    def get_area(self):  # переопределяем метод
        area = math.pi * self.radius ** 2  # площадь круга
        print(f"Круг '{self.name}': площадь = {area:.2f}")
        return area

# Задание 2. Контейнер Drawing и «ловушка списков»
class Drawing:
    def __init__(self, name):
        self.name = name
        self._shapes = []  # композиция: список внутри, а не наследование от list
    def add_shape(self, shape):
        self._shapes.append(shape)  # добавить фигуру на чертёж
    def __len__(self):
        return len(self._shapes)  # len(drawing)
    def __getitem__(self, index):
        return self._shapes[index]  # drawing[0] -> объект Shape
    def __str__(self):  # для пользователя (print)
        names = ", ".join(s.name for s in self._shapes)
        return f"📐 Чертёж '{self.name}': {names}"
    def __repr__(self):   # для разработчика (внутри списков, в отладке)
        return f"Drawing(name='{self.name}', shapes_count={len(self)})"

# Задание 3. Арифметика объектов Point2D
class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __add__(self, other):  # p1 + p2
        return Point2D(self.x + other.x, self.y + other.y)  # НОВЫЙ объект, self не меняем
    def __sub__(self, other):  # p1 - p2
        return Point2D(self.x - other.x, self.y - other.y)  # тоже новый объект
    def __abs__(self):  # abs(p)
        return math.hypot(self.x, self.y)  # расстояние до (0, 0)
    def __lt__(self, other):  # p1 < p2, нужно для sorted()
        return abs(self) < abs(other)  # сравниваем по удалённости от центра
    def __eq__(self, other):  # p1 == p2
        return self.x == other.x and self.y == other.y
    def __repr__(self):
        return f"Point2D({self.x}, {self.y})"

# Задание 4. Итератор пифагоровых троек
class PythagoreanIterator:
    def __init__(self, limit):
        self.limit = limit  # сколько троек выдать
        self.count = 0  # сколько уже выдано
        self.c = 1  # текущая гипотенуза
        self.a = 0  # текущий катет a
    def __iter__(self):
        return self  # итератор возвращает сам себя
    def __next__(self):
        if self.count >= self.limit:  # лимит достигнут
            raise StopIteration
        while True:  # перебор, пока не найдём тройку
            self.a += 1
            if self.a >= self.c:  # катеты кончились - увеличиваем c
                self.c += 1
                self.a = 1
            b_sq = self.c ** 2 - self.a ** 2
            b = math.isqrt(b_sq)  # целая часть корня
            if b * b == b_sq and self.a < b:  # b целое, а < b (без дублей)
                self.count += 1
                return (self.a, b, self.c)

# Демонстрация
if __name__ == "__main__":
    print("=== Задание 1: полиморфизм ===")
    shapes = [Triangle("T1", "красный", 3, 4, 5), Circle("C1", "синий", 2)]
    for shape in shapes:  # один интерфейс, без проверки типов
        shape.get_area()  # Python сам выбирает нужную версию

    print("\n=== Задание 2: контейнер и «ловушка списков» ===")
    drawing = Drawing("Деталь №1")
    for s in shapes:
        drawing.add_shape(s)
    print("len:", len(drawing))  # 2
    print("drawing[0]:", drawing[0].name)  # первая фигура
    print(drawing)  # print вызывает __str__ (красиво)
    print([drawing])  # внутри списка Python вызывает __repr__ (технически)
    # Ловушка: списки всегда показывают элементы через __repr__, а не __str__

    print("\n=== Задание 3: арифметика ===")
    p1, p2 = Point2D(1, 2), Point2D(4, 6)
    print("p1 + p2 =", p1 + p2)
    print("p1 - p2 =", p1 - p2)
    print("abs(p2) =", abs(p2))
    print("p1 < p2:", p1 < p2, "| p1 == p2:", p1 == p2)
    print("После операций:", p1, p2)  # не изменились (immutability)
    print("sorted:", sorted([p2, Point2D(0, 1), p1]))  # работает благодаря __lt__

    print("\n=== Задание 4: итератор ===")
    it = PythagoreanIterator(5)
    for triple in it:  # for сам вызывает __iter__ и __next__
        print(triple)
    try:
        next(it)  # пробуем взять ещё одно значение
    except StopIteration:
        print("Итератор «сгорел»: он помнит, что лимит исчерпан, и не перематывается")
    print("Повторный for:", list(it))  # [] - пусто, итератор уже исчерпан
print("\n=== Задание 3: арифметика ===")
p1, p2 = Point2D(1, 2), Point2D(4, 6)                       # две точки
print("Точка p1:", p1)                                      # __repr__
print("Точка p2:", p2)
print("Сумма p1 + p2 =", p1 + p2)                           # __add__
print("Разность p1 - p2 =", p1 - p2)                        # __sub__
print("Расстояние от p2 до центра:", round(abs(p2), 2))     # __abs__
print("p1 ближе к центру, чем p2:", p1 < p2)                # __lt__
print("p1 и p2 равны:", p1 == p2)                           # __eq__
print("p1 и p2 после операций не изменились:", p1, p2)      # новые объекты
print("Точки по удалённости от центра:", sorted([p2, Point2D(0, 1), p1]))  # sorted через __lt__
