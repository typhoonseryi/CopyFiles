import sys
import os
import shutil
import argparse
from bs4 import BeautifulSoup


class FileManager:

    def __init__(self, config):
        self.config = config

    def _parser(self):
        data = BeautifulSoup(self.config.read(), 'lxml')
        return data.find_all('file')

    def copy_files(self):
        files = self._parser()
        for file in files:
            src = r'{}'.format(file.get('source_path'))
            dst = r'{}'.format(file.get('destination_path'))
            fnm = r'{}'.format(file.get('file_name'))
            sep = os.path.sep
            sf = src + sep + fnm if src else fnm
            df = dst + sep + fnm if dst else fnm
            try:
                shutil.copyfile(sf, df)
            except IOError:
                print(f'The destination location of file "{fnm}" is not writable')
            except shutil.SameFileError as exc:
                print(f'Source and destination are the same file "{fnm}"')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config',
        type=argparse.FileType(
            mode='r',
            encoding='utf-8',
        ),
        help='Enter the path to the config file',
    )
    args = parser.parse_args(sys.argv[1:])
    fm = FileManager(args.config)
    fm.copy_files()
