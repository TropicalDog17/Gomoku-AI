from game import GameRunner
import string
import piece
from rich.console import Console

if __name__ == "__main__":
    console = Console()
    alphabet = list(string.ascii_uppercase)
    print("Player move will consist 2 uppercase letter, representing the position of a cell(e.g: FJ)")
    console.print("Choose who to play first (A/H): ", style="bold red")
    move_first = input()
    if move_first == "H":
        game_runner = GameRunner()
        while not game_runner.finished:
            console.print(game_runner.state.get_table())
            while True:
                if game_runner.finished:
                    break
                console.print("Your move: ", style="blue", end="")
                move = input()
                x, y = alphabet.index(move[0]), alphabet.index(move[1])
                if not game_runner.play(x, y):
                    console.print("[red]Invalid position! Try again!!!![/red]")
                    console.print(game_runner.state.get_table())
                    continue
                console.print(game_runner.state.get_table())
                console.print("AI is playing..........", style="yellow")
                game_runner.aiplay()
                console.print(game_runner.state.get_table())
    elif move_first == "A":
        game_runner = GameRunner(color=piece.WHITE)
        while not game_runner.finished:

            while True:

                console.print("AI is playing..........", style="yellow")
                game_runner.aiplay()
                console.print(game_runner.state.get_table())
                if game_runner.finished:
                    break
                console.print("Your move: ", style="blue", end="")
                move = input()
                x, y = alphabet.index(move[0]), alphabet.index(move[1])
                while not game_runner.play(x, y):
                    console.print("[red]Invalid position! Try again!!!![/red]")
                    console.print("Your move: ", style="blue", end="")
                    move = input()
                    x, y = alphabet.index(move[0]), alphabet.index(move[1])
                    console.print(game_runner.state.get_table())
                    continue
                console.print(game_runner.state.get_table())

    winner = game_runner.state.winner
    if winner == 1:
        print("X win")
    elif winner == -1:
        print("O win")
    else:
        print("Draw")
