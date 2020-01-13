import matplotlib.pyplot as plt
import numpy as np

from lyricsovh_handler import LyricsOvhHandler
from musicbrainz_handler import MusicBrainzHandler


class Artist:
    """
    A class representing an artist
    """

    def __init__(self, artist_name):
        self.artist_name = artist_name
        self.artist_id = MusicBrainzHandler.get_artist_id_from_artist_name(self.artist_name)
        self.artist_songs = MusicBrainzHandler.get_artist_songs_from_artist_id(self.artist_id)
        self.lyrics_dict = Artist.construct_lyrics_dict(self.artist_name, self.artist_songs)

    @staticmethod
    def construct_lyrics_dict(artist_name, artist_songs):
        """
        Constructs a dictionary, where the key is song name and the value is number of words

        :param artist_name: (str) the name of the artist
        :param artist_songs: (List[str]) the list of songs for the artist
        :return: the dictionary mapping songs to number of words
        """

        print('Finding lyrics for {} {} songs...'.format(len(artist_songs), artist_name))

        lyrics_dict = {}

        # Loop through found songs, finding the word count for each
        for song in artist_songs:
            word_count = LyricsOvhHandler.find_number_of_words_in_song(artist_name, song)

            if word_count is not None:  # Only triggers if we found lyrics for a song
                lyrics_dict[song] = word_count

        print('Found lyrics for {} of the {} songs\n'.format(len(lyrics_dict), len(artist_songs)))

        return lyrics_dict

    def print_artist_statistics(self):
        """
        Function which prints various statistics to the console related to song lengths of the artist
        """

        if len(self.lyrics_dict) == 0:
            print('No statistics to output for {}'.format(self.artist_name))
        else:
            song_lengths = list(self.lyrics_dict.values())

            # Compute a load of statistics
            mean_length = np.mean(song_lengths)
            median_length = np.median(song_lengths)
            length_stand_dev = np.std(song_lengths)

            min_length = np.min(song_lengths)
            max_length = np.max(song_lengths)
            min_length_song = min(self.lyrics_dict, key=self.lyrics_dict.get)
            max_length_song = max(self.lyrics_dict, key=self.lyrics_dict.get)

            # Output the computed statistics
            print('Outputting statistics for {}\n'.format(self.artist_name))

            print('Found lyrics for {} songs'.format(len(song_lengths)))
            print('Mean song length = {:.2f} words'.format(mean_length))
            print('Median song length = {:.2f} words'.format(median_length))
            print('Standard deviation of song length = {:.2f} words'.format(length_stand_dev))

            print('Shortest song is {} with {} words'.format(min_length_song, min_length))
            print('Longest song is {} with {} words'.format(max_length_song, max_length))

    def plot_artist_histogram(self):
        """
        Function which plots a song length histogram for the artist, and saves it into the plots folder
        """

        if len(self.lyrics_dict) == 0:
            print('No songs to plot for {}'.format(self.artist_name))
        else:
            # Create a histogram
            plt.figure()
            plt.hist(self.lyrics_dict.values(), bins=50)
            plt.title('Word count histogram for artist {}'.format(self.artist_name))
            plt.grid()
            plt.xlabel('Word count')
            plt.ylabel('Frequency')

            # And then save it
            plt.savefig('plots/{}.png'.format(self.artist_name))
