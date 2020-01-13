import re
import requests

from json import JSONDecodeError


class LyricsOvhHandler:
    """
    A class containing helper functions for interacting with the lyrics.ovh API
    """

    @staticmethod
    def find_number_of_words_in_song(artist_name, song_name):
        """
        Find the number of words in a song from the artist name and song name

        :param artist_name: (str) the name of the artist
        :param song_name: (str) the name of the song
        :return: (int) the number of words in the song, or None if the song is not found
        """

        search_url = 'https://api.lyrics.ovh/v1/{}/{}'.format(artist_name, song_name)

        try:
            song_json = requests.get(search_url).json()  # Try reading the response into a json format
        except JSONDecodeError:
            return None  # And if that's not possible, return None since the lyrics cannot be found

        if 'error' in song_json.keys() or 'lyrics' not in song_json.keys():
            return None  # If error is a key, then the lyrics cannot be found

        lyrics = song_json['lyrics']
        lyrics = re.sub(r'([(\[]).*?([)\]])', '', lyrics).strip()  # This regex removes all chars in brackets () & []

        if lyrics == 'Instrumental':
            return 0

        return len(lyrics.split())  # This counts the number of words
