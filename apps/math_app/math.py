def math_sum(left, right):
    return left+right


def math_sub(left, right):
    return left - right


def math_mult(left, right):
    return left * right


def math_div(left, right):
    if right == 0:
        return "Divisão não definida em denominador = 0"
    return left / right


def math_pow(left, right):
    return left ** right


def math_root(left, right):
    if left < 0 and right % 2 == 0:
        return "Raíz indefinida nos reais para left < 0 and right even"
    return left ** (1 / right)


def math_factorial(num: int) -> int:
    return math_factorial(num - 1) * num if num > 1 else num


def math_square_func(a, b, c):
    delta = b ** 2 - 4 * a * c
    if delta < 0:
        return "Não existem raizes reais para delta < 0"
    elif delta == 0:
        return -b/(2*a)
    return (-b - delta ** (1 / 2)) / 2 * a, (-b + delta ** (1 / 2)) / 2 * a
