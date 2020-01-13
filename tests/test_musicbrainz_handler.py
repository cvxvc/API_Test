import unittest

from musicbrainz_handler import MusicBrainzHandler


class TestMusicBrainzHandler(unittest.TestCase):
    """
    Class which tests functions in the MusicBrainzHandler class
    """

    def test_get_artist_id_from_artist_name(self):
        # Arrange
        artists = ['Metallica',
                   'queen',
                   'the Doors']

        fake_artist = 'nuiofiuohfiuoerwhufrie'  # Artist which should raise an error when searching for ID

        # Act
        results = [MusicBrainzHandler.get_artist_id_from_artist_name(name)
                   for name in artists]

        # Assert
        expected_results = ['65f4f0c5-ef9e-490c-aee3-909e7ae6b2ab',
                            '0383dadf-2a4e-4d10-a46a-e9e041da8eb3',
                            '9efff43b-3b29-4082-824e-bc82f646f93d']  # These IDs are pulled directly from the website

        self.assertEqual(results, expected_results)
        self.assertRaises(ValueError, MusicBrainzHandler.get_artist_id_from_artist_name, fake_artist)

    def test_get_artist_songs_from_artist_id(self):
        # Arrange
        queen_artist_id = '0383dadf-2a4e-4d10-a46a-e9e041da8eb3'  # Use queen since number of songs won't change

        # Act
        results = MusicBrainzHandler.get_artist_songs_from_artist_id(queen_artist_id)

        # Assert
        expected_song_list_length = 225

        self.assertEqual(len(results), expected_song_list_length)
