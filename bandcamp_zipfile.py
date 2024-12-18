'''Unzip zip files from Bandcamp.'''
from pathlib import Path
import re
from zipfile import ZipFile

class BandcampZipFile(ZipFile):
    def __init__(self, file, *args, **kwargs):
        super().__init__(file, *args, **kwargs)

        self.path = Path(self.filename)
        artist_album_info = self.path.stem.split(' - ') 
        if len(artist_album_info) == 2:
            self.artist = artist_album_info[0].title()
            self.album = artist_album_info[1].title()
        else:
            raise ValueError(f'Bad filename, {self.filename}')

    @staticmethod
    def remove_whitespace(s: str):
        "Replace whitespace with underscores."
        return re.sub(r'\s+', '_', s.strip())
    
    @staticmethod
    def starts_with_two_digits(name):
        return re.match(r'\d\d', name)
    
    def make_new_name(self, member_name):
        new_name = member_name.removeprefix(self.path.stem + ' - ')
        new_name = Path(new_name)
        new_name = new_name.stem.title() + new_name.suffix
        new_name = BandcampZipFile.remove_whitespace(new_name)

        # If the first two characters of new_name are digits, 
        # then insert '_-' between the digits and the rest of
        # new_name.
        if BandcampZipFile.starts_with_two_digits(new_name):
            new_name = new_name[:2] + '_-' + new_name[2:]  
        
        return new_name
        
    def extractall(self, dest):
        # assume that dest is a Path
        artist_dir = BandcampZipFile.remove_whitespace(self.artist.title())
        album_dir = BandcampZipFile.remove_whitespace(self.album.title())
        artist_album_path = dest / artist_dir / album_dir
        print(artist_album_path)
        try:
            artist_album_path.mkdir(parents=True)
        except FileExistsError:
            pass
        for member_name in self.namelist():
            new_member_name = self.make_new_name(member_name)
            member = self.extract(member_name, path=artist_album_path)
            new_member = artist_album_path / new_member_name
            print(f'Name: {member_name} of type {type(member_name)}')
            print(f'New Name: {new_member_name} of type {type(new_member_name)}')
            print(f'Path: {member} of type {type(member)}')
            print(f'New Path: {new_member} of type {type(new_member)}')
            print()
            Path(member).rename(new_member)

    def __str__(self):
        # return f'Path: {self.path}'
        return f'Filename: {self.path.name}\n' +\
            f'Artist: {self.artist}\n' +\
            f'Album: {self.album}'

if __name__ == '__main__':
    # print(__doc__)

    bczf = BandcampZipFile('zip/Riot City - Burn The Night.zip')
    # print(bczf)
    bczf.extractall(Path('music'))
