import os
import shutil
from behave import fixture, use_fixture
from behave.fixture import use_fixture_by_tag
from zipfile import ZipFile
from shutil import rmtree
import logging as log

log.debug("In environment.py")

@fixture
def base_rptok(context):
    """This defines a few variables to use in our BDD tests"""
    context.tokenpath = 'BaseToken30957877'
    context.tokenname = 'Base Token 30957877'
    context.tokenfilename = 'Base+Token+30957877'
    context.tokensrc = 'test/data/DNDB-Test/BaseToken30957877.zip'
    yield context.tokenpath
    try:
        # if we 'assembled' a token, remove it
        os.remove(context.tokenpath + '.rptok')
        os.remove(context.tokenfilename + '.rptok')
    except Exception as e:
        # avoid flake warning for not using e
        if e is not None:
            pass
        pass


@fixture
def base_token(context):
    """This extracts a base token for use by our BDD tests"""
    log.debug("In environment.base_token")
    use_fixture(base_rptok, context)
    log.debug("os.getcwd() = " + os.getcwd())
    log.debug("context.tokenpath = " + context.tokenpath)
    zf = ZipFile(context.tokensrc)
    zf.extractall()
    yield context.tokenpath
    try:
        rmtree(context.tokenpath)
    except Exception as e:
        pass


@fixture
def base_macro1(context):
    """This extracts a minimum viable macro for testing"""
    log.debug("In environment.base_macro")
    context.macropath = 'macro/MVMacro1'
    context.macroname = 'MVMacro1'
    context.macrosrc = 'test/data/MinViable/MVMacro1.zip'
    zf = ZipFile(context.macrosrc)
    zf.extractall()
    yield context.macropath
    if os.path.exists(context.macropath + '.xml'):
        os.remove(context.macropath + '.xml')
    if os.path.exists(context.macropath + '.command'):
        os.remove(context.macropath + '.command')


@fixture
def base_macro2(context):
    """This extracts a minimum viable macro for testing"""
    log.debug("In environment.base_macro")
    context.macropath = 'macro/MVMacro2'
    context.macroname = 'MVMacro2'
    context.macrosrc = 'test/data/MinViable/MVMacro2.zip'
    zf = ZipFile(context.macrosrc)
    zf.extractall()
    yield context.macropath
    if os.path.exists(context.macropath + '.xml'):
        os.remove(context.macropath + '.xml')
    if os.path.exists(context.macropath + '.command'):
        os.remove(context.macropath + '.command')

@fixture
def base_properties(context):
    """This unpacks the MVProperties"""
    log.debug("In environment.base_properties")
    context.proppath = 'MVProps'
    context.propname = 'MVProps'
    context.propsrc = 'test/data/MinViable/MVProps.zip'
    zf = ZipFile(context.propsrc)
    zf.extractall()
    yield context.proppath
    if os.path.exists(context.proppath):
        shutil.rmtree(context.proppath)


@fixture
def base_project(context):
    """This creates a project file for testing"""
    use_fixture(base_token, context)
    use_fixture(base_macro1, context)
    use_fixture(base_macro2, context)
    context.projpath = 'MVProject.project'
    context.projname = 'MVProject'
    context.projsrc = 'test/data/MinViable/MVProject.zip'
    zf = ZipFile(context.projsrc)
    zf.extractall()
    yield context.projsrc
    if os.path.exists(context.projpath):
        os.remove(context.projpath)


# Why is this so stupid in behave?  fixture should automatically
# register these so we don't have to.   I tried with fixture(name=)
FixtureRegistry = {
    "fixture.base_token": base_token,
    "fixture.base_rptok": base_rptok,
    "fixture.base_macro1": base_macro1,
    "fixture.base_macro2": base_macro2,
    "fixture.base_properties": base_properties,
    "fixture.base_project": base_project,
}


def before_tag(context, tag):
    log.debug("In environment.before_tag")
    if tag.startswith('fixture.'):
        return use_fixture_by_tag(tag, context, FixtureRegistry)
