# CENG 487 Assignment4 by
# Arif Burak Demiray
# December 2021


def add_generic(list, entity) -> int:
    try:
        return list.index(entity)
    except ValueError:
        list.append(entity)
        return len(list) - 1
