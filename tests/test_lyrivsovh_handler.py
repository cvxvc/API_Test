import unittest

from lyricsovh_handler import LyricsOvhHandler


class TestLyricsOvhHandler(unittest.TestCase):
    """
    Class which tests functions in the LyricsOvhHandler class
    """

    def test_find_number_of_words_in_song(self):
        # Arrange
        test_1 = ['Metallica', 'For whom the bell tolls']      # An actual song
        test_2 = ['fjdoisjfdios', 'For whom the bell tolls']   # Invalid artist
        test_3 = ['Metallica', 'jfioewjfoiew']                 # Invalid song
        test_4 = ['Metallica', 'Orion']                        # An instrumental

        # Act
        results = [LyricsOvhHandler.find_number_of_words_in_song(case[0], case[1])
                   for case in [test_1, test_2, test_3, test_4]]

        # Assert
        expected_results = [163, None, None, 0]

        self.assertEqual(results, expected_results)
