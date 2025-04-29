import unittest
import numpy as np
import pandas as pd
from montecarlo.MonteCarlo import Die, Game, Analyzer

class TestDie(unittest.TestCase):

    def setUp(self):
        self.faces = np.array(['A', 'B', 'C'])
        self.die = Die(self.faces)

    def test_change_weight(self):
        self.die.change_weight('A', 3.5)
        df = self.die.show()
        self.assertEqual(df.loc['A', 'weight'], 3.5)

    def test_roll(self):
        result = self.die.roll(5)
        self.assertEqual(len(result), 5)
        self.assertTrue(all(face in self.faces for face in result))

    def test_show(self):
        df = self.die.show()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertListEqual(list(df.columns), ['weight'])

class TestGame(unittest.TestCase):

    def setUp(self):
        faces = np.array([1, 2, 3])
        self.die1 = Die(faces)
        self.die2 = Die(faces)
        self.game = Game([self.die1, self.die2])
        self.game.play(10)

    def test_play(self):
        df = self.game.show()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape[0], 10)
        self.assertEqual(df.shape[1], 2)

    def test_show_wide(self):
        wide_df = self.game.show(form='wide')
        self.assertIsInstance(wide_df, pd.DataFrame)
        self.assertEqual(wide_df.shape[0], 10)

    def test_show_narrow(self):
        narrow_df = self.game.show(form='narrow')
        self.assertIsInstance(narrow_df, pd.DataFrame)
        self.assertEqual(narrow_df.index.names, ['Roll', 'Die'])
        self.assertIn('Outcome', narrow_df.columns)

class TestAnalyzer(unittest.TestCase):

    def setUp(self):
        faces = np.array([1, 2, 3])
        die1 = Die(faces)
        die2 = Die(faces)
        game = Game([die1, die2])
        game.play(10)
        self.analyzer = Analyzer(game)

    def test_jackpot(self):
        result = self.analyzer.jackpot()
        self.assertIsInstance(result, int)

    def test_face_counts_per_roll(self):
        df = self.analyzer.face_counts_per_roll()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.shape[0], 10)

    def test_combo_count(self):
        df = self.analyzer.combo_count()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn('Count', df.columns)

    def test_permutation_count(self):
        df = self.analyzer.permutation_count()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn('Count', df.columns)

if __name__ == '__main__':
    unittest.main()
