import requests
import pprint
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("--seconds", help="Delay the test API call in seconds. Default: 1 second.", type=int)
args = parser.parse_args()
seconds = args.seconds
if seconds is None:
    seconds = 1
    
time.sleep(seconds)


# url = 'http://localhost:5000/api/sentiment'
url = 'https://teks-sentimen-analisis.herokuapp.com/api/sentiment'
data = {
    "text": [
        "Itu kenapa dah? kok rusak? kecewa banget gw",
        "Alhamdulillah berhasil terima kasih yaa saya akan tambahkan bintang. Namun saran aja tolong dipercepat proses pengantarannya",
        "Ternyata benar kata netizen APK ini makin lama makin gk jelas,,,,,, BGST,,,,, pas gw coba sekali langsung di tipu mending di APK sebelah lebih memuaskan di banding APK ini ,,,, untuk kalian yang belum download APK ini mending gak usah di download nanti nyesel,,,, banyak penipuan di APK ini,,,,, percaya sama gw kalau kalian gak mau di tipu...",
        "Permisi mohon maaf kepada pihak lazada , sebelum nya saya menggunakan lazada sebelumnya enak aja pelayanan juga memuaskan. ,tapi kenapa setelah saya perbarui malah di suruh login lagi , dan setelah saya masuk kenapa tidak bisa dan (layanan sedang sibuk) seperti itu berkali ,= saran aja ya jadi semisal ada pembaruan nggak usah masuk lagi masukin kata sandi maupun e-mail tinggal tambahin aja fitur ( masuk akun lama) itu udah cukup dan berguna bagi temen semisal lagi keadaan dia lupa kata sandi",
        "Kenapa unggah foto GK bisa sih...pdhl saya pakai wifi...selama ini lazada pelayanan baik,cuma jika ada complain barang,saya mengajukan pengembalian dana GK bisa karena harus kirim foto,sedangkan gunggah foto loading trus,GK bisa2..knp????",
    ]
}

r = requests.post(url, json=data)

pprint.pprint(r.json())