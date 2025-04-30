import unittest
import numpy as np
import pandas as pd
from montecarlo.MonteCarlo import Die, Game, Analyzer

class TestDie(unittest.TestCase):


    def test_init_non_array_faces(self):
        with self.assertRaises(TypeError):
            Die(['H', 'T'])

    def test_change_weight(self):
        die = Die(np.array(['A', 'B']))
        die.change_weight('A', 2.0)
        self.assertEqual(die.show().loc['A', 'weight'], 2.0)

    def test_roll(self):
        die = Die(np.array(['A', 'B']))
        rolls = die.roll(5)
        self.assertEqual(len(rolls), 5)
        self.assertTrue(all(r in ['A', 'B'] for r in rolls))

    def test_show(self):
        die = Die(np.array(['A', 'B']))
        df = die.show()
        self.assertIsInstance(df, pd.DataFrame)


class TestGame(unittest.TestCase):

    def test_init_valid_dice(self):
        die1 = Die(np.array(['A', 'B']))
        die2 = Die(np.array(['A', 'B']))
        game = Game([die1, die2])
        self.assertEqual(len(game.dice), 2)
        self.assertIsNone(game._play_df)

    def test_play(self):
        die = Die(np.array(['X', 'Y']))
        game = Game([die, die])
        game.play(3)
        # Check the shape of the result after playing
        self.assertEqual(game._play_df.shape, (3, 2))  # 3 rolls and 2 dice

    def test_show(self):
        die = Die(np.array(['X', 'Y']))
        game = Game([die, die])
        game.play(3)
        df = game.show()
        # Ensure the show method works correctly
        self.assertEqual(df.shape, (3, 2))  # The same shape as the play result
        self.assertIsInstance(df, pd.DataFrame)


class TestAnalyzer(unittest.TestCase):

    def test_init_valid_game(self):
        die = Die(np.array(['A', 'B']))
        game = Game([die, die])
        game.play(3)
        analyzer = Analyzer(game)
        self.assertTrue(isinstance(analyzer.results, pd.DataFrame))
        self.assertEqual(analyzer.results.shape[0], 3)

    def test_jackpot(self):
        die = Die(np.array(['A', 'B']))  # Valid unique faces
        game = Game([die, die])
        game.play(5)
        analyzer = Analyzer(game)
        result = analyzer.jackpot()
        self.assertIsInstance(result, (int, np.integer))
        self.assertGreaterEqual(result, 0)

    def test_face_counts_per_roll(self):
        die = Die(np.array(['1', '2']))
        game = Game([die, die])
        game.play(5)
        analyzer = Analyzer(game)
        counts = analyzer.face_counts_per_roll()
        self.assertEqual(counts.shape[0], 5)

    def test_combo_count(self):
        die = Die(np.array(['1', '2']))
        game = Game([die, die])
        game.play(5)
        analyzer = Analyzer(game)
        combos = analyzer.combo_count()
        self.assertTrue(isinstance(combos, pd.DataFrame))
        self.assertGreater(len(combos), 0)  # Ensure that combinations are found

    def test_permutation_count(self):
        die = Die(np.array(['1', '2']))
        game = Game([die, die])
        game.play(5)
        analyzer = Analyzer(game)
        perms = analyzer.permutation_count()
        self.assertTrue(isinstance(perms, pd.DataFrame))
        self.assertGreater(len(perms), 0)  # Ensure that permutations are found

if __name__ == '__main__':
    unittest.main()
