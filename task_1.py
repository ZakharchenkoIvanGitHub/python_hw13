"""Создайте класс студента.
Используя дескрипторы проверяйте ФИО на первую заглавную букву и наличие только букв.
Названия предметов должны загружаться из файла CSV при создании экземпляра. Другие предметы в экземпляре недопустимы.
Для каждого предмета можно хранить оценки (от 2 до 5) и результаты тестов (от 0 до 100).
Также экземпляр должен сообщать средний балл по тестам для каждого предмета и по оценкам всех предметов вместе взятых."""

import csv
from statistics import mean


class InputError(Exception):
    def __init__(self, value, message):
        self.value = value
        self.message = message

    def __str__(self):
        return f'Значение {self.value} {self.message}'


class ChangeError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class SubjectsError(Exception):
    def __init__(self, subject, name):
        self.subject = subject
        self.name = name

    def __str__(self):
        return f'Предмет {self.subject} отсутствует у студента {self.name}'


class EvaluationFormatError(Exception):
    def __init__(self, value, rating):
        self.value = value
        self.rating = rating

    def __str__(self):
        return f'Неверный формат {self.value} {self.rating}'


class ResultReturnError(Exception):
    def __init__(self, subject):
        self.subject = subject

    def __str__(self):
        return f'По предмету {self.subject} балы не начислялись'


class ValidName:
    def __set_name__(self, owner, name):
        self.param_name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.param_name)

    def __set__(self, instance, value):

        for n in value.split():

            if not n.isalpha():
                raise InputError(n, "должно содержать только буквы")
            elif not n.istitle():
                raise InputError(n, "должно начинаться с заглавной буквы")

        self.value = value

        setattr(instance, self.param_name, value)


class Student:
    name = ValidName()

    def __init__(self, name, subject_csv_file):
        self.name = name
        self._subjects = self._load_subjects(subject_csv_file)
        self.ratings = {}
        self.test_results = {}

    @staticmethod
    def _load_subjects(subject_csv_file):
        subject_name = []
        with open(subject_csv_file, 'r', encoding='utf8') as file:
            for line in csv.reader(file):
                subject_name.append(*line)
            return subject_name

    @property
    def subjects(self):
        return self._subjects

    @subjects.setter
    def subjects(self, value):
        raise ChangeError(f'Невозможно изменить список предметов')

    def add_rating(self, subject, rating):
        if subject not in self._subjects:
            raise SubjectsError(subject, self.name)
        if isinstance(rating, int) and 2 <= rating <= 5:
            self.ratings.setdefault(subject, [])
            self.ratings[subject].append(rating)

        else:
            raise EvaluationFormatError("оценки", rating)

    def add_test_result(self, subject, result):
        if subject not in self._subjects:
            raise SubjectsError(subject, self.name)
        if isinstance(result, int) and 0 <= result <= 100:
            self.test_results.setdefault(subject, [])
            self.test_results[subject].append(result)

        else:
            raise EvaluationFormatError("результата тестов", result)

    def get_average_ratings(self):
        all_ratings = []
        for key, value in self.ratings.items():
            all_ratings.extend(value)
        print(f"Средний бал студента по оценкам всех предметов вместе взятых {mean(all_ratings)}")

    def get_average_score_test_results(self, subject):
        if subject not in self._subjects:
            raise SubjectsError(subject, self.name)
        if subject in self.test_results:
            print(f"Средний бал студента по тестам предмета {subject} {mean(self.test_results[subject])}")
        else:
            raise ResultReturnError(subject)


student1 = Student("Иванов Иван Иванович", "subjects.csv")

try:
    student2 = Student("петров Иван Иванович", "subjects.csv")
except InputError as e:
    print(e)

try:
    student1.subjects = ["Химия"]
except ChangeError as e:
    print(e)

try:
    student1.add_rating("Химия", 5)
except SubjectsError as e:
    print(e)

try:
    student1.add_test_result("Химия", 50)
except SubjectsError as e:
    print(e)

try:
    student1.add_rating("Физика", "5")
except EvaluationFormatError as e:
    print(e)

try:
    student1.add_test_result("Физика", "50")
except EvaluationFormatError as e:
    print(e)

try:
    student1.get_average_score_test_results('География')
except ResultReturnError as e:
    print(e)
