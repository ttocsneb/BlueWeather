from collections import Mapping

def dict_merge(a, b, leaf_merger=None):
    """
    Recursively deep-merges two dictionaries.
    Taken from Octoprint, which was taken from
    https://www.xormedia.com/recursively-merge-dictionaries-in-python/
    Example::
        >>> a = dict(foo="foo", bar="bar", fnord=dict(a=1))
        >>> b = dict(foo="other foo", fnord=dict(b=2, l=["some", "list"]))
        >>> expected = dict(foo="other foo", bar="bar",
                            fnord=dict(a=1, b=2,l=["some", "list"]))
        >>> dict_merge(a, b) == expected
        True
        >>> dict_merge(a, None) == a
        True
        >>> dict_merge(None, b) == b
        True
        >>> dict_merge(None, None) == dict()
        True
        >>> def leaf_merger(a, b):
        ...     if isinstance(a, list) and isinstance(b, list):
        ...         return a + b
        ...     raise ValueError()
        >>> result = dict_merge(dict(l1=[3, 4], l2=[1], a="a"),
                                dict(l1=[1, 2], l2="foo", b="b"),
                                leaf_merger=leaf_merger)
        >>> result.get("l1") == [3, 4, 1, 2]
        True
        >>> result.get("l2") == "foo"
        True
        >>> result.get("a") == "a"
        True
        >>> result.get("b") == "b"
        True
    Arguments:
        a (dict): The dictionary to merge ``b`` into
        b (dict): The dictionary to merge into ``a``
        leaf_merger (callable): An optional callable to use to merge leaves (
            non-dict values)
    Returns:
        dict: ``b`` deep-merged into ``a``
    """

    from copy import deepcopy

    if a is None:
        a = dict()
    if b is None:
        b = dict()

    if not isinstance(b, Mapping):
        return b
    result = deepcopy(a)
    for k, v in b.items():
        if k in result and isinstance(result[k], Mapping):
            result[k] = dict_merge(result[k], v, leaf_merger=leaf_merger)
        else:
            merged = None
            if k in result and callable(leaf_merger):
                try:
                    merged = leaf_merger(result[k], v)
                except ValueError:
                    # can't be merged by leaf merger
                    pass

            if merged is None:
                merged = deepcopy(v)

            result[k] = merged
    return result
