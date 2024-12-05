import random


def check_answer(input_answer: int, correct_answer: int) -> int:
    """
    Used to check whether user's input was correct
    :param input_answer:
    :param correct_answer:
    :return: 0 if correct, 1 if greater than correct answer, -1 if lesser than correct answer
    """
    if input_answer == correct_answer:
        return 0
    if input_answer > correct_answer:
        return 1
    if input_answer < correct_answer:
        return -1


def generate_random_number():
    """
    Used to generate a random number
    :return: an int number between 1-100
    """
    return random.randrange(1, 100)



def get_input_or_quit(prompt: str):
    """
    Ask user for input, special handling in the case user type quit, in which case program will exit
    :param prompt: string to query user with
    :return: input from user
    """
    res = input(prompt)
    if res == 'quit':
        exit(0)
    else:
        return res


def show_scoreboard(scores: list):
    """
    To show to the user how many tries it took
    :param scores: a list of int
    :return: None
    """
    print("\nScore".upper())
    for i, score in enumerate(scores):
        print(f"round {i + 1}: {score} tries")
    print()


def play_game_round() -> int:
    """
    Individual round of the game
    :return: number of tries user took for win
    """
    number = generate_random_number()
    tries = 0
    while tries < 8:
        user_input = int(get_input_or_quit("Guess the number, between 1 to 100. You have 8 tries: "))
        result = check_answer(user_input, number)
        if result == 0:
            print("Congratulations, your answer is correct")
            break
        if result > 0:
            print("Sorry, your guess was too high")
        if result < 0:
            print("Sorry, your guess was too low")
        tries += 1
    return tries + 1 # increment by one because 0 tries makes no sense


def game_loop():
    """
    Main game loop
    :return: None
    """
    scores = []
    new_round = "yes"
    while new_round != "n":
        round_score = play_game_round()
        scores.append(round_score)
        show_scoreboard(scores)
        new_round = get_input_or_quit("Would you like to play another round? [y, n]? ")
    return None


def main():
    print("Welcome to number guessing game.")
    print("You can quit at any time by writing 'quit' ")
    game_loop()
    return None


if __name__ == "__main__":
    main()
