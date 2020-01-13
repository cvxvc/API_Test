import requests
import time

from bs4 import BeautifulSoup


class MusicBrainzHandler:
    """
    A class containing helper functions for interacting with the MusicBrainz API
    """

    @staticmethod
    def parse_xml(url):
        """
        Read a url containing xml data, and parse this into a BeautifulSoup object

        :param url: (str) the url pointing to the data we want to parse
        :returns: (bs4.BeautifulSoup) the parsed data in BeautifulSoup form
        """

        req = requests.get(url)
        soup = BeautifulSoup(req.content, 'lxml')  # Pass the request content to an xml parser

        return soup

    @staticmethod
    def get_artist_id_from_artist_name(artist_name):
        """
        Given the name of an artist, find the MusicBrainz ID of that artist

        :param artist_name: (str) the name of the artist
        :return: (str) the MusicBrainz ID of the artist
        """

        print('Finding ID for artist {}...'.format(artist_name))

        # Search with a limit of 1 to find only the most likely match
        search_url = 'https://musicbrainz.org/ws/2/artist?query={}&limit=1'.format(artist_name)
        parsed_data = MusicBrainzHandler.parse_xml(search_url)

        artists = list(parsed_data.find_all('artist'))  # Find all artist tags in the xml tree

        if len(artists) == 0:
            raise ValueError('{} not found on musicbrainz'.format(artist_name))
        elif len(artists) > 1:
            raise ValueError('More than 1 artist found when search limit is 1')

        artist = artists[0]
        found_name = artist.find('name').text

        # Check that the name of the artist inputted matches the name of the artist found
        if artist_name.lower() != found_name.lower():
            print('Did you mean to search for {}?'.format(found_name))
            raise ValueError('{} not found on musicbrainz'.format(artist_name))

        artist_id = artist['id']  # Get the artist ID

        print('Found ID\n')

        return artist_id

    @staticmethod
    def get_artist_songs_from_artist_id(artist_id):
        """
        Find the list of an artist's songs from their MusicBrainz ID

        :param artist_id: (str) the MusicBrainz ID of the artist
        :return: (List[str]) the list of songs for the artist
        """

        print('Finding songs on musicbrainz for artist ID {}...'.format(artist_id))

        # Search limit set to 100 since this is the max
        search_url = 'https://musicbrainz.org/ws/2/work?artist={}&limit=100'.format(artist_id)
        parsed_data = MusicBrainzHandler.parse_xml(search_url)

        # Find how many songs there are for this artist ID
        work_list = parsed_data.find('work-list')
        number_of_songs = int(work_list['count'])

        # Find how many more additional queries we will need to make to get all songs
        required_iterations = int(number_of_songs / 100)

        songs = list(parsed_data.find_all('work'))  # Pull the first 100 songs

        # Iterate through the list in batches of 100 to pull the rest of the songs
        for i in range(required_iterations):
            time.sleep(1)  # Don't hammer the database!

            offset = 100 * (i + 1)  # Add offset to url to move along to the next 100 songs
            search_url = 'https://musicbrainz.org/ws/2/work?artist={}&limit=100&offset={}'.format(artist_id, offset)
            parsed_data = MusicBrainzHandler.parse_xml(search_url)

            songs.extend(list(parsed_data.find_all('work')))  # Add songs found in this iteration to the overall list

        song_names = [song.find('title').text for song in songs]  # Find the song titles
        song_names = list(set(song_names))  # Remove songs with duplicate names

        print('Found {} songs\n'.format(len(song_names)))

        return song_names
