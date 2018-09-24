

def increment_revision(title):
    """
    Increment revision n. at the end of the given title:

        "abc" --> "abc (2)"
        "abc (2)" --> "abc (3)"
        etc ..

    Used for cloning objects
    """

    new_title = ''
    try:
        start = title.rfind('(')
        if title.endswith(')') and start >= 0:
            n = int(title[start + 1:-1])
            new_title = title[:start].strip() + ' (%d)' % (n + 1)
    except:
        pass

    if len(new_title) <= 0:
        new_title = title + ' (2)'

    return new_title
