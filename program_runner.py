import sys

from artist import Artist


def main():
    artist = Artist(sys.argv[1])       # Initialize artist object
    artist.print_artist_statistics()   # Print statistics to the console
    artist.plot_artist_histogram()     # Save the histogram of word counts to the plots folder


if __name__ == '__main__':
    main()
