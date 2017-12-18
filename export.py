#!/usr/bin/env python3

"""
Updated version of https://github.com/tobanw/laverna-export

Upgrades:

- Works with new laverna export format (.json + 'incomplete'.md)
- Tags are included in each note and in the filename (compatible with tagspaces)
- Creation and modification times are kept

Usage:

./export.py path_to_laverna_backups output_path

laverna_backups is the directory that you find in the laverna exported .zip file
output_path is the desired path for your .md files.
"""

import re,os,json,glob,sys

def main():

    workdir = sys.argv[1] 
    out_dir = sys.argv[2] # example: '/home/user/laverna-exported-md'

    db_dir = 'notes-db'
    notes_dir = 'notes'

    try:
        os.mkdir(out_dir)
    except FileExistsError:
        print('Output directory already exists. Proceeding')
      
    # we will save each notebook in a subfolder (not tested)
    notebooksjson = os.path.join(workdir, db_dir, 'notebooks.json')
    with open(notebooksjson,'r') as f:
      notebooks = json.load(f)
    notebook_names = {}  
    for notebook in notebooks:
        notebook_names['id'] = notebook['name']
        try:
          os.mkdir(out_dir, notebook['name'])
        except FileExistsError:
          pass

    for notejson in glob.iglob(os.path.join(workdir,db_dir,notes_dir,'*.json')):
        notemd = notejson.replace('.json', '.md')
        
        with open(notejson,'r') as f:
          notedict = json.load(f)
                  
        with open(notemd,'r') as f:
          notetext = f.read()
          
        # we will save each notebook in a subfolder (not tested)
        if notedict['notebookId'] in notebook_names.keys():
            notebook_dir = notebook_names['notebookId']
        else:
            notebook_dir = ''

        # create filename. It will include tags if they exist
        notename = clean_filename(notedict['title'].lower(), 'md')
        if len(notedict['tags']) > 0:
            tagstr = ' '.join(notedict['tags'])
            notepath = os.path.join(out_dir,notebook_dir,notename.replace('.md','['+tagstr+'].md'))
        else:
            notepath = os.path.join(out_dir,notebook_dir,notename)

        # copy laverna's markdown. Add title and tags.
        with open(notepath,'w') as output_md:
            output_md.write('# '+notedict['title']+'\n\n')
            if len(notedict['tags']) > 0:
              output_md.write('tags: ')             
              for tag in notedict['tags']:
                output_md.write('['+tag+'] ')
              output_md.write('\n\n')
            output_md.write(notetext)
                
        #fix creation and modification date
        os.utime(notepath, (notedict['created'] / 1000, notedict['updated'] / 1000))        
        
        print(notepath, 'done.')
    print('All Done!')

#filename utility functions
def clean_filename(namestr,ext):
    cleaned = strip_ends(namestr)
    cleaned = sep_to_dash(cleaned)
    cleaned = strip_special(cleaned)
    return cleaned + '.' + ext

def strip_ends(namestr):
    return re.sub('^\W+|\W+$','',namestr)

def sep_to_dash(namestr):
    #convert separator characters to dashes
    outstr = re.sub('[\s/\|;:,\.\+&]','-',namestr)
    return re.sub('-+','-',outstr) #compress multi-dash

def strip_special(namestr):
    #remove special characters
    return re.sub('[^a-zA-Z0-9-_]','',namestr)

#execute only if run as script
if __name__ == "__main__":
    main()
