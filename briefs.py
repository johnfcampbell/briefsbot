import re
#
# We want to create individual briefs from the text that was
# pasted from the PHP page. 
# The page gives instructions to select the copy from Newsgate 
# in WYSIWIG mode. This gives us tags that we can hang 
# a subsitution on.
#
# We want to be ready for either briefhead or subhed tags.
# And these are where we want to do the spliit.
# other than that, we wanna pick out notesface and 
# a few basic tags such as an endnote.
# 
# Paragraphs are separated as in the AP Exchange feed.
#
# Profile ID comes from a pulldown on the PHP page,
# and it identifies the briefs as state, local region or crime. 
#
# The Saxotech slug is created from the 'M' prefix familiar from Coyote,
# the date, the stamp from the PHP write and a suffix applied here to
# distinguish briefs in the same batch.



def break_up(text,filename):
    pubText = text
#    print "pubText ="
#    print pubText
    #pubText = re.sub(r'subhead_lead>',r'generic_head>',pubText)
    pubText = generalizeHeds(pubText)
    
    pubText = re.sub(r'<generic_head>',r'<split_element><generic_head>',pubText)
    briefsList = pubText.split('<split_element>')
    profileID = briefsList.pop(0)
    print "profileId ="
    print profileID
    profileID = re.sub(r'.SOM..(\d{4}).',r'\1',profileID)

    print "profileId ="
    print profileID
    profileID = re.sub(r'.EP.',r'',profileID)
    print "profileId ="
    print profileID
    profileID = re.sub(r'<.*',r'',profileID)
    print "profileId ="
    print profileID
    sequenceLetter = "A"

    for brief in briefsList:
        slug=makeBriefSlug(profileID,filename,sequenceLetter)
        prepForPublicus(brief, profileID,slug)
        sequenceLetter = nextSequenceLetter(sequenceLetter)
    return

def generalizeHeds(text):
    pubText = text

    pubText = re.sub(r'subhead_lead>',r'generic_head>',pubText)
    pubText = re.sub(r'subhead>',r'generic_head>',pubText)
    pubText = re.sub(r'subhead_lead>',r'generic_head>',pubText)

    return pubText

def makeBriefSlug(profileID,filename,sequenceLetter):
    from slugTools import slugTomorrowString

    theSlug = "M"
    theDate = slugTomorrowString()
    theChunk = filename
    theChunk = re.sub(r'FTP',r'BRF',theChunk)
    theSlug = theSlug + theDate + theChunk + sequenceLetter
    print "theslug = " + theSlug
    return theSlug 

def nextSequenceLetter(sequenceLetter):
    if (sequenceLetter == 'Z'): 
        return '0'
    if (sequenceLetter == '9'):
        return 'a'
    return chr(ord(sequenceLetter)+1)

def webFixed(theText):
    theText = re.sub(r'(?i)<web.*?>','',theText)
    theText = re.sub(r'(?i)<.web.*?>','',theText)
    theText = re.sub(r'<[A-Z][A-Z]>','',theText)
    theText = re.sub(r'<EL.{2,4}>','',theText)
    theText = re.sub(r'(?i)<tag.*?>','',theText)
    theText = re.sub(r'(?i)<.tag.*?>','',theText)
    theText = re.sub(r'(?i)<end.*?>','',theText)
    theText = re.sub(r'(?i)<.end.*?>','',theText)
    return theText

def signatureFixed(theText):
    theText = re.sub(r'<EP>(<.signature>)','\1',theText)
    theText = re.sub(r'(<.signature>)(<signature_credit>)','\1, \2',theText)
    theText = re.sub(r'<.signature>','',theText)
    theText = re.sub(r'<signature>','',theText)
    theText = re.sub(r'<.signature_credit>','',theText)
    theText = re.sub(r'<signature_credit>.{1,4}([A-Z])','\1',theText)
    theText = re.sub(r'<signature_credit>\W{1,4}','',theText)
    theText = re.sub(r'<signature_credit>','',theText)
    return theText

def prepForPublicus(brief,profileID,slug):
    from slugTools import wrapAndWrite
    from slugTools import openArticle
    from slugTools import closeArticle
    from slugTools import tomorrowString
    filename=slug
    #slug = slug + '.xml'
    slug = '/Users/Editmac05/Documents/bin/briefs/workbin/' + slug + '.xml'
    fileXML = open(slug,'w')
    openArticle(fileXML)
    briefHed = brief
    briefBody = brief

    briefHed = re.sub(r'(.*<.generic_head>).*',r'\1',briefHed)
    briefHed = re.sub(r'<EP>',r' ',briefHed)
    briefHed = re.sub(r' <.gen',r'</gen',briefHed)
    print "brief hed = " + briefHed
    briefHed = re.sub(r'generic_head','headline',briefHed)
    briefHed = re.sub(r'<NO.*?>',r'<NO>',briefHed)
    briefHed = re.sub(r'<NO>.*?<NO>',r'',briefHed)

    wrapAndWrite("filename",filename,fileXML)
    wrapAndWrite("profileId",profileID,fileXML)
    wrapAndWrite("Gns","",fileXML)
    wrapAndWrite("keyword","BRIEF",fileXML)
    wrapAndWrite("pubdate",tomorrowString(),fileXML)
    #wrapAndWrite("pubdate",'2/7/2012',fileXML)
    wrapAndWrite("edition","",fileXML)
    wrapAndWrite("section","",fileXML)

    print >> fileXML, briefHed

    briefBody = re.sub(r'.*_head>',r'',briefBody)
    #print "briefBody = " + briefBody
    hasDateline = re.search('<dateline>',briefBody) 
    #print "hasdateline = " + hasDateline
    if hasDateline:
        dateline = re.sub(r'(.*<.dateline>).*',r'\1',briefBody)
        briefBody = re.sub(r'.*<.dateline>(.*)',r'\1',briefBody)
        print "dateline = " + dateline
        dateline = re.sub(r'.*(<dateline>)',r'\1',dateline)
        print "dateline revised = " + dateline
        #print "briefbody = " + briefBody
        print >> fileXML, dateline
    briefBody = re.sub(r'#EOM#',r'',briefBody)
    #print "1. briefbody = " + briefBody
    briefBody = re.sub(r'<NO.*?>',r'<NO>',briefBody)
    #print "2. briefbody = " + briefBody
    briefBody = re.sub(r'<NO>.*?<NO>',r'',briefBody)
    #briefBody = re.sub(r'<EP>',r'</body_text><body_text>',briefBody)
    briefGrafs = briefBody.split('<EP>')
    for graf in briefGrafs:
        graf = signatureFixed(graf)
        graf = webFixed(graf)
        wrapAndWrite('body_text',graf,fileXML) 
    
    #wrapAndWrite('body_text',briefBody,fileXML) 
    closeArticle(fileXML)
    
    return
