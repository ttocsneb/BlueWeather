

def dict_merge(a, b, leaf_merger=None):
    """
    Recursively deep-merges two dictionaries.
    Taken from
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

    if not isinstance(b, dict):
        return b
    result = deepcopy(a)
    for k, v in b.items():
        if k in result and isinstance(result[k], dict):
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


def dict_minimal_mergediff(source, target):
    """
    Recursively calculates the minimal dict that would be needed to be deep
    merged with a in order to produce the same result as deep merging a and b.
    Example::
        >>> a = dict(foo=dict(a=1, b=2), bar=dict(c=3, d=4))
        >>> b = dict(bar=dict(c=3, d=5), fnord=None)
        >>> c = dict_minimal_mergediff(a, b)
        >>> c == dict(bar=dict(d=5), fnord=None)
        True
        >>> dict_merge(a, c) == dict_merge(a, b)
        True
    Arguments:
        source (dict): Source dictionary
        target (dict): Dictionary to compare to source dictionary and derive
        diff for
    Returns:
        dict: The minimal dictionary to deep merge on ``source`` to get the
            same result as deep merging ``target`` on ``source``.
    """

    if not isinstance(source, dict) or not isinstance(target, dict):
        raise ValueError("source and target must be dictionaries")

    if source == target:
        # shortcut: if both are equal, we return an empty dict as result
        return dict()

    from copy import deepcopy

    all_keys = set(source.keys() + target.keys())
    result = dict()
    for k in all_keys:
        if k not in target:
            # key not contained in b => not contained in result
            continue

        if k in source:
            # key is present in both dicts, we have to take a look at the value
            value_source = source[k]
            value_target = target[k]

            if value_source != value_target:
                # we only need to look further if the values are not equal

                if isinstance(value_source, dict) and \
                        isinstance(value_target, dict):
                    # both are dicts => deeper down it goes into the rabbit
                    # hole
                    result[k] = dict_minimal_mergediff(value_source,
                                                       value_target)
                else:
                    # new b wins over old a
                    result[k] = deepcopy(value_target)

        else:
            # key is new, add it
            result[k] = deepcopy(target[k])
    return result
