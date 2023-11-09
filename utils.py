
def item_type_convert(item_type):
    types = {
        'M':'MINIFIG',
        'MINIFIG':'M',
        'S':'SET',
        'SET':'S'
    }
    return types[item_type]

def clean_html_codes(string:str) -> str:
    codes = {
        '&#41;': ')',
        '&#40;': '(',
        '&#39;': "'"
    }
    for html, char in codes.items():
        if html in string:
            string = string.replace(html, char)
    return string