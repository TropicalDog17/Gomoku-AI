from game import GameRunner
import string
import piece
if __name__ == "__main__":
    alphabet = list(string.ascii_uppercase)
    print("Player move will consist 2 uppercase letter, representing the position of a cell(e.g: FJ)")
    move_first = input("Choose first move(A/H)<A for AI, H for Human>: ")
    if move_first == "H":
        game_runner = GameRunner()
        while not game_runner.finished:
            # print("AI is playing..........")
            # game_runner.aiplay()
            print(game_runner.state)
            while True:
                if game_runner.finished:
                    break
                move = input("Your move: ")
                x, y = alphabet.index(move[0]), alphabet.index(move[1])
                if not game_runner.play(x, y):
                    print("Invalid position")
                    print(game_runner.state)
                    continue
                print(game_runner.state)
                print("AI is thinking....")
                game_runner.aiplay()
                print(game_runner.state)
    elif move_first == "A":
        game_runner = GameRunner(color=piece.WHITE)
        while not game_runner.finished:

            while True:

                print("AI is playing..........")
                game_runner.aiplay()
                print(game_runner.state)
                if game_runner.finished:
                    break
                move = input("Your move: ")
                x, y = alphabet.index(move[0]), alphabet.index(move[1])
                while not game_runner.play(x, y):
                    print("Invalid position")
                    move = input("Your move: ")
                    x, y = alphabet.index(move[0]), alphabet.index(move[1])
                    print(game_runner.state)
                    continue
                print(game_runner.state)

    winner = game_runner.state.winner
    if winner == 1:
        print("X win")
    elif winner == -1:
        print("O win")
    else:
        print("Draw")
