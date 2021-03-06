""" File managing decorators managing who is logged in and not, as well as permission handling as well as functions decorated with before_app_request """

from flask import g, session, flash, redirect, url_for

import logging

from stuybulletin.models.permissions import Role
from stuybulletin.models.users import User

from stuybulletin.blueprints import auth_mod

import functools

import logging

LOG = logging.getLogger(__name__)

def parametrized(dec):
    """ Utility function to allow for decorators with arguments """
    def layer(*args, **kwargs):
        def repl(f):
            return dec(f, *args, **kwargs)
        return repl
    return layer

def email_in_organization(email = '', organization = ''):
    """ Checks whether an email is part of a specified organization 
    
    :param email: The email to check
    :type email: str
    :param organization: The organization to check
    :type organization: str
    :returns: True if the organization is part of the email and False if the organization is not part of the email
    """

    return organization == email.split('@')[1]

@auth_mod.before_app_request
def load_user():
    """ Loads the user from the session into the g variable 

    Runs before any request is passed to the appropriate view route using the flask before_app_request decorator

    If session does not contain id, sets g.user to None
    """
    
    user = None
    
    if 'id' in session:
        LOG.debug('Found the user')
        user = User.query.filter_by(id = session['id']).first()

    g.user = user
    #    LOG.debug(session['id'])
    LOG.debug(g.user)

def require_login(f):
    """ require_login(f)
    Authentication decorator

    :param f: The original view route, or, more generally, the method (perhaps another decorator), that will eventually return something for flask to display.
    :type f: function
    :returns: A rendered page to display, either through the view route that it is decorating, or a page with a flashed message.

    If user is logged in run the route

    If user is not logged in display a message to the user and redirect to the 'index' route
    """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if not g.user:
            LOG.debug('You are not logged in')
            flash('You are not logged in')
            return redirect(url_for('public.controller.index'))
        return f(*args, **kwargs)
    return wrapper

@parametrized
def require_role(f, role):
    """ require_role(f, role)
    Authentication decorator

    :param f: The original view route, or, more generally, the method (perhaps another decorator), that will eventually return something for flask to display.
    :type f: function
    :param role: The role to check
    :type role: str
    :returns: A rendered page to display, either through the view route that it is decorating, or a page with a flashed message.

    If the user has the requisite role, call the view route which this function decorates.

    If user does not have the requisite role, display a message to the user and redirect to the 'index' route
    """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if not g.user.check_role(role):
            flash('You do not have the required role')
            return redirect(url_for('public.controller.index'))
        return f(*args, **kwargs)
    return wrapper




