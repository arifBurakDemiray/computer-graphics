

from .polygon import Edge


def add_generic(list,entity) -> int:
    try:
        return list.index(entity)
    except ValueError:
        list.append(entity)
        return len(list) - 1