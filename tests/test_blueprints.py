""" Tests all blueprints """

import importlib

from flask import Blueprint
import pytest

from stuybulletin.blueprints import _factory, all_blueprints

def test_blueprint_instances():
    """ Ensures all blueprints are configured correctly 
    
    They must be instances of Blueprint, the url_prefixs must be set correctly, and that the view modules are defined correctly (starting with stuybulletin.views.
    """
    
    assert all([isinstance(bp, Blueprint) for bp in all_blueprints])
    assert len(all_blueprints) == len(set([bp.url_prefix for bp in all_blueprints if bp.url_prefix]))
    assert all([b.import_name.startswith('stuybulletin.views.') for b in all_blueprints])

def test_importable():
    """ Ensures the view modules for all blueprints are able to be imported """

    for bp in all_blueprints:
        importlib.import_module(bp.import_name)

def test_factory():
    """ Tests the blueprint factory

    Creates a test blueprint
    Ensures that the import name is correct
    Ensures that the url_prefix is correct
    """
    
    bp = _factory('public.controller', '/test/123')
    assert 'stuybulletin.views.public.controller' == bp.import_name
    assert '/test/123' == bp.url_prefix
