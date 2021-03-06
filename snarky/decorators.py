"""Snarky behavioral decorators.
Decorators define behaviors that are involed when jk==True.
"""
from functools import wraps
from random import randint

from . import messages

import time # TODO: don't need to load it if not necessary... let user only load specifics

__all__ = ['snarky',
           'snarkyvoice',
           'say_time']

# See https://stackoverflow.com/questions/5929107/decorators-with-parameters; still confused?
# See https://www.pydanny.com/python-partials-are-fun.html
# from functools import partial

# def _pseudo_decor(fun, argument):
#     def ret_fun(*args, **kwargs):
#         #do stuff here, for eg.
#         print ("decorator arg is %s" % str(argument))
#         return fun(*args, **kwargs)
#     return ret_fun

# real_decorator = partial(_pseudo_decor, argument=arg)

# @real_decorator
# def foo(*args, **kwargs):
#     pass

def snarky(*args, run_anyway=False):
    """Snarky text reaction when using the jk=True keyword argument."""
    no_args = False
    assert len(args) <2, "'run_anyway' is the only argument allowed!"
    if len(args) == 1 and not run_anyway and callable(args[0]):
        # We were called without args
        no_args = True
        fun = args[0]

    def outer(fun):
        @wraps(fun)
        def inner(*args, **kwargs):
            jk = kwargs.pop('jk', None)
            # before function call:
            if jk:
                text = "LOL! Then why are you asking me to run '" + fun.__name__ + "'? Unbelievable!"
                print(text)

            # function call:
            if run_anyway or not jk:
                out = fun(*args, **kwargs)
            else:
                out = None

            # after function call:
            if jk:
                message_idx = randint(0, len(messages.default)-1)
                text = messages.default[message_idx]
                print(text)
            return out
        return inner

    if no_args:
        return outer(fun)
    else:
        return outer

def snarkyvoice(*args, lang='en', sox=None, run_anyway=False):
    """Snarky text-to-speech reaction when using the jk=True keyword argument.

        # you can also apply audio effects (using SoX)
        # see http://sox.sourceforge.net/sox.html#EFFECTS for full effect documentation
        sox_effects = ("speed", "1.5")
        speech.play(sox_effects)
    """

    from google_speech import Speech

    if sox:
        raise NotImplementedError('SoX support has not been implemented yet...')

    no_args = False
    assert len(args) <2, "no positional arguments are supported!"
    if len(args) == 1 and not run_anyway and callable(args[0]):
        # We were called without args
        no_args = True
        fun = args[0]

    def outer(fun):
        @wraps(fun)
        def inner(*args, **kwargs):
            jk = kwargs.pop('jk', None)
            # before function call:
            if jk:
                text = "LOL! Then why are you asking me to run '" + fun.__name__ + "'? Unbelievable!"
                speech = Speech(text, lang)
                speech.play(None)

            # function call:
            if run_anyway or not jk:
                out = fun(*args, **kwargs)
            else:
                out = None

            # after function call:
            if jk:
                message_idx = randint(0, len(messages.default)-1)
                text = messages.default[message_idx]
                speech = Speech(text, lang)
                speech.play(None)
            return out
        return inner

    if no_args:
        return outer(fun)
    else:
        return outer

def say_time(fun):
    """
    Outputs the time a function takes
    to execute.
    """

    from google_speech import Speech
    lang = "en"

    def wrapper(*args, **kwargs):
        t1 = time.time()
        out = fun(*args, **kwargs)
        t2 = time.time()
        text = "It took " + str((t2 - t1)) + " to run the function."
        print(text)
        speech = Speech(text, lang)
        speech.play(None)
        return out
    return wrapper

def custom_response(*, before=None, after=None):
    """Build a custom response decorator.

    Params
    ======
    before: callable, optional
        A callable function which will be executed before entering the calling
        function. Default does nothing.
    after: callable, optional
        A callable function which will be executed after leaving the calling
        function. Default does nothing.

    Returns
    =======
    decorator: function
        A decorator function implementing the custom before and after actions.

    Example
    =======

    >>> def after():
    >>>     print('I regret doing that...')

    >>> my_response = snarky.decorators.custom_response(after=after)

    >>> @my_response
    >>> def my_fun(a,b):
    >>>    return a*b
    """

    def do_nothing():
        pass

    if not before:
        before = do_nothing

    if not after:
        after = do_nothing

    def decorator(fun):
        """Snarky text reaction when using the jk=True keyword argument."""
        def wrapper(*args, **kwargs):
            jk = kwargs.pop('jk', None)

            # before function call:
            if jk:
                before()

            # function call:
            out = fun(*args, **kwargs)

            # after function call:
            if jk:
                after()
            return out
        return wrapper
    return decorator