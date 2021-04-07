# Hugo Encryptor 🔏

> Note: This is a fork of https://github.com/Li4n0/hugo_encryptor

**Hugo Encryptor** is a tool to protect your [Hugo](https://gohugo.io) posts. It uses AES-256 to encrypt the contents of your posts, and inserts a snippet of `<script>` code to verify whether the password is correct or not in readers' browser. Without a correct key, nobody can decrypt your private posts.

Note: `Hugo Encryptor` currently works with `HTML` and `XML` outputs only

---

## Installation 📥

### Requirements

- Python3
### Step 1: Install Hugo-Encryptor

```shell
$ git clone https://github.com/adityatelange/hugo_encryptor.git
$ cd hugo_encryptor
$ pip3 install .
```


### Step 2: Copy `shortcodes/hugo_encryptor.html`


Copy `shortcodes/hugo_encryptor.html` into the `shortcodes` directory of your website source

```
.(site root)
├── content/
├── layouts/
│   └── shortcodes/
│       └── hugo_encryptor.html  <---
├── public/
├── resources/
├── static/
└── themes/
```

---

## Usage ℹ️

Wrap the text you want to encrypt with the tag `hugo_encryptor`

> Note: Some text is required before you actually start the encrypting part, with a tag `<!--more-->` placed in the middle of them. Example:**

```
---
title: "A Post which has encrypted content"
---

Some text is required to be placed here.

<!--more-->

{{< hugo_encryptor "PASSWORD" >}}

This is the content you want to encrypt!

{{</ hugo_encryptor >}}

```

### Step 1: Generate your site

Go to your website's root and generate it as usual.

For ex.

```shell
$ hugo
```

### Step 2: Enncrypt your posts

The following command will encrypt all the blocks with `hugo_encryptor` with provided password

```shell
$ hugo_encryptor
```


---

## Style 🎀

**Hugo Encryptor** has **no style** elements attached to it.

However it has some classes which you can use to customize it accordingly.


---

## Note ⚠️

- Do remember to keep the source code of your encrypted posts private. Never push your blog directory into a public repository.

- Every time when you generate your site, you should run `hugo_encryptor` again to encrypt the posts which you want to be protected. If you are worried about you will forgot that, it's a good idea to use a shell script to take the place of  `hugo` ,such as below:

    ```bash
    #!/bin/bash

    hugo
    hugo_encryptor
    # Then upload your generated output
    ```
