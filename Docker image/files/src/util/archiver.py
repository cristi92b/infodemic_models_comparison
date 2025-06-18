import logging
import os
import sys
from os import listdir
from os.path import isfile, join
import tarfile

class Archiver:

    def __init__(self,folder):
        self.folder = folder

    def create_bz2(self,remove_files = True):
        logging.info('Archiving contents [ remove_files = ' + str(remove_files) + ' ] of folder: ' + str(self.folder))
        filename = os.path.join(self.folder, os.path.basename(self.folder) + '_archive.tar.bz2')
        allfiles = [f for f in listdir(self.folder) if isfile(join(self.folder, f))]
        archived = []
        with tarfile.open(filename, "w:bz2") as archive:
            for file in allfiles:
                if 'result' not in str(os.path.basename(file)) and ( '.csv' in str(os.path.basename(file)) or '.xml' in str(os.path.basename(file)) ):
                    logging.info('Adding file to tar: ' + file)
                    archive.add(os.path.join(self.folder,file), arcname=str(os.path.basename(file)))
                    archived.append(os.path.join(self.folder,file))
        if remove_files:
            for file in archived:
                logging.info('Removing file ' + file)
                os.remove(os.path.join(self.folder,file))
        return filename


#cwd = os.getcwd()
#folder = os.path.join(cwd,'SIR')
#arch = Archiver(folder)
#arch.create_tar()
