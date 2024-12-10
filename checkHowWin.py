# файл для проверки ПОБЕДИЛ\ПРОИГРАЛ
# словарь формата победитель:проигравший
combos = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper",
    "axe": "paper",
    "picaxe": "rock"
}


def check(my_card, en_card):  # функция по проверке выигроша
    if combos[my_card] == en_card:
        return True
    else:
        return False
