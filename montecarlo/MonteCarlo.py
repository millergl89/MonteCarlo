import numpy as np
import pandas as pd

class Die:
    """
    A die has N sides, or “faces”, and W weights, and can be rolled to select a face.

    Each face contains a unique symbol (either all strings or all numbers). Weights default to 1.0 but can be changed.

    Attributes
        __df : pandas.DataFrame
            A private dataframe indexed by face, with a column for the weight.

    Methods
        change_weight(face, new_weight):
            Change the weight of a single face after initialization.
        
        roll(times=1):
            Roll the die one or more times.

        show():
            Return a copy of the die’s current state.
    """

    def __init__(self, faces):
        """
        Initialize the Die with a NumPy array of unique faces.

        Parameters
            faces : numpy.ndarray
                Array of face symbols (must be unique and of a consistent type).
        """
        if not isinstance(faces, np.ndarray):
            raise TypeError("Faces must be a NumPy array.")
        if len(np.unique(faces)) != len(faces):
            raise ValueError("All face values must be unique.")

        self.__df = pd.DataFrame({
            'weight': np.ones(len(faces), dtype=float)
        }, index=faces)

    def change_weight(self, face, new_weight):
        """
        Change the weight of a single face.

        Parameters
            face : object
                The face value whose weight is to be changed.
            new_weight : float or int
                The new weight to assign. Must be numeric.
        """
        if face not in self.__df.index:
            raise IndexError("Not a valid face.")
        try:
            new_weight = float(new_weight)
        except (ValueError, TypeError):
            raise TypeError("Weight must be numeric.")
        self.__df.loc[face, 'weight'] = new_weight

    def roll(self, times=1):
        """
        Roll the die one or more times.

        Parameters
            times : int, optional
                The number of times to roll the die. Default is 1.

        Returns
            list
                List of outcomes from rolling the die.
        """
        faces = self.__df.index.to_numpy()
        weights = self.__df['weight'].to_numpy()
        rolls = np.random.choice(faces, size=times, replace=True, p=weights / weights.sum())
        return rolls.tolist()

    def show(self):
        """
        Show the current state of the die.

        Returns
            pandas.DataFrame
                A copy of the internal dataframe showing faces and weights.
        """
        return self.__df.copy()


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

        Returns
            perm_counts - pandas.DataFrame
                A dataframe with MultiIndex of permutations and counts.
        """
        perms = self.results.apply(lambda row: tuple(row), axis=1)
        perm_counts = perms.value_counts().to_frame(name='Count')
        perm_counts.index.name = 'Permutation'
        return perm_counts