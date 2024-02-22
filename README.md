# KTP NIK Recognition
Aplikasi sederhana untuk mendeteksi nomor induk kependudukan. Aplikasi ini menggunakan beberapa teknik image processing seperti thresholding, contour detection, dilation, erosion, OCR, dll. Teknik OCR yang digunakan di aplikasi ini tidak menggunakan machine learning atau deep learning, melainkan menggunakan similarity dari setiap digitnya. Hasilnya akan lebih cepat namun akurasinya tidak seakurat machine learning. 

Berikut adalah contoh bagaimana aplikasi ini dapat mendeteksi nomor NIK <br>
_semua gambar ktp diambil dari google image_ 
<br>
![step1](https://github.com/widyamsib/KTP-NIK-recognition/assets/118953030/325316b4-efd7-4454-8a91-9055922f100b)
![step2](https://github.com/widyamsib/KTP-NIK-recognition/assets/118953030/980cb179-352b-4c87-8550-6ca0015aeec4)
![step3](https://github.com/widyamsib/KTP-NIK-recognition/assets/118953030/9c2ce5fd-ffbd-4c75-a253-f035b416e961)

## Cara Menggunakan
Buat docker image sendiri
```console 
root@ubuntu:~$ git clone git@github.com:widyamsib/KTP-NIK-recognition.git
root@ubuntu:~$ cd KTP-NIK-recognition
root@ubuntu:~$ docker build -t haidhi/ktp .
root@ubuntu:~$ chmod +x nik_recognition.sh 
root@ubuntu:~$ ./nik_recognition.sh /assets/sample1.jpg

+-----------------------+
| NIK: 3471140209790001 |
+-----------------------+
execution time: 0.21s
```

Atau bisa juga langsung pull dari docker hub tanpa clone dan build lagi. Cukup download file **`nik_recognition.sh`** saja
```console 
root@ubuntu:~$ docker pull haidhi/ktp
root@ubuntu:~$ chmod +x nik_recognition.sh 
root@ubuntu:~$ ./nik_recognition.sh /assets/sample1.jpg

+-----------------------+
| NIK: 3471140209790001 |
+-----------------------+
execution time: 0.21s
```

## Penutup 
Aplikasi ini memiliki beberapa kekurangan seperti 
- Program berjalan optimal jika background KTP gelap
- Program OCR masih melakukan beberapa kesalahan dalam deteksi digit

Improvement yang dapat dilakukan menggunakan deeep learning: 
- Menggunakan deep learning untuk deteksi object KTP, sehingga dalam background apapun program dapat mendeteksi letak KTP dengan akurat
- Mendapatkan database digit yang lebih baik atau menggunakan teknik yang lebih advanced yaitu OCR dengan deep learning
