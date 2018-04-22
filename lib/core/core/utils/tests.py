from functools import wraps


def raises(exception, msg=None):
    valid = exception.__name__

    def decorate(func):
        name = func.__name__

        def newfunc(*arg, **kw):
            try:
                func(*arg, **kw)
            except exception as e:
                if msg and str(e) != msg:
                    raise AssertionError(
                        "Exception msg '%s' does't match '%s'" % (str(e), msg)
                    )
            else:
                message = "%s() did not raise %s" % (name, valid)
                raise AssertionError(message)
        newfunc = wraps(func)(newfunc)
        return newfunc
    return decorate
