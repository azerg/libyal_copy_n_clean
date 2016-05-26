# usage <path_to_libyal_library_root>

import sys
import os
from distutils.dir_util import copy_tree
from distutils.dir_util import remove_tree

libyalPath = sys.argv[1]

knownFolders = [
     ["msvscpp\\Release",        "x32\\Release"], # rootPathRelease86
     ["msvscpp\\VSDebug",        "x32\\VSDebug"], # rootPathDebug86
     ["msvscpp\\x64\\Release",   "x64\\Release"], # rootPathRelease64
     ["msvscpp\\x64\\VSDebug",   "x64\\VSDebug"]  # rootPathDebug64
 ]

junkMasks = [".ilk", ".iobj", ".ipdb", ".exp", ".VC.opendb", ".VC.db", ".vs", ".suo"]

def ProcessFolderImpl(rootFolder, folderpath, callback):
    """Loop through all folders"""
    filesInFolder = os.listdir(folderpath)

    for fileInFolder in filesInFolder:
        filePath = folderpath + "\\" + fileInFolder
        if (os.path.isdir(filePath)):
            ProcessFolderImpl(rootFolder, filePath, callback)
            VisitFolder(rootFolder, filePath)
    return

def VisitFolder(rootFolder, filePath):
    """Process folder. Delete if invalid. Copy if valid"""
    if (CopyFolderIfNeeded(rootFolder, filePath) == True):
        return
    # deleting folder @filePath
    basename = os.path.basename(filePath)
    if (basename == 'VSDebug') or (basename == 'Release'):
        for validPathPrefix in knownFolders:
            # dont delete valid folders that were copied already
            if (filePath == rootFolder + '\\' + validPathPrefix[1]):
                return
        remove_tree(filePath)

def CopyFolderIfNeeded(rootFolder, filePath):
    """Copied folder if it fits knownFolders list"""
    CleanJunkFiles(filePath, junkMasks)
    for knownFolder in knownFolders:
        if (filePath == (rootFolder + '\\' + knownFolder[0])):
            destPath = rootFolder + '\\' + knownFolder[1]
            print 'Copying To: ', destPath
            copy_tree(filePath, destPath)
            remove_tree(filePath)
            return True
    return False

def CleanJunkFiles(folderPath, junkMasks):
    """Removes all files with juntMask in filename"""
    filesInFolder = os.listdir(folderPath)
    for fileInFolder in filesInFolder:
        for junkMask in junkMasks:
            if (fileInFolder.endswith(junkMask)) or (fileInFolder == junkMask):
                fileToDelete = folderPath + '\\' + fileInFolder
                try:
                    os.remove(fileToDelete)
                except WindowsError:
                    print 'Error deleting: ', fileToDelete

def ProcessFolder(folderpath, callback):
    """Process root folder"""
    return ProcessFolderImpl(folderpath, folderpath, callback)

if __name__ == '__main__':
    ProcessFolder(libyalPath, VisitFolder)
    print 'Done.'