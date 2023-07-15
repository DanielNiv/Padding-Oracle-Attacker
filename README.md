# Background

I wanted to solve the picoCTF-2018 "Magic Padding Oracle" challenge.
All available resources online gives us the `challenge/pkcs7.py` server file, but not the `key, cookie, flag` files that are necessary in order for the challenge to work.
I decided to generate my own files, after I generted some random key.
The script that does it is `my_ctf_setup.py`



# Solution

```python
python3 sol.py
```

gives us the final payload:

```html
ea8496c0be8f66f232b0587923cec8787454e2327def953e61ae4d898a15e90029238adbc9bb409d2b2d8282dafb237e91f661ee1b3d5a3feeac7b544e3cac3f41414141414141414141414141414141
```

and indeed we get the correct output:

```bash
What is your cookie?
ea8496c0be8f66f232b0587923cec8787454e2327def953e61ae4d898a15e90029238adbc9bb409d2b2d8282dafb237e91f661ee1b3d5a3feeac7b544e3cac3f41414141414141414141414141414141
username: admin
Admin? true
Cookie is not expired
The flag is: picoCTF{0r4cl3s_c4n_l34k_86bb783e}
```

