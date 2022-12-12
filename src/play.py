from game import GameRunner


game_runner = GameRunner()

while not game_runner.finished:
    print("AI is playing..........")
    game_runner.aiplay()
    print(game_runner.state)
    player_move = (-1, -1)
    x, y = map(int, input("Please enter the desired position").split())
    while not game_runner.play(x, y):
        print("Plese enter a valid move")
        x, y = map(int, input("Please enter the desired position").split())
    print(game_runner.state)
winner = game_runner.state.winner
if winner == 1:
    print("1 win")
else:
    print("0 win or draw")
