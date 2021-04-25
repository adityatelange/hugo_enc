# coding=utf-8
import os
import sys
import base64
import hashlib
import pkgutil
import getopt

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
    scriptURL = "https://cdnjs.cloudflare.com/ajax/libs/crypto-js/3.1.9-1/crypto-js.js"
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["scriptURL="])
    except getopt.GetoptError:
        print('hugo-encryptor.py --scriptURL <scriptURL>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('hugo-encryptor.py --scriptURL <scriptURL>')
            sys.exit()
        elif opt in ("--scriptURL"):
            scriptURL = arg
    print('=> scriptURL =', scriptURL)

    for dirpath, dirnames, filenames in os.walk('public'):
        for filename in filenames:
            fullpath = os.path.join(dirpath, filename)
            if filename.lower().endswith('.html'):
                soup = BeautifulSoup(open(fullpath, 'rb'), 'lxml')
                blocks = soup.findAll(
                    'div', {'class': 'hugo-encryptor-cipher-text'})

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
                        'hugo_encryptor', 'decoder_script.js').decode('utf8')

                    script_tag.string = "\n" + decoder_script
                    soup.body.append(script_tag)
                    soup.body.append("\n")

                    with open(fullpath, 'w') as f:
                        html = str(soup)
                        f.write(str(soup))
            elif filename.lower().endswith('.xml'):
                soup = BeautifulSoup(open(fullpath, 'rb'), 'xml')
                print("[+] Processing '{}'".format(fullpath))
                descriptions = soup('description')

                for description in descriptions:
                    if description.string is not None:
                        post = BeautifulSoup(description.string, 'html.parser')
                        block = post.find('hugo-encryptor')

                        if block is None:
                            pass

                        else:
                            language = block.find('p')

                            if language.string == 'Part of this article is encrypted with password:':
                                prompt = BeautifulSoup(
                                    '<p><i>Part of this article is encrypted with password, please goto the original webpage to check it out.</i></p>', 'html.parser')

                            block.replace_with(prompt)
                            description.string.replace_with(str(post))

                with open(fullpath, 'w') as f:
                    f.write(str(soup))

            elif filename.lower().endswith('.json'):
                pass
