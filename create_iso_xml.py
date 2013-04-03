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

import csv
import re

def customUcfirst(matchobj):
    strfound = matchobj.group(0)
    if strfound.lower() not in ('l', 'le', 'les', 'la', 'the', '\'s', 'a', 'et', 'and', 'du', 'de', 'd', 'des', 'of') :
        return strfound.capitalize() 
    else :
        return strfound.lower() 

def customCapitalize(string):
    reg = re.compile(r"[\w,']+", re.UNICODE)
    return reg.sub(customUcfirst,string)

def sortedDictValues(adict):
    items = adict.items()
    items.sort()
    return [value for key, value in items]

countries = {}

with open("iso_sources/iso_3166-1_list_en.xml", "r") as iso3166en:
    tree = etree.parse(iso3166en)
    
    for elt in tree.iter('ISO_3166-1_Entry'):
        name = elt.findtext('ISO_3166-1_Country_name')
        code = elt.findtext('ISO_3166-1_Alpha-2_Code_element')
        
        if not code in countries or type(countries[code]) != dict:
	        countries[code] = { 'code': '' , 'english_name' : '' , 'french_name' : ''}
	    
        countries[code]['code'] = code
        countries[code]['english_name'] = name

with open("iso_sources/iso_3166-1_list_fr.xml", "r") as iso3166fr:
    tree = etree.parse(iso3166fr)
        
    for elt in tree.iter('ISO_3166-1_Entry'):
        name = elt.findtext('ISO_3166-1_Country_name')
        code = elt.findtext('ISO_3166-1_Alpha-2_Code_element')
        
    	if not code in countries or type(countries[code]) != dict:
            countries[code] = { 'code': '' , 'english_name' : '' , 'french_name' : ''}
            
        countries[code]['code'] = code
        countries[code]['french_name'] = name

countries = sortedDictValues(countries)
countriesElt = etree.Element('countries')

for  c in countries:
    countryElt = etree.SubElement(countriesElt, 'country')
    
    codeElt = etree.SubElement(countryElt, 'code')
    codeElt.text = c['code']
    
    englishNameElt = etree.SubElement(countryElt, 'english_name')
    englishNameElt.text = customCapitalize(c['english_name'])
    
    frenchNameElt = etree.SubElement(countryElt, 'french_name')
    frenchNameElt.text = customCapitalize(c['french_name']) 

countriesTree = etree.ElementTree(countriesElt)
countriesTree.write('iso_xml/countries.xml', encoding='UTF-8', pretty_print = True, xml_declaration=True)

#print csv.list_dialects()

languages = {}

with open('iso_sources/ISO-639-2_utf-8.txt', 'r') as langCSVFile:
    langCSV = csv.reader(langCSVFile, delimiter='|', lineterminator="\n", quotechar='"', skipinitialspace=True)
    for row in langCSV:
        if row[1] == '' or row[1] == None :
            row[1] = row[0]
        
        languages[row[0]] = { 'alpha3_B_code': row[0].decode("utf-8")  , 'alpha3_T_code': row[1].decode("utf-8")  , 'alpha2_code': row[2].decode("utf-8")  , 'english_name' : row[3].decode("utf-8")  , 'french_name' : row[4].decode("utf-8")  }

languagesElt = etree.Element('languages')
languages = sortedDictValues(languages)

for l in languages:
        languageElt = etree.SubElement(languagesElt, 'language')
        
        alpha3BElt = etree.SubElement(languageElt, 'alpha3_B_code')
        alpha3BElt.text = l['alpha3_B_code']
        
        alpha3TElt = etree.SubElement(languageElt, 'alpha3_T_code')
        alpha3TElt.text = l['alpha3_T_code']
        
        alpha2Elt = etree.SubElement(languageElt, 'alpha2_code')
        alpha2Elt.text = l['alpha2_code']
        
        englishNameElt = etree.SubElement(languageElt, 'english_name')
        englishNameElt.text = l['english_name']
        
        frenchNameElt = etree.SubElement(languageElt, 'french_name')
        frenchNameElt.text = l['french_name']

languagesTree = etree.ElementTree(languagesElt)
languagesTree.write('iso_xml/languages.xml', encoding='UTF-8', pretty_print = True, xml_declaration=True)
    