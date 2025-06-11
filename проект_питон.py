class TreeNode:   # Класс узла дерева выражений
    def __init__(self, value):
        self.value = value  # Значение узла (число, переменная или оператор)
        self.left = None
        self.right = None
    

    def __str__(self):
        return str(self.value)


class ExpressionTree:   # Класс для работы с деревом выражений
    def __init__(self):
        self.root = None  # Корень дерева


    def build_from_infix(self, expression):   # Построение дерева из инфиксной записи
        tokens = self.tokenize(expression)
        postfix = self.infix_to_postfix(tokens)
        self.root = self.build_tree(postfix)
        return self.root


    def tokenize(self, expression):    # Разбиение выражения на токены
        tokens = []
        i = 0
        n = len(expression)
        
        while i < n:
            if expression[i] == ' ':
                i += 1
                continue
            
            if expression[i] in '()+-*/':
                # Обработка унарного минуса
                if expression[i] == '-' and (not tokens or tokens[-1] == '(' or tokens[-1] in '+-*/'):
                    tokens.append('u-')  # Специальный маркер для унарного минуса
                    i += 1
                else:
                    tokens.append(expression[i])
                    i += 1
            elif expression[i].isdigit():
                j = i
                while j < n and expression[j].isdigit():
                    j += 1
                tokens.append(expression[i:j])
                i = j
            elif expression[i].isalpha():
                tokens.append(expression[i])
                i += 1
            else:
                raise ValueError(f"Недопустимый символ: {expression[i]}")
        
        return tokens


    def infix_to_postfix(self, tokens):   # Преобразование инфиксной записи в постфиксную
        output = []
        stack = []
        precedence = {'+': 1, '-': 1, '*': 2, '/': 2, 'u-': 3}
        
        for token in tokens:
            if token.isdigit() or token.isalpha():
                output.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()  # Удаляем '('
            else:  # оператор или унарный минус
                while (stack and stack[-1] != '(' and
                       precedence.get(stack[-1], 0) >= precedence.get(token, 0)):
                    output.append(stack.pop())
                stack.append(token)
        
        while stack:
            output.append(stack.pop())
        return output


    def build_tree(self, postfix):   # Построение дерева из постфиксной записи
        stack = []
        
        for token in postfix:
            if token in '+-*/':
                node = TreeNode(token)
                node.right = stack.pop()
                node.left = stack.pop()
                stack.append(node)
            elif token == 'u-':
                node = TreeNode('-')
                node.right = stack.pop()
                stack.append(node)
            else:
                stack.append(TreeNode(token))
        
        if not stack:
            raise ValueError("Неверное выражение")
        return stack[0]


    def to_expression(self, node=None):   # Преобразование дерева обратно в строку
        if node is None:
            node = self.root
        
        if not node:
            return ""
        
        if not node.left and not node.right:
            return str(node.value)
        
        left_str = self.to_expression(node.left)
        right_str = self.to_expression(node.right)
        
        # Добавляем скобки по приоритетам
        if node.left and node.left.value in '+-*/' and self.get_precedence(node.left.value) < self.get_precedence(node.value):
            left_str = f"({left_str})"
        if node.right and node.right.value in '+-*/' and self.get_precedence(node.right.value) <= self.get_precedence(node.value):
            right_str = f"({right_str})"
        
        return f"{left_str} {node.value} {right_str}"


    def get_precedence(self, op):   # Получение приоритета оператора
        if op in '*/':
            return 2
        elif op in '+-':
            return 1
        return 0


class FormulaProcessor:   # Класс для вычисления и упрощения формул
    def __init__(self):
        self.tree = ExpressionTree()
        self.variables = {}


    def set_formula(self, expression):   # Установка формулы
        self.tree.build_from_infix(expression)


    def set_variable(self, name, value):   # Установка значения переменной
        self.variables[name] = value


    def evaluate(self, node=None):   # Вычисление значения формулы
        if node is None:
            node = self.tree.root
            if node is None:
                raise ValueError("Формула не задана")
        
        if node.value.isdigit():
            return int(node.value)
        elif node.value.startswith('-') and node.value[1:].isdigit():
            return -int(node.value[1:])
        elif node.value.isalpha():
            if node.value not in self.variables:
                raise ValueError(f"Неопределённая переменная: {node.value}")
            return self.variables[node.value]
        
        left_val = self.evaluate(node.left) if node.left else 0
        right_val = self.evaluate(node.right) if node.right else 0
        
        if node.value == '+':
            return left_val + right_val
        elif node.value == '-':
            return left_val - right_val
        elif node.value == '*':
            return left_val * right_val
        elif node.value == '/':
            if right_val == 0:
                raise ValueError("Деление на ноль")
            return left_val / right_val
        else:
            raise ValueError(f"Неизвестный оператор: {node.value}")


    def simplify(self):   # Упрощение формулы
        if self.tree.root is None:
            raise ValueError("Формула не задана")
        self.tree.root = self.simplify_node(self.tree.root)
        return self.tree.to_expression()


    def simplify_node(self, node):   # Рекурсивное упрощение узла
        if not node:
            return node
        
        node.left = self.simplify_node(node.left)
        node.right = self.simplify_node(node.right)
        
        if node.value in '+-':
            node = self.try_simplify_pattern(node)
        
        return node


    def try_simplify_pattern(self, node):   # Попытка упрощения по заданным шаблонам
        left = node.left
        right = node.right
        
        if left and left.value == '*' and right and right.value == '*':
            # Шаблоны: (f1*f3 +- f2*f3) -> (f1 +- f2)*f3
            #          (f1*f2 +- f1*f3) -> f1*(f2 +- f3)
            ll, lr = left.left, left.right
            rl, rr = right.left, right.right
            
            # Проверяем 4 возможных варианта совпадения множителей
            for case in [(lr, rr), (ll, rl), (ll, rr), (lr, rl)]:
                if self.is_equal_trees(*case):
                    a, b = case
                    new_node = TreeNode('*')
                    if a == lr and b == rr:  # (f1*f3 +- f2*f3)
                        new_left = TreeNode(node.value)
                        new_left.left = ll
                        new_left.right = rl
                        new_node.left = new_left
                        new_node.right = lr
                    elif a == ll and b == rl:  # (f1*f2 +- f1*f3)
                        new_right = TreeNode(node.value)
                        new_right.left = lr
                        new_right.right = rr
                        new_node.left = ll
                        new_node.right = new_right
                    return new_node
        return node


    def is_equal_trees(self, tree1, tree2):   # Проверка равенства двух поддеревьев
        if not tree1 and not tree2:
            return True
        if not tree1 or not tree2:
            return False
        return (tree1.value == tree2.value and 
                self.is_equal_trees(tree1.left, tree2.left) and 
                self.is_equal_trees(tree1.right, tree2.right))


def main():   # Основная функция программы
    print("Программа для работы с формулами")
    processor = FormulaProcessor()
    
    while True:
        print("\nМеню:")
        print("1. Ввести формулу")
        print("2. Задать значения переменных")
        print("3. Вычислить формулу")
        print("4. Упростить формулу")
        print("5. Выход")
        
        choice = input("Выберите действие: ").strip()
        
        if choice == '1':
            try:
                expr = input("Введите формулу: ").strip()
                processor.set_formula(expr)
                print("Формула успешно разобрана.")
            except Exception as e:
                print(f"Ошибка: {e}")
        
        elif choice == '2':
            try:
                var_input = input("Введите переменные (например, a=5 b=10): ").strip()
                if var_input:
                    for part in var_input.split():
                        name, value = part.split('=')
                        processor.set_variable(name, int(value))
                print("Значения переменных:", processor.variables)
            except Exception as e:
                print(f"Ошибка: {e}")
        
        elif choice == '3':
            try:
                result = processor.evaluate()
                print(f"Результат: {result}")
            except Exception as e:
                print(f"Ошибка вычисления: {e}")
        
        elif choice == '4':
            try:
                simplified = processor.simplify()
                print(f"Упрощенная формула: {simplified}")
            except Exception as e:
                print(f"Ошибка упрощения: {e}")
        
        elif choice == '5':
            print("Выход")
            break
        
        else:
            print("Неверный ввод, выберете действие от 1-5")


if __name__ == "__main__":
    main()