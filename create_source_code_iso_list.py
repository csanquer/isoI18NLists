#!/usr/bin/env python
# -*- coding: utf8 -*-
'''
@author: Charles SANQUER
'''


try:
  from lxml import etree
except ImportError:
  try:
    # Python 2.5
    import xml.etree.cElementTree as etree
  except ImportError:
    try:
      # Python 2.5
      import xml.etree.ElementTree as etree
    except ImportError:
      try:
        # normal cElementTree install
        import cElementTree as etree
      except ImportError:
        try:
          # normal ElementTree install
          import elementtree.ElementTree as etree
        except ImportError:
          print("Failed to import ElementTree from any known place")

def sortedDictValues(adict):
    items = adict.items()
    items.sort()
    return [value for key, value in items]

countries = {}
languages = {}
          
with open("iso_xml/countries.xml", "r") as countriesXml:
    tree = etree.parse(countriesXml)
    
    for elt in tree.iter('country'):
        code = elt.findtext('code')
        englishName = elt.findtext('english_name')
        frenchName = elt.findtext('french_name')
        
        if not code in countries or type(countries[code]) != dict:
            countries[code] = { 'code': '' , 'english_name' : '' , 'french_name' : ''}
        
        countries[code]['code'] = code
        countries[code]['english_name'] = englishName
        countries[code]['french_name'] = frenchName

with open("iso_xml/languages.xml", "r") as languagesXml:
    tree = etree.parse(languagesXml)
    
    for elt in tree.iter('language'):
        code3B = elt.findtext('alpha3_B_code')
        code3T = elt.findtext('alpha3_B_code')
        code2 = elt.findtext('alpha2_code')
        englishName = elt.findtext('english_name')
        frenchName = elt.findtext('french_name')
        
        if not code3B in languages or type(languages[code3B]) != dict:
            languages[code3B] = { 'code3B': '' , 'code3T': '' , 'code2': '' , 'english_name' : '' , 'french_name' : ''}
        
        languages[code3B]['code3B'] = code3B
        languages[code3B]['code3T'] = code3T
        languages[code3B]['code2'] = code2
        languages[code3B]['english_name'] = englishName
        languages[code3B]['french_name'] = frenchName

indent=' '*4

with open("iso_code_output/iso_lists.php", "w") as phpfile:
    
    phpfile.write('<?php'+"\n\n")
    
    sortedCountries = sortedDictValues(countries)
    sortedLanguages = sortedDictValues(languages)
    
    phpfile.write('$countries = array('+"\n")
    for country in sortedCountries :
       phpfile.write(indent+"'"+(country['code'].replace("'","\'")).encode('utf-8')+"' =>  array("+"\n")
       phpfile.write(indent*2+"'code' => '"+(country['code'].replace("'","\\\'")).encode('utf-8')+"',\n")
       phpfile.write(indent*2+"'french' => '"+(country['french_name'].replace("'","\\\'")).encode('utf-8')+"',\n")
       phpfile.write(indent*2+"'english' => '"+(country['english_name'].replace("'","\\\'")).encode('utf-8')+"',\n") 
       phpfile.write(indent+'),'+"\n") 
    phpfile.write(');'+"\n\n")
    
    phpfile.write('$countriesFrench = array('+"\n")
    for country in sortedCountries :
       phpfile.write(indent+"'"+(country['code'].replace("'","\'")).encode('utf-8')+"' => '"+(country['french_name'].replace("'","\\\'")).encode('utf-8')+"',\n") 
    phpfile.write(');'+"\n\n")
    
    phpfile.write('$countriesEnglish = array('+"\n")
    for country in sortedCountries :
       phpfile.write(indent+"'"+(country['code'].replace("'","\'")).encode('utf-8')+"' => '"+(country['english_name'].replace("'","\\\'")).encode('utf-8')+"',\n") 
    phpfile.write(');'+"\n\n")
    
    phpfile.write('$languages = array('+"\n")
    for language in sortedLanguages :
       phpfile.write(indent+"'"+(language['code3B'].replace("'","\'")).encode('utf-8')+"' =>  array("+"\n")
       phpfile.write(indent*2+"'code3B' => '"+(language['code3B'].replace("'","\\\'")).encode('utf-8')+"',\n")
       phpfile.write(indent*2+"'code3T' => '"+(language['code3T'].replace("'","\\\'")).encode('utf-8')+"',\n")
       phpfile.write(indent*2+"'code2' => '"+(language['code2'].replace("'","\\\'")).encode('utf-8')+"',\n")
       phpfile.write(indent*2+"'french' => '"+(language['french_name'].replace("'","\\\'")).encode('utf-8')+"',\n")
       phpfile.write(indent*2+"'english' => '"+(language['english_name'].replace("'","\\\'")).encode('utf-8')+"',\n") 
       phpfile.write(indent+'),'+"\n") 
    phpfile.write(');'+"\n\n")
    
    phpfile.write('$languages2French = array('+"\n")
    for language in sortedLanguages :
       if len(language['code2']) > 0 :
           phpfile.write(indent+"'"+(language['code2'].replace("'","\'")).encode('utf-8')+"' => '"+(language['french_name'].replace("'","\\\'")).encode('utf-8')+"',\n")
    phpfile.write(');'+"\n\n")
    
    phpfile.write('$languages2English = array('+"\n")
    for language in sortedLanguages :
       if len(language['code2']) > 0 :
           phpfile.write(indent+"'"+(language['code2'].replace("'","\'")).encode('utf-8')+"' => '"+(language['english_name'].replace("'","\\\'")).encode('utf-8')+"',\n")
    phpfile.write(');'+"\n\n")
    
    phpfile.write('$languages3BFrench = array('+"\n")
    for language in sortedLanguages :
       phpfile.write(indent+"'"+(language['code3B'].replace("'","\'")).encode('utf-8')+"' => '"+(language['french_name'].replace("'","\\\'")).encode('utf-8')+"',\n")
    phpfile.write(');'+"\n\n")
    
    phpfile.write('$languages3BEnglish = array('+"\n")
    for language in sortedLanguages :
       phpfile.write(indent+"'"+(language['code3B'].replace("'","\'")).encode('utf-8')+"' => '"+(language['english_name'].replace("'","\\\'")).encode('utf-8')+"',\n")
    phpfile.write(');'+"\n\n")
    
    phpfile.write('$languages3TFrench = array('+"\n")
    for language in sortedLanguages :
       phpfile.write(indent+"'"+(language['code3T'].replace("'","\'")).encode('utf-8')+"' => '"+(language['french_name'].replace("'","\\\'")).encode('utf-8')+"',\n")
    phpfile.write(');'+"\n\n")
    
    phpfile.write('$languages3TEnglish = array('+"\n")
    for language in sortedLanguages :
       phpfile.write(indent+"'"+(language['code3T'].replace("'","\'")).encode('utf-8')+"' => '"+(language['english_name'].replace("'","\\\'")).encode('utf-8')+"',\n")
    phpfile.write(');'+"\n\n")    
