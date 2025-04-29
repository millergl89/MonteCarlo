import pandas as pd

class Analyzer:
"""
Analyzer class to compute descriptive statistical properties of a Game object.

Attributes
    game : Game
        The Game object to analyze.
        
    results : pandas.DataFrame
        A copy of the game's most recent play results in wide format.
Methods
    jackpot():
        Count how many times all dice had the same face value.

    face_counts_per_roll():
        Count the number of times each face appeared per roll.

    combo_count():
        Count occurrences of unique combinations of face values (order-independent).

    permutation_count():
        Count occurrences of unique permutations of face values (order-dependent).
    """

    def __init__(self, game):
    """
    Initialize the Analyzer with a Game object.

    Parameters
        game : Game
            The Game object to analyze.
    """
        if not isinstance(game, Game):
            raise ValueError("Input must be a Game object.")

        self.game = game
        self.results = self.game.show(form='wide').copy()

    def jackpot(self):
    """
    Count how many times the roll resulted in all dice showing the same face.

    Returns
        int
            Number of jackpot outcomes (all dice in a roll show the same face).
    """
        return (self.results.nunique(axis=1) == 1).sum()

    def face_counts_per_roll(self):
    """
    Count the number of times each face appeared in each roll.

    Returns
        counts - pandas.DataFrame
            A dataframe with roll numbers as index and face counts as columns.
            Missing face counts are filled with 0.
    """
        counts = self.results.apply(lambda row: row.value_counts(), axis=1)
        return counts.fillna(0).astype(int)

    def combo_count(self):
    """
    Count unique combinations of rolled faces (order-independent).

    Returns
        combo_counts - pandas.DataFrame
            A dataframe with MultiIndex of combinations and counts.
    """
        combos = self.results.apply(lambda row: tuple(sorted(row)), axis=1)
        combo_counts = combos.value_counts().to_frame(name='Count')
        combo_counts.index.name = 'Combination'
        return combo_counts

    def permutation_count(self):
    """
    Count unique permutations of rolled faces (order-dependent).

    Returns - perm_counts
        pandas.DataFrame
            A dataframe with MultiIndex of permutations and counts.
    """
        perms = self.results.apply(lambda row: tuple(row), axis=1)
        perm_counts = perms.value_counts().to_frame(name='Count')
        perm_counts.index.name = 'Permutation'
        return perm_counts