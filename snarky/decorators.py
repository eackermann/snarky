"""Snarky behavioral decorators.
Decorators define behaviors that are involed when jk==True.
"""

import time # TODO: don't need to load it if not necessary... let user only load specifics

__all__ = ['test',
           'snarky',
           'snarkyvoice',
           'say_time']

def test(fun):
    """"""
    def wrapper(*args, **kwargs):
        jk = kwargs.pop('jk', None)

        # before function call:
        if jk:
            text = "Shay, Shayok, or Shayoghurt. It's all the same to me..."
            print(text)

        # function call:
        out = fun(*args, **kwargs)

        # after function call:
        if jk:
            text = "Just kidding..."
            print(text)
        return out
    return wrapper

def snarky(fun):
    """"""
    def wrapper(*args, **kwargs):
        jk = kwargs.pop('jk', None)

        # before function call:
        if jk:
            text = "Shay, Shayok, or Shayoghurt. It's all the same to me..."
            print(text)

        # function call:
        out = fun(*args, **kwargs)

        # after function call:
        if jk:
            text = "Just kidding..."
            print(text)
        return out

    return wrapper

def snarkyvoice(fun):
    """"""
    from google_speech import Speech
    lang = "en"
    def wrapper(*args, **kwargs):
        jk = kwargs.pop('jk', None)

        # before function call:
        if jk:
            text = "Shay, Shayok, or Shayoghurt. It's all the same to me..."
            speech = Speech(text, lang)
            speech.play(None)

         # function call:
        out = fun(*args, **kwargs)

        # after function call:
        if jk:
            text = "Just kidding..."
            speech = Speech(text, lang)
            speech.play(None)
        return out
#             # you can also apply audio effects (using SoX)
#             # see http://sox.sourceforge.net/sox.html#EFFECTS for full effect documentation
#             sox_effects = ("speed", "1.5")
#             speech.play(sox_effects)
    return wrapper

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