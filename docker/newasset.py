#!/usr/bin/env python3
"""
This presents a Maptool Asset Class to assemble or extract
any of our assets.

The asset type is determined by the container.  Either a maptool
asset file which is a zipfile containing a content.xml and other
files, or an xml file with the outer tag matching one of our asset
types.

This class will provide a mechanism to extract macros from some
objects to individual files.  A file for the xml wrapper and a 
file for the macro text itself.

Macro and MacroSet objects extract to a generic macro/ directory,
Token macros extract to the Token directory. Campaign Macros
extract to the Campaign directory.
"""
import sys
sys.path.append('docker')
from MTAssetLibrary import properties_xml, print_info, XML2File
from MTAssetLibrary import MacroNameQuote, DataElement, NewElement
from MTAssetLibrary import maptool_macro_tags as tagset
from MTAssetLibrary import add_directory_to_zipfile
from MTAssetLibrary import write_macro_files, make_directory_path

import os
from zipfile import ZipFile, is_zipfile, ZIP_DEFLATED
from lxml import objectify
import lxml, lxml.etree as etree
import logging as log
from io import StringIO

def GetAsset(whence, name=None, path=None):
    """Asset Generator

    Load the thing we were given to find out what kind of asset
    it is, then return that asset.
    """
    zf = None
    if not os.path.exists(whence):
        log.error(f"Cannot create an asset, {whence} not found.")

    # find the xml file
    # if we were given a zipfile, load the zipfile and content.xml 
    # to find out what we are. If we were loaded from another type
    # of file we find and load the xml.
    if is_zipfile(whence):
        zf = ZipFile(whence)
        content_xml = zf.open('content.xml')
    elif os.path.isdir(whence):
        content_xml = open(os.path.join(whence,'content.xml'))
    else:
        content_xml = open(whence)
        
    xml = objectify.parse(content_xml)

    if xml.getroot().tag == tagset.macro.tag:
        return MTMacroObj(whence, zf, content_xml.name, xml, name, path)
    if xml.getroot().tag == tagset.macroset.tag:
        return MTMacroSet(whence, zf, content_xml.name, xml, name, path)
    if xml.getroot().tag == tagset.token.tag:
        return MTToken(whence, zf, content_xml.name, xml, name, path)
    if xml.getroot().tag == tagset.properties.tag:
        return MTProperties(whence, zf, content_xml.name, xml, name, path)
    if xml.getroot().tag == tagset.campaign.tag:
        return MTCampaign(whence, zf, content_xml.name, xml, name, path)
    if xml.getroot().tag == tagset.project.tag:
        return MTProject(whence, zf, content_xml.name, xml, name, path)


class MTAsset:
    """
    A MapTool Asset class
    """
    def __init__(self, whence, zf=None, xmlfile=None, xml=None, name=None, path=None):
        self.whence = whence # file or directory this object loads
        self.zipfile = zf # zipfile object if whence is a zipfile
        self.xmlfile = xmlfile # path to xml file opened in GetAsset
        self.xml = xml # xml object
        self.given_name = name # output file prefix for saves
        self.output_dir = path or '.' # output directory prefix for saves

    @property
    def fromdir(self):
        if os.path.isdir(self.whence):
            return self.whence
        else:
            return os.path.dirname(self.xmlfile)

    @property
    def _loaded_from(self):
        if is_zipfile(self.whence):
            return 'assetTypeFile'
        if os.path.isdir(self.whence):
            if os.path.isfile(os.path.join(self.whence, 'content.xml')):
                return 'directoryWithContentFile'
        if os.path.isfile(self.whence):
            return self.whence + 'File'
        return None

    @property
    def tag(self): # return tag from xml
        """
        Return the current object's outer tag (xml name of the object)
        """
        return self.root.tag

    @property
    def is_token(self): # tag matches token tag
        """
        Return True if the tag matches a token tag
        """
        return self.tag == tagset.token.tag

    @property
    def is_properties(self): # tag matches properties tag
        """
        Return True if the tag matches a properties tag
        """
        return self.tag == tagset.properties.tag \
            or self.tag == 'campaignProperties'

    @property
    def is_macroset(self): # tag matches macro set tag
        """
        Return True if the tag matches a macro set tag
        """
        return self.tag == tagset.macroset.tag

    @property
    def is_project(self): # tag matches project tag
        """
        Return True if the tag matches a project tag
        """
        return self.tag == tagset.project.tag

    @property
    def is_macro(self): # tag matches macro tag
        """
        Return True if the tag matches a macro tag
        """
        return self.tag == tagset.macro.tag

    @property
    def is_campaign(self): # tag matches campaign tag
        """
        Return True if the tag matches a campaign tag
        """
        return self.tag == tagset.campaign.tag

    @property
    def isasset_type(self): # return tag object with ext, name, tag
        """
        Returns the Tag Type of the current object, the Tag
        contains a .ext, .name, and .tag attribute.
        """
        if self.is_token: return tagset.token
        if self.is_macroset: return tagset.macroset
        if self.is_properties: return tagset.properties
        if self.is_project: return tagset.project
        if self.is_macro: return tagset.macro
        if self.is_campaign: return tagset.campaign
        return None

    @property
    def root(self): # root element from xml
        """
        Return the root element in the xml for this object
        """
        return self.xml.getroot()

    @property
    def _from_dir(self): # return true if whence is a directory
        return os.path.isdir(self.whence)

    @property
    def dirname(self): # return directory of the xmlfile (naively)
        return os.path.dirname(self.xmlfile)

    @property
    def name(self):
        """
        Figure out the name of this object based on the file
        or attributes.  Each type of object may or may not have
        a name in a different place.

        If the object does not normally have a name, we can
        try to discover them from the filesystem name.

        This is the base object, which has a default name strategy.
        """
        if self.whence.endswith('content.xml'):
            return os.path.basename(os.path.dirname(self.whence))
        elif os.path.isdir(self.whence):
            return os.path.basename(self.whence)
        elif self.whence.endswith(tagset.properties.ext) or \
             self.whence.endswith(tagset.macroset.ext) or \
             self.whence.endswith(tagset.campaign.ext) or \
             self.whence.endswith(tagset.project.ext):
            return os.path.basename(os.path.splitext(self.whence)[0])
        else:
            return 'Generic' + self.isasset_type.name.capitalize()

    def best_name(self, save_name=None): # return best name from given, set, embedded
        if save_name:
            return save_name
        if self.given_name:
            return self.given_name
        if self.name:
            return str(self.name)
        return 'Generic' + self.isasset_type.name.capitalize()

    def best_name_escaped(self, save_name=None): # return best_name html escaped
        return MacroNameQuote(self.best_name(save_name))

    def assemble(self, save_name=None, output_dir=None, ext=None, dryrun=None, verbose=None):
        """
        MTAsset.assemble() method

        Returns None

        This will cause the asset to write itself to a file based on the
        maptool asset type.
        
            <output_dir>/<name>.<ext>

        Keyword Arguments:
        save_name (default None) - temporary change of name to the object (and resulting filename)
        dryrun (default None) - don't actually save anything
        verbose (default None) - print out debugging information normally logged
        """

        if not output_dir:
            output_dir = self.output_dir or '.'
        # print(f'{type(output_dir)=}')
        # print(f'{type(self.best_name(save_name))=}')
        
        save_file = os.path.join(output_dir,
                                 self.best_name(save_name))
        save_file += '.' + (ext or self.isasset_type.ext)

        log.debug(f'.save: opening {save_file} for output')
        
    def save_to(self, save_name=None, output_dir=None):
        output_dir = output_dir or self.output_dir or '.'
        output_dir = MacroNameQuote(output_dir)
        save_name = self.best_name_escaped(save_name)
        return os.path.join(output_dir, save_name)

    def extract(self, save_name=None, dryrun=None, verbose=None):
        """
        MTAsset.extract() method

        Returns None


        This will cause the asset to write itself to a directory and/or files based on the type:
            <save_name|Objec

        Keyword Arguments
        save_name (default object_name) - temporary change of name to the object (and resulting directory)
        dryrun (default None) - don't actually save anything
        verbose (default None) - print out debugging information normally logged
        """
        pass


class MTCampaign(MTAsset): pass


class MTProperties(MTAsset): pass


class MTToken(MTAsset):
    @property
    def name(self):
        return self.root.name

    def assemble(self, save_name=None, output_dir=None, ext=None, dryrun=None):
        """MTToken.assemble()

        Keyword Arguments:
        save_name
        output_dir
        ext
        dryrun
        verbose
        """
        if not output_dir:
            output_dir = self.output_dir or '.'
        save_file = os.path.join(output_dir,
                                 self.best_name_escaped(save_name))
        save_file += '.' + (ext or self.isasset_type.ext)
        if not dryrun:
            zf = ZipFile(save_file, mode='w', compression=ZIP_DEFLATED)
            add_directory_to_zipfile(zf, self.dirname)
        if self.xml.find('macroPropertiesMap') is not None:
            for i, entry in enumerate(self.root.macroPropertiesMap.entry):
                try:
                    name = entry.macro.attrib['name']
                except AttributeError:
                    pass
                else:
                    macrobase = os.path.join(self.dirname, name)
                    command_file = macrobase + '.command'
                    xml_file = macrobase + '.xml'
                    macro = objectify.parse(xml_file)
                    command = open(command_file, 'r').read()
                    macro.getroot().command = DataElement(command)
                    entry_template = '<entry><int>{}</int>{}</entry>'
                    new_entry = objectify.fromstring(
                        entry_template.format(
                                entry.int.text,
                                etree.tostring(macro).decode()))

                    self.root.macroPropertiesMap.entry[i] = new_entry
        if not dryrun:
            try:
                zf.writestr('content.xml',
                            etree.tostring(self.xml, pretty_print=True))
            finally:
                zf.close()

    def extract(self, save_name=None, output_dir=None, dryrun=None):
        """MTToken.extract()

        Keyword Arguments:
        save_name (None) - use this name instead of the name when loaded
        output_dir (None) - put the extracted Token in this path prefix
        dryrun (None) - don't actually do anything
        """
        # make the directory
        # extract the files from the zipfile into the directory
        #   exclude or plan to overwrite the content.xml
        # go through the content.xml, extracting the macros and leaving
        #   a placeholder
        # write the modified content.xml

        new_entry_template = '<entry><int>{}</int><macro name="{}"/></entry>'
        # make the directory if needed
        output_path = self.save_to(save_name, output_dir)
        if not dryrun:
            make_directory_path(output_path)
        
        # extract all the files from the zipfile into the directory
        log.info(f"extracting {self.best_name} to {output_path}")
        if not dryrun:
            self.zipfile.extractall(output_path)

        for i, entry in enumerate(self.root.macroPropertiesMap.entry):
            macro = entry[tagset.macro.tag]
            label = MacroNameQuote(macro.label.text)
            macrobase = os.path.join(output_path, label)
            if not dryrun:
                write_macro_files(macro, macrobase)

            # replace macro with placeholder in content.xml
            new_entry = new_entry_template.format(entry.int, label)
            new_entry = objectify.fromstring(new_entry)
            self.root.macroPropertiesMap.entry[i] = new_entry

        if not dryrun:
            XML2File(output_path, 'content.xml', self.xml)
  

# Disambiguate from MTMacro from MTAssetLibrary and 
# still have something to 
class MTMacroSet(MTAsset):
    @property
    def name(self):
        return os.path.basename(os.path.splitext(self.whence)[0])

    def append(self, thing):
        return self.root.append(thing)

class MTMacroObj(MTAsset):
    def __init__(self, *args, **kwargs):
        # whence, zf=None, xmlfile=None, xml=None, name=None, path=None):
        super().__init__(*args, **kwargs)
        # self.whence = whence # file or directory this object loads
        # self.zipfile = zf # zipfile object if whence is a zipfile
        # self.xmlfile = xmlfile # path to xml file opened in GetAsset
        # self.xml = xml # xml object
        # self.given_name = name # output file prefix for saves
        # self.output_dir = path # output directory prefix for saves

        # Special for MacroObjects loaded from xml files on disk
        # is to reassemble the extracted command file
        if not self._loaded_from == 'assetTypeFile':
            log.info('loading %s for the macro xml file' % self.whence)
            log.info('loading %s for the macro command file' % self.command_file)
            command = open(self.command_file).read()
            # reassemble the command into the xml
            self.xml.getroot().command = DataElement(command)


    @property
    def command_file(self):
        return os.path.splitext(self.whence)[0] + '.command'

    @property
    def name(self):
        """
        Macros have a label, return that for name
        """
        return self.root.label.text

    def assemble(self, save_name=None, output_dir=None, ext=None, dryrun=None, verbose=None):
        """MTMacroObj.assemble()

        write the macro object to <output_dir>/<save_name>.<ext>

        Keyword Arguments:
        save_name - the base name of the output file, defaults to the label
        output_dir - a directory for the output file, defaults to '.'
        ext - a new extension, defaults to mtmacro for MTMacroObj
        dryrun - if True, don't create anything, just log what you would do
        verbose - turn up logging to 'debug' for this run only
        """
        if not output_dir:
            output_dir = self.output_dir or '.'
        # print(f'{type(output_dir)=}')
        # print(f'{type(self.best_name(save_name))=}')
        
        save_file = os.path.join(output_dir,
                                 self.best_name_escaped(save_name))
        save_file += '.' + (ext or self.isasset_type.ext)

        log.debug(f'.assemble: creating {output_dir} if needed')
        if not dryrun and not os.path.isdir(output_dir):
            os.makedirs(output_dir)
        log.debug(f'.save: opening {save_file} for output')
        if not dryrun:
            zf = ZipFile(save_file, mode='w', compression=ZIP_DEFLATED)
            try:
                zf.writestr('content.xml',
                            etree.tostring(self.xml, pretty_print=True))
                zf.writestr('properties.xml', properties_xml)
            finally:
                zf.close()
            print_info(save_file)

    def append(self, new):
        """
        Appending to a macro should convert us to a macroset
        object, at least the object should identify as such
        and assemble should create a .mtmacset object (currently
        the latter is true, it doesn't actually cast us to the
        MTMacroSet object)
        """
        s = StringIO('<'+tagset.macroset.tag+'/>')
        newxml = objectify.parse(s)
        newxml.getroot().append(self.root)
        if type(new) == MTMacroObj:
            newxml.getroot().append(new.root)

        self.xml = newxml
        


class MTProject(MTAsset):
    pass
# junk.project xml file
# Dir/content.xml with net.rptools.maptool.model.CampaignProperties creates a .mtprops
# Dir/content.xml with net.rptools.maptool.model.Token creates a .rptok
# Dir/content.xml with net.rptools.maptool.util.PersistenceUtil_-PersistedCampaign creates a .cmpgn
# Dir/content.xml with list creates a .mtmacset
# *.xml with net.rptools.maptool.model.MacroButtonProperties creates a .mtmacro