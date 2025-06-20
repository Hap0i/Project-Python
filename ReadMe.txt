# Выполнил: Булатов Антон, ИКНТ, ИТ-6, 1 курс
# Ссылка на github: https://github.com/Hap0i/Project-Python.git

# Программа для работы с деревом математических выражений

# Описание
Программа строит дерево математических выражений, вычисляет их значения и выполняет алгебраические упрощения. Поддерживаются операции `+`, `-`, `*`, `/`, унарный минус, скобки и однобуквенные переменные.

# Поставленная задача
Разработать программу для:
1. Построения дерева математических выражений из инфиксной записи
2. Вычисления значений с подстановкой переменных
3. Алгебраического упрощения выражений по заданным шаблонам
4. Обработки ошибок ввода и вычислений

# Структура данных
Выбрано бинарное дерево потому что:
- Натурально отражает структуру математических выражений
- Каждый оператор имеет ровно два операнда (бинарные операции)
- Рекурсивная природа дерева упрощает обход и преобразования
- Позволяет наглядно представить приоритет операций

# ООП в проекте
Классы:
1. TreeNode:
Инкапсуляция данных узла (value, left, right)
Метод str для строкового представления

2. ExpressionTree:
Инкапсуляция корня дерева
Полиморфизм: методы build_from_infix/to_expression работают с разными форматами

3. FormulaProcessor:
Композиция: содержит экземпляр ExpressionTree
Инкапсуляция переменных (словарь variables)

# Принципы ООП:
1. Инкапсуляция:
Скрытие внутренней реализации (например, стека в postfix-преобразовании)
Доступ к данным только через методы

2. Полиморфизм:
Метод evaluate() работает с разными типами узлов (операторы/операнды)
Единый интерфейс для работы с деревом

3. Наследование не используется, так как:
Нет естественной иерархии классов
Все узлы однотипны (нет специализированных подклассов)

# Требования
- ЯП: Python
- Установленные пакеты: не требуются

# Установка
1. Скопируйте файлы проекта в любую папку на вашем компьютере
2. Убедитесь, что у вас установлен Python 3

## Использование
1. Ввести формулу
2. Задать значения переменных
3. Вычислить формулу
4. Упростить формулу
5. Выход

Пример работы:
1. Выберите пункт 1 и введите формулу, например: a*b + a*c
2. Выберите пункт 2 и задайте значения переменных, например: a=2 b=3 c=4
3. Выберите пункт 3 для вычисления результата (выведет 14)
4. Выберите пункт 4 для упрощения формулы (выведет a * (b + c))
5. Выберите пункт 5 для выхода из программы

# Особенности реализации
Построение дерева выражений через алгоритм сортировочной станции
Поддержка унарного минуса
Автоматическое упрощение выражений по шаблонам:

(f1*f3 ± f2*f3) → (f1 ± f2)*f3
(f1*f2 ± f1*f3) → f1*(f2 ± f3)

# Обработка ошибок
Программа обнаруживает и сообщает о:

Несбалансированных скобках
Неопределенных переменных
Делении на ноль
Некорректных символах в формуле
