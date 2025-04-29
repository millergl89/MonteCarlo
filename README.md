# MonteCarlo


## Metadata
- **Name:** Greg Miller
- **Project Name:** MonteCarlo

## Synopsis

    Creating Dice
        To create a die, instantiate the Die class with a NumPy array of unique face values. Optionally, you can change the weight of a specific face.

    import numpy as np
    from die import Die

# Create a die with 3 faces: 'A', 'B', 'C'
faces = np.array(['A', 'B', 'C'])
die = Die(faces)


# Optionally change the weight of face 'A'
die.change_weight('A', 3.5)
Playing a Game
To play a game, instantiate the Game class with a list of Die objects. Then, use the play method to roll the dice a specified number of times.


from game import Game

# Create two dice
die1 = Die(faces)
die2 = Die(faces)

# Create a game with these dice
game = Game([die1, die2])

# Roll the dice 10 times
game.play(10)

# Show the results in wide format
print(game.show(form='wide'))
Analyzing the Game
Use the Analyzer class to analyze the results of the game. The Analyzer provides methods to find jackpots, count face occurrences per roll, and more.


from analyzer import Analyzer

# Create an Analyzer for the game
analyzer = Analyzer(game)

# Get the number of jackpots
print(analyzer.jackpot())

# Get the face counts per roll
print(analyzer.face_counts_per_roll())

### Installation

To install the simulator, simply clone the repository and ensure you have the required dependencies:

```bash
git clone <https://github.com/millergl89/MonteCarlo>
cd <project_folder>
pip install -r requirements.txt
```


## API Description

    Die Class
        Methods:
            __init__(self, faces: np.ndarray): Initializes the die with a NumPy array of faces.
                Parameters:
                    faces: A NumPy array containing the unique face values of the die.

            change_weight(self, face: str, new_weight: float): Changes the weight of a given face.
                Parameters:
                    face: The face whose weight is to be changed.
                    new_weight: The new weight for the specified face (should be numeric).

            roll(self, times: int = 1): Rolls the die a specified number of times.
                Parameters:
                    times: The number of times to roll the die (default is 1).
                Returns:
                    A list of the outcomes (faces rolled).

            show(self): Shows the current state of the die (faces and weights).
                Returns:
                    A pandas DataFrame showing the faces and their weights.

    Game Class
        Methods:

            __init__(self, dice_list: list): Initializes the game with a list of Die objects.
                Parameters:
                    dice_list: A list of Die objects.

            play(self, num_rolls: int): Rolls all the dice a specified number of times and stores the result.
                Parameters:
                    num_rolls: The number of times to roll each die.
                Updates:
                    Stores the results in a private DataFrame.

            show(self, form='wide'): Displays the results of the most recent play.
                Parameters:
                    form: A string specifying the format of the results ('wide' or 'narrow', default is 'wide').
                Returns:
                    A pandas DataFrame of the results in the specified format.


    Analyzer Class
        Methods:

            __init__(self, game: Game): Initializes the analyzer with a Game object.
                Parameters:
                    game: The Game object whose results will be analyzed.

            jackpot(self): Finds how many times all faces rolled in the game were the same (a jackpot).
                Returns:
                    An integer representing the number of jackpots.

            face_counts_per_roll(self): Counts the occurrences of each face on every roll.
                Returns:
                    A pandas DataFrame with face counts per roll.

            combo_count(self): Counts the distinct combinations of faces rolled across all rolls.
                Returns:
                    A pandas DataFrame with distinct combinations and their counts.

            permutation_count(self): Counts the distinct permutations of faces rolled across all rolls.
                Returns:
                    A pandas DataFrame with distinct permutations and their counts.