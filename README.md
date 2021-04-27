# Hugo Enc (Encryptor) 🔏

> Note: This is a fork of https://github.com/Li4n0/hugo_encryptor

**Hugo Enc** is a tool to protect your [Hugo](https://gohugo.io) posts. It uses AES-256 to encrypt the contents of your posts, and inserts a snippet of `<script>` code to verify whether the password is correct or not in readers' browser. Without a correct key, nobody can decrypt your private posts.

**Hugo Enc** currently works with `HTML`, `XML` and `JSON` outputs.

---

## Installation 📥

### Requirements

-   Python3

### Step 1: Clone Hugo-Enc

1. Change your directory to your website source

    ```shell
    $ cd to/your/hugo/website/source
    ```

2. Install `hugo_enc` as a submodule

    ```shell
    $ git submodule add https://github.com/adityatelange/hugo_enc themes/hugo_enc --depth=1
    ```

3. Add `hugo_enc` as a theme

    In your `config.yml` add `hugo_enc` in themes variable ex.

    ```yml
    theme: [MyTheme, hugo_enc]
    ```

### Step 2: Install Hugo-Enc

```shell
$ cd themes/hugo_enc
$ pip3 install .
```

---

## Usage ℹ️

Wrap the text you want to encrypt with the tag `hugo_enc`

> Note: Some text is required before you actually start the encrypting part, with a tag `<!--more-->` placed in the middle of them. Example:\*\*

```
---
title: "A Post which has encrypted content"
---

Some text is required to be placed here.

<!--more-->

{{< hugo_enc "PASSWORD" >}}

This is the content you want to encrypt!

{{</ hugo_enc >}}

```

Usage for `hugo_enc`

```shell
Usage:
        hugo_enc [flags]

Flags:
    -h, --help              -           get help about hugo_enc
        --scriptURL         string      override the default 'scriptURL' to load crypto-js
        --destination       string      set the output folder (default: 'public')
```

### Step 1: Generate your site

Go to your website's root and generate it as usual.

For ex.

```shell
$ hugo
```

### Step 2: Encrypt your posts

The following command will encrypt all the blocks with `hugo_enc` with provided password

```shell
$ hugo_enc
```

---

## Style 🎀

**Hugo Encryptor** has **no style** elements attached to it.

However, it has some classes which you can use to customize it accordingly.

View the template here => [layouts/shortcodes/hugo_enc.html](layouts/shortcodes/hugo_enc.html)

---

## Adding custom Text to `hugo_enc` shortcode

You can use the following `params` in your `site config.yml`:

```yml
Params:
    hugoEnc:
        promptText: "Part of this article is encrypted with password:"
        inputPlaceholder: "Please input the password"
        buttonText: "Unlock"
```

---

## Note ⚠️

-   Do remember to keep the source code of your encrypted posts private. Never push your blog directory into a public repository.

-   Every time when you generate your site, you should run `hugo_enc` again to encrypt the posts which you want to be protected. If you are worried about you will forget that, it's a good idea to use a shell script to take the place of `hugo`,such as below:

    ```bash
    #!/bin/bash

    hugo
    hugo_enc
    # Then upload your generated output
    ```
