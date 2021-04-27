# coding=utf-8
import os
import sys
import base64
import hashlib
import pkgutil
import getopt
import json

from bs4 import BeautifulSoup
from Crypto.Cipher import AES


class AESCrypt(object):
    LEN = 32

    def __init__(self, key: str):
        self.key = key.encode()
        self.mode = AES.MODE_CBC

    def encrypt(self, text: bytes):
        cryptor = AES.new(self.key, self.mode, self.key[16:])
        padlen = AESCrypt.LEN - len(text) % AESCrypt.LEN
        padlen = padlen if padlen != 0 else AESCrypt.LEN
        text += (chr(padlen)*padlen).encode('utf8')

        return cryptor.encrypt(text)


def main():
    scriptURL = "https://cdnjs.cloudflare.com/ajax/libs/crypto-js/4.0.0/crypto-js.js"
    placeholder = "This article is encrypted with a password, please goto the original webpage to check it out."
    identifier = "--- DON'T MODIFY THIS LINE ---"
    destination = "public"

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:",
                                   ["scriptURL=", "destination="])
    except getopt.GetoptError:
        print('hugo_enc --scriptURL <scriptURL>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('hugo_enc --scriptURL <scriptURL>')
            sys.exit()
        elif opt in ("--scriptURL"):
            scriptURL = arg
            print('=> scriptURL =', scriptURL)
        elif opt in ("--destination"):
            destination = arg
            print('=> destination =', destination)

    if not os.path.exists(destination):
        sys.exit("[!] No destination directory '{}' found!\n[!] No files processed.".format(destination))

    for dirpath, dirnames, filenames in os.walk(destination):
        for filename in filenames:
            fullpath = os.path.join(dirpath, filename)
            if filename.lower().endswith('.html'):
                soup = BeautifulSoup(open(fullpath, 'rb'), 'lxml')
                blocks = soup.findAll(
                    'div', {'class': 'hugo-enc-cipher-text'})

                if blocks:
                    print("[+] Processing '{}'".format(fullpath))

                    for block in blocks:
                        md5 = hashlib.md5()
                        if block.find("span"):
                            try:
                                md5.update(
                                    block['data-password'].encode('utf-8'))
                                key = md5.hexdigest()
                                cryptor = AESCrypt(key)
                                text = ''.join(map(str, block.contents))
                                written = base64.b64encode(
                                    cryptor.encrypt(text.encode('utf8')))

                                del block['data-password']
                                block.string = written.decode()
                            except KeyError:
                                print("\tNo Password found")
                        else:
                            print("\tAlready Processed")

                    # append decryption scripts
                    soup.body.append(
                        soup.new_tag("script", src=scriptURL))

                    soup.body.append("\n")
                    script_tag = soup.new_tag("script")

                    decoder_script = pkgutil.get_data(
                        'hugo_enc', 'decoder_script.js').decode('utf8')

                    script_tag.string = "\n" + decoder_script
                    soup.body.append(script_tag)
                    soup.body.append("\n")

                    with open(fullpath, 'w') as f:
                        html = str(soup)
                        f.write(str(soup))
            elif filename.lower().endswith('.xml'):
                soup = BeautifulSoup(open(fullpath, 'rb'), 'xml')
                print("[+] Processing '{}'".format(fullpath))
                items = soup('item')

                for item in items:
                    link = item('link')[0]
                    description = item('description')[0]

                    if description.string:
                        if identifier in description.string:
                            description.string.replace_with(str(placeholder))
                            print("\tProcessed for: {}".format(link.string))
                        elif placeholder in description.string:
                            print("\tAlready Processed")

                with open(fullpath, 'w') as f:
                    f.write(str(soup))

            elif filename.lower().endswith('.json'):
                print("[+] Processing '{}'".format(fullpath))

                data = None
                try:
                    with open(fullpath) as f:
                        data = json.load(f)

                    for x in data:
                        for y in x:
                            if identifier in x[y]:
                                x[y] = placeholder
                except Exception as e:
                    print("\t[!] {}: {}".format(type(e).__name__, e))
                finally:
                    if data:
                        with open(fullpath, "w") as f:
                            json.dump(data, f, indent=4)
