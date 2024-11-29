combos = {
    "rock" : "paper",
    "paper" : "scissors",
    "scissors" : "rock"
}


def check(my_card, en_card):
    if combos[my_card] == en_card:
        return False
    elif combos[en_card] == my_card:
        return True
    else:
        return 0