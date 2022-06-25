import requests
import pprint

url = 'http://localhost:5000/api/sentiment'
data = {
    "text": [
        "SARAN AJA KALO BISA DIBENERIN, BIAR LEBIH BAIK LAGI KE DEPANNYA SOALNYA BANYAK ERROR. TERIMA KASIH",
        "Itu kenapa dah? kok rusak? kecewa banget gw",
        "Astaga tolong diperbaiki dong, ini gimana nih? saran aja kalo lama2 ntar rusak",
        "Senang bat gw, terima kasih. alhamdulillah slalu lancar dan baik. Gak pernah rusak",
        "Nanti saya tambah ratingnya kalo udah betul, tolong ini kenapa ya? kok error? makanya saya turunin dulu"
    ]
}

r = requests.post(url, json=data)

pprint.pprint(r.json())