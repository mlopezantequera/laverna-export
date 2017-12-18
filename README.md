#Intro
This python script exports notes from [Laverna](http://laverna.cc) to markdown files.
The notes are saved in directories corresponding to notebooks.

This version is updated to work with the new laverna export format (.json + 'incomplete'.md)

#Usage

./export.py path_to_laverna_backups output_path

laverna_backups is the directory that you find in the laverna exported .zip file
output_path is the desired path for your .md files.

#Limitations
This is a simple script that has some limitations. However, it could easily be extended to handle more complex use cases.

- Flat notebook structure: the exporter ignores the notebook hierarchy
  
