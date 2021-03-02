from docker.MTAssetLibrary.utils import random_string
import sys
sys.path.insert(0, 'docker')

import os
import random
import string
import lxml
from lxml import objectify
import logging as log
from behave import given, when, then
import zipfile
from subprocess import Popen, PIPE
from MTAssetLibrary import maptool_macro_tags as tagset

# the noqa: F811 turns off complaining that the function is redefined.
# In behave, common usage is to use step_impl as the function in each
# step.  They don't have to be, but they also don't have to have unique
# or any other predefined name pattern.

@given('I have a test token dir')  # noqa: F811
def step_impl(context):
    assert os.path.exists(context.tokenpath)

@given(u'I have two base macros')  # noqa: F811
def step_impl(context):
    assert os.path.exists(context.macro1['xml'])
    assert os.path.exists(context.macro2['xml'])


@given(u'I have a base properties dir')  # noqa: F811
def step_impl(context):
    assert os.path.exists(context.proppath)


@given(u'I have a base project file')  # noqa: F811
def step_impl(context):
    assert os.path.exists(context.projpath)

    
@given('I have the assemble command')  # noqa: F811
def step_impl(context):
    assert os.path.exists('docker/assemble')
    assert os.access('docker/assemble', os.X_OK)
    context.assemble = 'docker/assemble'


@when('I call the assemble command with that test token dir')  # noqa: F811
def step_impl(context):
    p = Popen(['./docker/assemble', context.tokenpath],
        stderr=PIPE, stdout=PIPE, close_fds=True)
    context.stdout, context.stderr = p.communicate()
    assert b'Error' not in context.stderr, context.stderr


@when(u'I call the assemble command with two or more macros as input and an output directory')  # noqa: F811
def step_impl(context):
    p = Popen(['./docker/assemble', context.macro1['path'], context.macro2['path'], '--name',
        context.macrosetRandomName, '--output', context.temp_directory],
        stderr=PIPE, stdout=PIPE, close_fds=True)
    context.stdout, context.stderr = p.communicate()
    assert b'Error' not in context.stderr, context.stderr


@then(u'I should get an output directory')  # noqa: F811
def step_impl(context):
    assert os.path.exists(context.temp_directory)
    assert os.path.isdir(context.temp_directory)


@then(u'a named macroset')  # noqa: F811
def step_impl(context):
    ptf = os.path.join(context.temp_directory, context.macrosetRandomName)
    ptf = ptf + '.mtmacset'
    assert os.path.exists(ptf), f'Expected macroset {ptf} does not exist.  {os.listdir(context.temp_directory)=}'
    assert os.path.isfile(ptf), 'Expected macroset %s is not a file' % ptf

@then(u'I will have a Token file')  # noqa: F811
def step_impl(context):
    assert os.path.exists(context.tokenfilename), f'{os.listdir(".")=}'

@then(u'the Token file will be a zipfile')  # noqa: F811
def step_impl(context):
    assert zipfile.is_zipfile(context.tokenfilename)
    context.zf = zipfile.ZipFile(context.tokenfilename)

@then(u'the Token file will contain a content.xml')  # noqa: F811
def step_impl(context):
    assert 'content.xml' in [x.filename for x in  context.zf.filelist]
    context.contentfile = context.zf.open('content.xml')

@then(u'the Asset content.xml will be a "{tag}"')  # noqa: F811
def step_impl(context, tag):
    context.xml = objectify.parse(context.contentfile)
    assert context.xml.getroot().tag == tag

@when(u'I assemble that Token specifying output')  # noqa: F811
def step_impl(context):
    p = Popen(['./docker/assemble', context.tokenpath, '--output', context.temp_directory],
        stderr=PIPE, stdout=PIPE, close_fds=True)
    context.stdout, context.stderr = p.communicate()
    assert b'Error' not in context.stderr, context.stderr

@then(u'I will have a Token file in the output')  # noqa: F811
def step_impl(context):
    assert os.path.exists(os.path.join(context.temp_directory, context.tokenfilename))

@when(u'I call assemble without an argument')  # noqa: F811
def step_impl(context):
    p = Popen(['./docker/assemble'],
        stderr=PIPE, stdout=PIPE, close_fds=True)
    context.stdout, context.stderr = p.communicate()
    assert b'Error' not in context.stderr, context.stderr

@then(u'I get an error message about required input')  # noqa: F811
def step_impl(context):
    assert b'arguments are required' in context.stderr

@when(u'I call assemble on the Token Dir verbosely')  # noqa: F811
def step_impl(context):
    if os.path.exists(context.tokenfilename):
        os.remove(context.tokenfilename)
    assert not os.path.exists(context.tokenfilename)
    p = Popen(['./docker/assemble', context.tokenpath, '--verbose'],
        stderr=PIPE, stdout=PIPE, close_fds=True)
    context.stdout, context.stderr = p.communicate()
    assert b'Error' not in context.stderr, context.stderr

@then(u'I should get more verbose output')  # noqa: F811
def step_impl(context):
    assert b"INFO: Verbose output." in context.stderr

@then(u'It builds the Token')  # noqa: F811
def step_impl(context):
    assert os.path.exists(context.tokenfilename)

@when(u'I call assemble with a Macro name')  # noqa: F811
def step_impl(context):
    p = Popen(['./docker/assemble', context.macro1['path']],
        stderr=PIPE, stdout=PIPE, close_fds=True)
    context.stdout, context.stderr = p.communicate()
    assert b'Error' not in context.stderr, context.stderr

@then(u'I should get a mtmacro asset')  # noqa: F811
def step_impl(context):
    macrofile = context.macro1['macrofilename']
    assert os.path.exists(macrofile)
    context.zf = zipfile.ZipFile(macrofile)

@then(u'that Macro should contain a content.xml')  # noqa: F811
def step_impl(context):
    assert 'content.xml' in [x.filename for x in  context.zf.filelist]
    context.contentfile = context.zf.open('content.xml')

@when(u'I call assemble with a Macro XML FileName')  # noqa: F811
def step_impl(context):
    p = Popen(['./docker/assemble', context.macro1['xml']],
        stderr=PIPE, stdout=PIPE, close_fds=True)
    context.stdout, context.stderr = p.communicate()
    assert b'Error' not in context.stderr, context.stderr

@when(u'I call assemble with a Macro Command File Name')  # noqa: F811
def step_impl(context):
    p = Popen(['./docker/assemble', context.macro1['command']],
        stderr=PIPE, stdout=PIPE, close_fds=True)
    context.stdout, context.stderr = p.communicate()
    assert b'Error' not in context.stderr, context.stderr

@when(u'I call assemble with a Properties directory name')  # noqa: F811
def step_impl(context):
    p = Popen(['./docker/assemble', context.proppath],
        stderr=PIPE, stdout=PIPE, close_fds=True)
    context.stdout, context.stderr = p.communicate()
    assert b'Error' not in context.stderr, context.stderr

@then(u'I should get a mtprops asset')  # noqa: F811
def step_impl(context):
    assert os.path.exists(context.propfilename), f'{context.propfilename} does not exist'

@then(u'the Properties file will be a zipfile')  # noqa: F811
def step_impl(context):
    assert zipfile.is_zipfile(context.propfilename)
    context.zf = zipfile.ZipFile(context.propfilename)

@then(u'that mtprops should contain a content.xml')  # noqa: F811
def step_impl(context):
    assert 'content.xml' in [x.filename for x in  context.zf.filelist]
    context.contentfile = context.zf.open('content.xml')

@when(u'I call assemble with a Project file name')  # noqa: F811
def step_impl(context):
    p = Popen(['./docker/assemble', context.projpath],
        stderr=PIPE, stdout=PIPE, close_fds=True)
    context.stdout, context.stderr = p.communicate()
    context.projcontents = open(context.projpath).read()
    assert b'Error' not in context.stderr, f'{context.stderr=} {context.stdout=}'

@when(u'that Project contains a macroset')  # noqa: F811
def step_impl(context):
    assert 'macroset' in context.projcontents
    
@when(u'that Project contains a token')  # noqa: F811
def step_impl(context):
    assert '<token' in context.projcontents

@when(u'that Project contains a Properties')  # noqa: F811
def step_impl(context):
    assert '<properties' in context.projcontents

@then(u'I should get a macroset file')  # noqa: F811
def step_impl(context):
    context.macrofilename = 'MVMacroSet.' + tagset.macroset.ext
    assert os.path.exists(context.macrofilename), f'{context.macrofilename} does not exist after building {context.projpath} with {context.stderr=} and {context.stdout=}'

@then(u'that macroset should contain a content.xml')  # noqa: F811
def step_impl(context):
    zf = zipfile.ZipFile('MVMacroSet.' + tagset.macroset.ext)
    assert 'content.xml' in [x.filename for x in  zf.filelist]
    context.contentfile = zf.open('content.xml')

@then(u'the Asset content.xml will be a list')  # noqa: F811
def step_impl(context):
    context.xml = objectify.parse(context.contentfile)
    assert context.xml.getroot().tag == tagset.macroset.tag

@then(u'I should get a token file')  # noqa: F811
def step_impl(context):
    filename = 'MVToken+1.' + tagset.token.ext
    assert os.path.exists(filename), f'{filename} does not exist'

@then(u'that token should contain a content.xml')  # noqa: F811
def step_impl(context):
    zf = zipfile.ZipFile('MVToken+1.rptok')
    assert 'content.xml' in [x.filename for x in  zf.filelist]
    context.contentfile = zf.open('content.xml')

@then(u'I should get a properties file')  # noqa: F811
def step_impl(context):
    assert os.path.exists(context.propfilename)

@then(u'that properties file should be a zipfile')  # noqa: F811
def step_impl(context):
    assert zipfile.is_zipfile(context.propfilename)
    context.zf = zipfile.ZipFile(context.propfilename)

@then(u'that properties file should contain a content.xml')  # noqa: F811
def step_impl(context):
    assert 'content.xml' in [x.filename for x in  context.zf.filelist]
    context.contentfile = context.zf.open('content.xml')

@when(u'I call assemble with a Project file name and output directory')  # noqa: F811
def step_impl(context):
    p = Popen(['./docker/assemble', context.projpath, '--output', context.temp_directory],
        stderr=PIPE, stdout=PIPE, close_fds=True)
    context.stdout, context.stderr = p.communicate()
    context.projcontents = open(context.projpath).read()
    assert b'Error' not in context.stderr, context.stderr

@then(u'I should get a macroset file in the output directory')  # noqa: F811
def step_impl(context):
    macrosetfile = os.path.join(context.temp_directory, 'MVMacroSet.' + tagset.macroset.ext)
    assert os.path.exists(macrosetfile), f'{macrosetfile} not found in {context.temp_directory} {os.listdir()=} {os.listdir(context.temp_directory)=}'

@then(u'I should get a token file in the output directory')  # noqa: F811
def step_impl(context):
    tokenfile = os.path.join(context.temp_directory, 'MVToken+1.' + tagset.token.ext)
    assert os.path.exists(tokenfile), f'{tokenfile} not found in {context.temp_directory} {os.listdir()=} {os.listdir(context.temp_directory)=}'

@then(u'I should get a properties file in the output directory')  # noqa: F811
def step_impl(context):
    propfile = os.path.join(context.temp_directory, 'MVProps.' + tagset.properties.ext)
    assert os.path.exists(propfile), f'{propfile} not found in {context.temp_directory} {os.listdir()=} {os.listdir(context.temp_directory)=}'
    context.zf = zipfile.ZipFile(propfile)

@given(u'I start with an extracted Token')
def step_impl(context):
    assert os.path.exists(context.tokenpath)

@when(u'I assemble that Token')
def step_impl(context):
    p = Popen(['./docker/assemble', context.tokenpath],
        stderr=PIPE, stdout=PIPE, close_fds=True)
    context.stdout, context.stderr = p.communicate()
    context.projcontents = open(context.projpath).read()
    assert b'Error' not in context.stderr, context.stderr

@when(u'that token is in a clean checkout')
def step_impl(context):
    raise NotImplementedError(u'STEP: When that token is in a clean checkout')  # noqa: F811

@when(u'that checkout is not based on a Tag')
def step_impl(context):
    raise NotImplementedError(u'STEP: When that checkout is not based on a Tag')  # noqa: F811

@then(u'the assembled token will have a gmName of [hash]')  # noqa: F811
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the assembled token will have a gmName of [hash]')

@then(u'the token\'s macros will have an html comment of "https://github.com/mr-ice/maptool-macros/ [hash]" replacing a previous comment in that format')  # noqa: F811
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the token\'s macros will have an html comment of "https://github.com/mr-ice/maptool-macros/ [hash]" replacing a previous comment in that format')

@given(u'A project with a text element')
def step_impl(context):
    assert os.path.exists(context.projecttextfile)

@when(u'I call the assemble command with the project/text structure')  # noqa: F811
def step_impl(context):
    p = Popen(['./docker/assemble', context.projecttextfile],
        stderr=PIPE, stdout=PIPE, close_fds=True)
    context.stdout, context.stderr = p.communicate()
    assert b'Error' not in context.stderr, context.stderr

@then(u'I should get a text file')  # noqa: F811
def step_impl(context):
    assert os.path.exists(context.textfile)

@then(u'the text file should contain my content')  # noqa: F811
def step_impl(context):
    assert context.random_text in open(context.textfile).read()

@given(u'A project with a project element')
def step_impl(context):
    assert os.path.exists(context.projectprojectfile)
    assert os.path.exists(context.projectfile)

@when(u'I call the assemble command with the project/project structure')
def step_impl(context):
    p = Popen(['./docker/assemble', context.projectprojectfile],
        stderr=PIPE, stdout=PIPE, close_fds=True)
    context.stdout, context.stderr = p.communicate()
    assert b'Error' not in context.stderr, context.stderr

@then(u'I should get a text file from the embedded project')
def step_impl(context):
    assert os.path.exists(context.textfile), f'{context.textfile} does not exist'

@then(u'that text file should contain the embedded content')
def step_impl(context):
    assert context.project_random_text in open(context.textfile).read()
