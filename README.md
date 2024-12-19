# Unzipping Albums Downloaded from Bandcamp

An album downloaded from [Bandcamp](https://bandcamp.com/) is typically a zip file that contain the album's cover and songs. The class `BandcampZipFile` defined in `bandcamp_zipfile.py` inherits from `ZipFile`, overwriting the `extractall()` method in favour of a new version which extracts the album's songs and cover to an Artist/Album directory. Also, in directory and file names, whitespace is replaced by underscores.

## Usage

```python
from bandcamp_zipfile import BandcampZipFile

# a zip file from Bandcamp
src = 'zip/Cirith Ungol - Frost and Fire.zip'

# the directory to unzip to
dest = 'music'

bczf = BandcampZipFile(src)
bczf.extractall(dest)
```
