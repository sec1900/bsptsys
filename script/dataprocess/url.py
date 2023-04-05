from urllib.parse import quote
from urllib.parse import unquote
import argparse



def urlcode(text):
    texten = quote(text, 'utf-8')
    textde = unquote(text, 'utf-8')
    print("url加密内容:")
    print(texten + "<br>")
    print("url解密内容:")
    print(textde + "<br>")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--text', type=str)
    args = parser.parse_args()
    print(urlcode(args.text))
