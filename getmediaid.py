url = "https://www.instagram.com/p/B8iwlG9pXHI/"
# ----> use regexp to extract code from url
code = "B8iwlG9pXHI"

charmap = {
    'A': '0',
    'B': '1',
    'C': '2',
    'D': '3',
    'E': '4',
    'F': '5',
    'G': '6',
    'H': '7',
    'I': '8',
    'J': '9',
    'K': 'a',
    'L': 'b',
    'M': 'c',
    'N': 'd',
    'O': 'e',
    'P': 'f',
    'Q': 'g',
    'R': 'h',
    'S': 'i',
    'T': 'j',
    'U': 'k',
    'V': 'l',
    'W': 'm',
    'X': 'n',
    'Y': 'o',
    'Z': 'p',
    'a': 'q',
    'b': 'r',
    'c': 's',
    'd': 't',
    'e': 'u',
    'f': 'v',
    'g': 'w',
    'h': 'x',
    'i': 'y',
    'j': 'z',
    'k': 'A',
    'l': 'B',
    'm': 'C',
    'n': 'D',
    'o': 'E',
    'p': 'F',
    'q': 'G',
    'r': 'H',
    's': 'I',
    't': 'J',
    'u': 'K',
    'v': 'L',
    'w': 'M',
    'x': 'N',
    'y': 'O',
    'z': 'P',
    '0': 'Q',
    '1': 'R',
    '2': 'S',
    '3': 'T',
    '4': 'U',
    '5': 'V',
    '6': 'W',
    '7': 'X',
    '8': 'Y',
    '9': 'Z',
    '-': '$',
    '_': '_'
}

def instagram_code_to_media_id(code):
    # code = "B8iwlG9pXHI"
    id = ""
    for letter in code:
        id += charmap[letter]
  
    alphabet = list(charmap.values())
    number = 0
    for char in id:
        number = number * 64 + alphabet.index(char)

    return number

def getInstagramUrlFromMediaId(media_id):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
    shortened_id = ''

    while media_id > 0:
        remainder = media_id % 64
        # dual conversion sign gets the right ID for new posts
        media_id = (media_id - remainder) // 64;
        # remainder should be casted as an integer to avoid a type error. 
        shortened_id = alphabet[int(remainder)] + shortened_id

    return 'https://instagram.com/p/' + shortened_id + '/'
  
media_id = instagram_code_to_media_id("CwXIutptCzn")
print(media_id)
# print(media_id == 3128420490671065656)

print(getInstagramUrlFromMediaId(3176713886269711742))
print(getInstagramUrlFromMediaId(3128420490671065656))