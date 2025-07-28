# Задание 1: Наследование
class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}  # курс -> [список оценок]

    def get_average_grade(self):
        total = 0
        count = 0
        for grades in self.grades.values():
            total += sum(grades)
            count += len(grades)
        return round(total / count, 1) if count else 0

    def __str__(self):
        avg = self.get_average_grade()
        return (super().__str__() +
                f'\nСредняя оценка за лекции: {avg}')

    def __lt__(self, other):
        if isinstance(other, Lecturer):
            return self.get_average_grade() < other.get_average_grade()
        return (f'Ошибка')

    def __le__(self, other):
        if isinstance(other, Lecturer):
            return self.get_average_grade() <= other.get_average_grade()
        return (f'Ошибка')

    def __eq__(self, other):
        if isinstance(other, Lecturer):
            return self.get_average_grade() == other.get_average_grade()
        return (f'Ошибка')


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):

        if (isinstance(student, Student) and
            course in self.courses_attached and
            course in student.courses_in_progress):
            if course not in student.grades:
                student.grades[course] = []
            student.grades[course].append(grade)
            return None
        else:
            return (f'Ошибка')

    def __str__(self):
        return super().__str__()


class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecture(self, lecturer, course, grade):

        if not isinstance(lecturer, Lecturer):
            return 'Ошибка: можно оценивать только лекторов.'
        if course not in self.courses_in_progress:
            return 'Ошибка: вы не изучаете этот курс.'
        if course not in lecturer.courses_attached:
            return 'Ошибка: лектор не ведёт этот курс.'
        if not isinstance(grade, int) or not (1 <= grade <= 10):
            return 'Ошибка: оценка должна быть целым числом от 1 до 10.'

        if course not in lecturer.grades:
            lecturer.grades[course] = []
        lecturer.grades[course].append(grade)
        return None

    def get_average_grade(self):
        total = 0
        count = 0
        for grades in self.grades.values():
            total += sum(grades)
            count += len(grades)
        return round(total / count, 1) if count else 0

    def __str__(self):
        avg = self.get_average_grade()
        courses_in_progress = ', '.join(self.courses_in_progress) if self.courses_in_progress else 'нет'
        finished_courses = ', '.join(self.finished_courses) if self.finished_courses else 'нет'
        return (f'Имя: {self.name}\n'
                f'Фамилия: {self.surname}\n'
                f'Средняя оценка за домашние задания: {avg}\n'
                f'Курсы в процессе изучения: {courses_in_progress}\n'
                f'Завершённые курсы: {finished_courses}')

    def __lt__(self, other):
        if isinstance(other, Student):
            return self.get_average_grade() < other.get_average_grade()
        return (f'Ошибка')

    def __le__(self, other):
        if isinstance(other, Student):
            return self.get_average_grade() <= other.get_average_grade()
        return (f'Ошибка')

    def __eq__(self, other):
        if isinstance(other, Student):
            return self.get_average_grade() == other.get_average_grade()
        return (f'Ошибка')


# Задание 4: Полевые испытания
if __name__ == "__main__":
    # Создаём экземпляры
    # Студенты
    student1 = Student('Петрова', 'Ольга', 'Ж')
    student2 = Student('Иванов', 'Петр', 'М')
    student1.courses_in_progress += ['Python', 'Java']
    student1.finished_courses += ['Введение в программирование']
    student2.courses_in_progress += ['Python', 'C++']
    student2.finished_courses += ['Основы Python']

    # Лекторы
    lecturer1 = Lecturer('Иван', 'Иванов')
    lecturer2 = Lecturer('Сидорова', 'Мария')
    lecturer1.courses_attached += ['Python', 'C++']
    lecturer2.courses_attached += ['Java', 'Python']

    # Эксперты (рецензенты)
    reviewer1 = Reviewer('Пётр', 'Петров')
    reviewer2 = Reviewer('Ирина', 'Смирнова')
    reviewer1.courses_attached += ['Python', 'Java']
    reviewer2.courses_attached += ['Python', 'C++']

    # Выставляем оценки студентам
    reviewer1.rate_hw(student1, 'Python', 9)
    reviewer1.rate_hw(student1, 'Java', 8)
    reviewer2.rate_hw(student1, 'Python', 10)
    reviewer1.rate_hw(student2, 'Python', 7)
    reviewer2.rate_hw(student2, 'C++', 9)
    reviewer2.rate_hw(student2, 'Python', 8)

    # Студенты оценивают лекторов
    student1.rate_lecture(lecturer1, 'Python', 9)
    student1.rate_lecture(lecturer2, 'Java', 10)
    student2.rate_lecture(lecturer1, 'Python', 8)
    student2.rate_lecture(lecturer1, 'C++', 7)  # Ошибка: студент не на C++
    student2.rate_lecture(lecturer2, 'Python', 9)

    # Проверка Задания 1
    print("Задание 1:")
    print(isinstance(lecturer1, Mentor))  # True
    print(isinstance(reviewer1, Mentor))  # True
    print(lecturer1.courses_attached)     # ['Python', 'C++']
    print(reviewer1.courses_attached)     # ['Python', 'Java']
    print()

    # Проверка Задания 2
    print("Задание 2:")
    print(student1.rate_lecture(lecturer1, 'Python', 7))   # None
    print(student1.rate_lecture(lecturer1, 'Java', 8))     # Ошибка: не лектор по Java
    print(student1.rate_lecture(lecturer1, 'C++', 8))      # Ошибка: студент не на C++
    print(student1.rate_lecture(reviewer1, 'Python', 6))   # Ошибка: не лектор
    print(f"Оценки лектора1: {lecturer1.grades}")          # {'Python': [9, 8, 7]}
    print()

    # Проверка Задания 3: __str__
    print("Задание 3:")
    print(reviewer1)
    print()
    print(lecturer1)
    print()
    print(student1)
    print()

    # Сравнение
    print(f"lecturer1 < lecturer2: {lecturer1 < lecturer2}")
    print(f"student1 > student2: {student1 > student2}")
    print()

    # Задание 4: Функции подсчёта средней оценки по курсу
    def average_hw_grade_for_students(students, course):
        """Средняя оценка за ДЗ по всем студентам по курсу"""
        total = 0
        count = 0
        for student in students:
            if course in student.grades:
                total += sum(student.grades[course])
                count += len(student.grades[course])
        return round(total / count, 1) if count else 0

    def average_lecture_grade_for_lecturers(lecturers, course):
        """Средняя оценка за лекции по всем лекторам по курсу"""
        total = 0
        count = 0
        for lecturer in lecturers:
            if course in lecturer.grades:
                total += sum(lecturer.grades[course])
                count += len(lecturer.grades[course])
        return round(total / count, 1) if count else 0

    # Тест функций
    print("Задание 4:")
    print(f"Средняя оценка за ДЗ по Python: {average_hw_grade_for_students([student1, student2], 'Python')}")
    print(f"Средняя оценка за лекции по Python: {average_lecture_grade_for_lecturers([lecturer1, lecturer2], 'Python')}")