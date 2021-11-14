# Pekompressor
> Website yang bisa melakukan kompresi gambar.

## Table of Contents
* [Features](#features)
* [Screenshots](#screenshots)
* [Setup](#setup)
* [Usage](#usage)
* [Room for Improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)

## Features
1. Kompresi gambar
2. Input dengan fitur drag and drop maupun memilih gambar dari folder
3. Pemilihan persen kompresi gambar berdasarkan rank


## Screenshots
![Example screenshot](doc/image/page_1.jpg)
![Example screenshot](doc/image/page_2.jpg)
![Example screenshot](doc/image/page_3.jpg)
![Example screenshot](doc/image/page_4.jpg)

## Setup
Dependencies:
-nodejs  
-vuejs  
-flask  
-axios  
-json-server  
-python 3.2:  
    a. numpy  
    b. pillow  
    c. scipy  
    d. base64  

Install menggunakan pip install module python:
1. pip install numpy
2. pip install pillow
3. pip install scipy
4. pip install base64
5. pip install flask
6. pip install flask-cors

Setup aplikasi
1. Download nodejs
2. Setelah menginstall nodejs, install vue menggunakan terminal OS dengan command "npm install vue"
3. Masuk ke folder yang ingin digunakan di terminal

Untuk start program ini, kita perlu menyalakan 3 server yaitu flask,vue, dan json dengan run command di 3 terminal berbeda sebagai berikut:
1. flask
    a. cd src/flask/env/scripts  
    b.  ./activate  
    c. cd ../..  
    d. python app.py  

2. vue
    a. cd src/vue  
    b. npm run serve  

3. json
    a. cd src/vue  
    b. npx json-server --watch Data/image.json cd src/vue  

## Usage
Setelah menyalakan ketiga server di atas, buka server yang disediakan oleh vue yaitu " http://localhost:8080/"

## Room for improvement
1. Mempertahankan transparansi file png
2. Mempercepat kompresi
3. Penentuan persentase kompresi yang lebih akurat
4. Input file dengan drag and drop masih belum dibatasi jenis filenya
5. Jika menerima input yang error server akan langsung error dan harus di start ulang

## Acknowledgements
- Project ini dilakukan untuk pemenuhan tugas besar 2 Aljabar Linear dan Geometri 2021
- Referensi yang digunakan pada tugas besar ini
1. Back-end
[this tutorial](https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/#bootstrap-setup).
2. Front-end
[this tutorial](https://www.udemy.com/course/build-web-apps-with-vuejs-firebase/).
