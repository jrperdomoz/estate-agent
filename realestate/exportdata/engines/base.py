# -*- coding: utf-8 -*-
from lxml import etree
import datetime
import os
from django.core.cache import cache
import cPickle as pickle
import pytz
import logging
import sys
logger = logging.getLogger('estate')
import abc

# translation.activate('ru')
#rules_url
#encoding UTF-8 windows-1251
#xhtml_namespace


class BaseEngine(object):
    encoding = 'UTF-8'    
    CACHE_TIME = 3600 * 24  
    VALID_DAYS = 100
    XHTML_NAMESPACE = None
    error_log = {}    
    def __init__(self, feed):               
#         self.XHTML = "{%s}" % self.XHTML_NAMESPACE
#         self.NSMAP = {None : self.XHTML_NAMESPACE}
#         self.tz = pytz.timezone('Europe/Moscow')       
        self._use_cache = True          
        self._feed = feed
        self._feed_name = feed.name                
              
    def get_cache_key(self, lot):
        return '%s%s' % (self._feed_name, lot.id) 
        
    def get_cache(self, lot):        
        pickled_cache = cache.get(self.get_cache_key(lot))
        if pickled_cache:
            cached_dict = pickle.loads(pickled_cache)
            if cached_dict['modificated'] == lot.modificated:
                parser = etree.XMLParser(strip_cdata=False)
                offer = etree.XML(cached_dict['str_xml'], parser)                
                return offer
    
    def set_cache(self, lot, offer):
        str_xml = etree.tostring(offer, encoding='unicode')         
        pickled_dict = {'str_xml':str_xml, 'modificated':lot.modificated}
        pickle_xml = pickle.dumps(pickled_dict)
        cache.set(self.get_cache_key(lot), pickle_xml, self.CACHE_TIME)

    def write_XML_error(self, line):
        msg = u"%s\t%s\n" % (self.name, line)
        logger.error(msg)  
    
    @abc.abstractmethod    
    def create_offer(self, lot):
        """ create etree.Element with Add item """
        return    
    
    @abc.abstractmethod
    def get_XHTML(self, lots, use_cache):
        """ XML generator """
        return
    
    def get_offer(self, lot):         
        if self._use_cache: 
            offer = self.get_cache(lot)
            if offer is not None:
                return offer            
        offer, errors  = self.create_offer(lot)
        if errors:
            self.error_log[lot.id] = errors            
            return            
        if offer is not None:                      
            self.set_cache(lot, offer)   
        return offer    
    
    def add_offers(self, xhtml, lots):                      
        for lot in lots:
            offer = self.get_offer(lot)            
            if offer is not None:                                  
                xhtml.append(offer)    
                                
    def gen_XML(self, lots, file_name, use_cache=True):   
        xhtml = self.get_XHTML(lots, use_cache)  
        etree.ElementTree(xhtml).write(file_name, pretty_print=True, xml_declaration=True, encoding=self.encoding)
        self.write_error_log('%s.errors.xml' % file_name)   
    
    def el_maker(self, offer, empty_nodes):
        def sub_element(node, text, required=True): 
            if not text:
                if required:
                    empty_nodes.append(node)
            else:                
                etree.SubElement(offer, node).text = u"'%s'" % text
        return sub_element
        
    def write_error_log(self, file_name):
        try:
            os.remove(file_name)
        except OSError:
            pass
        if not self.error_log:
            return
        xhtml = etree.Element('Errors')     
        for lot_id, err_dict in self.error_log.iteritems():
            lot_node = etree.SubElement(xhtml, 'lot', {'id': u'%s' % lot_id})
            for err_type, err_msg in err_dict.iteritems():
                etree.SubElement(lot_node, 'error', {'type': err_type}).text = err_msg 
        etree.ElementTree(xhtml).write(file_name, pretty_print=True, xml_declaration=True, encoding=self.encoding)
            
            
    