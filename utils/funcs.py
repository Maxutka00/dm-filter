import random


def math_question_gen():
    num1 = random.randint(1, 20)
    num2 = random.randint(20, 50)
    return f"{num1} + {num2}", str(num1 + num2)


def less_than_100(text: str):
    if not text.isdigit():
        return False
    if int(text) < 100:
        return True
    else:
        return False


def bigger_than_1000(text: str):
    if not text.isdigit():
        return False
    if int(text) >= 1000:
        return True
    else:
        return False


def less_than_1000(text: str):
    if not text.isdigit():
        return False
    if int(text) < 1000:
        return True
    else:
        return False


def bigger_than_100(text: str):
    if not text.isdigit():
        return False
    if int(text) >= 100:
        return True
    else:
        return False
