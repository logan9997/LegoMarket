
def item_type_convert(item_type):
    types = {
        'M':'MINIFIG',
        'MINIFIG':'M',
        'S':'SET',
        'SET':'S'
    }
    return types[item_type]
