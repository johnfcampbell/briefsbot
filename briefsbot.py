import re, os, briefs

# The joined briefs will have been placed in the drop box 
# after being pasted into the PHP page. 
# PHP has write only access to the drop box,
# and we get read access as the native user.

path = '/Users/johncampbell/Public/Drop Box/briefspath'
brief_files = os.listdir(path)

for briefpackage in brief_files:
    print "briefpackage = "
    print briefpackage
    
    realBrief = re.match('FTP',briefpackage)
    #nonBrief = re.search(r'!F',briefpackage)
    if not realBrief: continue
    the_file = os.path.join(path, briefpackage)
    the_text = open(the_file, "r")

    for the_line in the_text:
        briefs.break_up(the_line,briefpackage)
