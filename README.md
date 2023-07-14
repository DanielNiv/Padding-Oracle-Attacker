we want to have the following decrypted message:

{"username": "admin", "expires": "3017-01-01", "is_admin": "true"}

in hexhexlify()'ed bytes, this is the message:

7b22757365726e616d65223a202261646d696e222c202265787069726573223a2022333031372d30312d3031222c202269735f61646d696e223a202274727565227d

splitted into 16 bytes chunks, we get:

7b22757365726e616d65223a20226164    <-------------------- DECRYPTED BLOCK 0
6d696e222c202265787069726573223a    <-------------------- DECRYPTED BLOCK 1
2022333031372d30312d3031222c2022    <-------------------- DECRYPTED BLOCK 2
69735f61646d696e223a202274727565    <-------------------- DECRYPTED BLOCK 3
227d                                <-------------------- DECRYPTED BLOCK 4