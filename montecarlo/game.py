import pandas as pd

class Game:
"""
A game consists of rolling one or more similar Die objects one or more times.

Dice in a game must have the same faces, but may have different weights.

Attributes
    dice_list : list
        List of Die objects used in the game.
    _play_df : pandas.DataFrame or None
        Private dataframe storing the most recent game play results.
Methods
    play(num_rolls):
        Roll all dice a given number of times and store the result.
    show(form='wide'):
        Show the results of the most recent play in wide or narrow format.
"""

    def __init__(self, dice_list):
        self.dice = dice_list
        self._play_df = None

    def play(self, num_rolls):
    """
    Roll all dice a specified number of times.

    Parameters
        num_rolls : int
            Number of times to roll each die.
    Updates
        self._play_df : pandas.DataFrame
            Stores results of the play in wide format.
    """
        results = {}
        for i, die in enumerate(self.dice):
            rolls = die.roll(num_rolls)
            results[i] = rolls

        self._play_df = pd.DataFrame(results)
        self._play_df.index.name = 'Roll'

    def show(self, form='wide'):
    """
    Show the result of the most recent play.

    Parameters
        form : str, optional
            'wide' (default) returns wide format with roll numbers as index.
            'narrow' returns a MultiIndex with roll and die number.
    Returns
        pandas.DataFrame
            Copy of the results dataframe in the specified format.
    """
        if self._play_df is None:
            raise ValueError("No game has been played yet.")

        if form == 'wide':
            return self._play_df.copy()

        elif form == 'narrow':
            narrow_df = self._play_df.stack()
            narrow_df.index.set_names(['Roll', 'Die'], inplace=True)
            narrow_df.name = 'Outcome'
            return narrow_df.to_frame()

        else:
            raise ValueError("Invalid form. Use 'wide' or 'narrow'.")
