#!/usr/bin/env python
#coding=utf-8

__author__ = 'Dmitriy Shikhalev'
__author_email__ = 'dmitriy.shikhalev@gmail.com'
__version__ = '1.6'

import xml.sax
import xml.dom.minidom as xmlp

# Хак для python3.3:
import sys
if sys.version.startswith('3'):
    unicode = lambda string: str(string)
# ... (хак для python3.3)



class XmlParserUAException(Exception): pass
class BadTag(XmlParserUAException): pass



class XmlParserUAHandler( xml.sax.ContentHandler ):
    def __init__(self, dict_for_result, to_strip):
        dict_for_result['_parent_'] = None
        dict_for_result['_tagName_'] = None
        dict_for_result['_value_'] = ''
        
        self.result = dict_for_result
        self.currentElement = self.result
        self.currentTag = None
        
        self.to_strip = to_strip

   # Call when an element starts
    def startElement(self, tag, attributes):
        self.currentTag = tag
        if not self.currentElement.get(tag):
            self.currentElement[tag] = list()
        newElement = dict(
            _parent_ = self.currentElement,
            _tagName_ = tag,
            _value_='',
            _attrs_ = None
        )
        self.currentElement[tag].append(newElement)
        self.currentElement = newElement
        self.currentElement['_attrs_'] = dict(attributes)

   # Call when an elements ends
    def endElement(self, tag):
        if self.currentElement['_tagName_'] == tag:
            self.currentElement = self.currentElement['_parent_']
        else:
            raise BadTag
    # Call when a character is read
    def characters(self, content):
        if self.to_strip:
            content = content.strip()
            
        self.currentElement['_value_'] += content


def xml2dict(txt, to_strip=True):
    dict_for_result = dict()
    h = XmlParserUAHandler(dict_for_result, to_strip)
    
    xml.sax.parseString(txt, h)
    
    def postClear(dic):
        if dic.get('_parent_'):
            del dic['_parent_']
        if dic.get('_tagName_'):
            del dic['_tagName_']
        if dic.get('_value_') == '':
            del dic['_value_']
        if dic.get('_attrs_') == {}:
            del dic['_attrs_']
        for key, value in dic.items():
            if not (key.startswith('_') and key.endswith('_')):
                for subdic in value:
                    postClear(subdic)
    
    postClear(dict_for_result)
    
    try: del dict_for_result['_attrs_']
    except: pass
    try: del dict_for_result['_parent_']
    except: pass
    try: del dict_for_result['_tagName_']
    except: pass
    
    return dict_for_result


def dict2xml(dic, document=None, parent=None, to_return=True):
    document = xmlp.Document()
    for key, sublist in dic.items():
        if not (key.startswith('_') and key.endswith('_')):
            for subdic in sublist:
                _dict2xml(subdic, key, document, document, True)
    
    return document.toprettyxml(encoding='UTF-8')


def _dict2xml(dic, tagName, document=None, parent=None, to_return=True):
    currentNode = None
    
    # Создание нода
    if tagName:
        currentNode = document.createElement(unicode(tagName))
    else:
        currentNode = document.createElement(unicode(dic['_tagName_']))
    parent.appendChild(currentNode)
    if dic.get('_value_'):
        currentNode.appendChild(document.createTextNode(unicode(dic['_value_'])))
    
    # Установка атрибутов для нода
    if dic.get('_attrs_'):
        for attr_key, attr_value in dic['_attrs_'].items():
            currentNode.setAttribute(unicode(attr_key), unicode(attr_value))
            
    for key, value in dic.items():
        if not (key.startswith('_') and key.endswith('_')):
            # Рекурсия:
            for subdic in value:
                if isinstance(subdic, dict):
                    _dict2xml(subdic, key, document, currentNode, False)

if __name__ == '__main__':
    TEST_STRING = b"""<?xml version="1.0" encoding="UTF-8"?>
    <a y="10">
        <b>
            something
        </b>
    </a>
    """

    TEST_DICT = {
        u'a': [
            {
                '_attrs_': {
                    u'y': u'10'
                },
                u'b': [
                    {
                        '_value_': u'something'
                    }
                ]
            }
        ]
    }
    
    print(dict2xml(TEST_DICT))
    print(xml2dict(dict2xml(xml2dict(TEST_STRING))))
    print(dict2xml(xml2dict(dict2xml(TEST_DICT))))
