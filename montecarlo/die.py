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
