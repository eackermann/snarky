def myDecorator(fun):
    def wrapper(*args, **kwargs):
        print('before ' + fun.__name__)
        out = fun(*args, **kwargs)
        print('after ' + fun.__name__)
        return out
    return wrapper

def decorate_class(cls, *, exclude=[], decorator):
    for attr in cls.__dict__:
        if callable(getattr(cls, attr)) and attr not in exclude:
            setattr(cls, attr, decorator(getattr(cls, attr)))
    return cls

def decorate_module(mod, *, exclude=[], decorator):
    for attr in mod.__dict__:
        if str(mod.__dict__[attr].__class__) == "<class 'type'>" and attr not in exclude:
            mod.__dict__[attr] = decorate_class(mod.__dict__[attr], decorator=decorator)
        elif str(mod.__dict__[attr].__class__) == "<class 'abc.ABCMeta'>" and attr not in exclude:
            pass
#             mod.__dict__[attr] = decorate_class(mod.__dict__[attr], decorator=decorator)
        elif str(mod.__dict__[attr].__class__) == "<class 'module'>":
            pass
        elif str(mod.__dict__[attr].__class__) == "<class 'function'>":
            pass
        else:
            pass
    return mod