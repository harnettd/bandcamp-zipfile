"""
Unzip Bandcamp zip files.

Unzip Bandcamp zip files to an artist/album directory structure. Replace
whitespace with underscores in all path names.

@author: Derek Harnett
"""
from pathlib import Path
import re
from zipfile import ZipFile

class BandcampZipFile(ZipFile):
    def __init__(self, file, **kwargs) -> None:
        """
        Create a new BandcampZipFile instance.

        :param file: path of a Bandcamp zip file
        :type file: str or pathlike object
        """
        super().__init__(file, **kwargs)

        self.stem: str = Path(self.filename).stem
        artist_album_info: list[str] = self.stem.split(' - ') 
        if len(artist_album_info) == 2:
            self.artist: str = artist_album_info[0].title()
            self.album: str = artist_album_info[1].title()
        elif len(artist_album_info) == 3 and artist_album_info[0] == artist_album_info[1]:
            self.artist: str = artist_album_info[0].title()
            self.album: str = artist_album_info[2].title()
        else:
            raise ValueError(f'Bad Bandcamp zipfile name, {self.filename}')

    @staticmethod
    def remove_whitespace(s: str) -> str:
        """
        Trim whitespace and replace remaining whitespace with underscores.

        Usage:
        >>> BandcampZipFile.remove_whitespace('  a  b ')
        'a_b'
        """
        return re.sub(r'\s+', '_', s.strip())
    
    @staticmethod
    def starts_with_two_digits(s: str) -> bool:
        """
        Return True if s starts with two digits, False otherwise.

        Usage:
        >>> BandcampZipFile.starts_with_two_digits('05 Song Title')
        True
        >>> BandcampZipFile.starts_with_two_digits('5 Song Title')
        False
        """
        return re.match(r'\d\d', s) is not None
    
    def make_new_name(self, name: str) -> str:
        """
        Make a new name for a member of the zipfile.
        """
        new_name = Path(name)
        stem: str = new_name.stem
        suffix: str = new_name.suffix
        new_name: str = stem.removeprefix(self.stem + ' - ').title() + suffix
        new_name = BandcampZipFile.remove_whitespace(new_name)

        if BandcampZipFile.starts_with_two_digits(new_name):
            new_name = new_name[:2] + '_-' + new_name[2:]  
        
        return new_name
        
    def extractall(self, dest) -> None:
        """
        Extract all members of the zipfile.

        :param dest: Directory to unzip to
        :type dest: string or pathlike
        """
        if isinstance(dest, str):
            dest = Path(dest)

        # Make a directory for the album, if one doesn't already exist.
        artist_dir: str = BandcampZipFile.remove_whitespace(self.artist.title())
        album_dir: str = BandcampZipFile.remove_whitespace(self.album.title())
        artist_album_path: Path = dest / artist_dir / album_dir
        try:
            artist_album_path.mkdir(parents=True)
        except FileExistsError:
            # If the directory already exists, then do nothing.
            pass

        # For each member of the zipfile, extract and rename.
        member_name: str
        for member_name in self.namelist():
            new_member_name: str = self.make_new_name(member_name)
            member: str = self.extract(member_name, path=artist_album_path)
            new_member: Path = artist_album_path / new_member_name
            Path(member).rename(new_member)

    def __str__(self):
        return f'Filename: {self.filename}\n' +\
            f'Stem: {self.stem}\n' +\
            f'Artist: {self.artist}\n' +\
            f'Album: {self.album}'

if __name__ == '__main__':
    print(__doc__)
    src = Path('zip')
    dest = Path('music')
    with open('bandcamp-extract.log', 'w') as logfile:
        for zf in src.iterdir():
            try:
                bczf = BandcampZipFile(zf)
            except ValueError as err:
                message: str = f'[-] {err}'
                print(message)
                logfile.write(message)
            else:
                bczf.extractall('music')
                message: str = f'[+] {bczf.filename}'
                print(message)
                logfile.write(message)
