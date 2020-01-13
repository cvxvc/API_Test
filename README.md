# API Tech Test

### Prerequisites

##### Python 3.6.* or later

Installation instructions: https://www.python.org/downloads/

##### A Python IDE e.g. Pycharm Community Edition

https://www.jetbrains.com/pycharm/download/

### Initial checks

Ensure that all the packages are installed correctly by running this from the command line:

```bash
pip3 install -r ./requirements.txt
```

Run the tests to make sure everything is working correctly, by running this from the command line:

```bash
python -m pytest
```

### Running the program

The program is run from the command line. The command to run is:

```bash
python program_runner.py name_of_artist
```

The command line argument is the name of the artist. If the artist name has a space in it, you'll need to enclose the command line argument in quotation ("") marks.

After running this command, the program will find all the songs it can for the given artist. Various statistics will then be outputted to the console. Additionally, the program will also plot a histogram of the word count of the artist, and save it into the plots folder (the image file will have the same name as the artist). Some histograms have already been created and saved into the plots file.
