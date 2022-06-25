import requests
import pprint

url = 'http://localhost:5000/api/sentiment'
data = {
    "text": "SARAN AJA KALO BISA DIBENERIN, BIAR LEBIH BAIK LAGI KE DEPANNYA SOALNYA BANYAK ERROR. TERIMA KASIH"
}

r = requests.post(url, json=data)

pprint.pprint(r.json())