import requests
text = input("nhap từ cần đọc : ")
list_text = text.split()
text = list_text[0]
for i in range(1,len(list_text)):
    text = text + "+" + list_text[i]
before_url= "https://vbee.vn/api/v1/convert-tts?input_text="
ten_nguoi_doc1 = "&voice=vbee-tts-voice-hn_female_ngochuyen_news_48k-h&bit_rate=128000"

ten_nguoi_doc2="&voice=sg_female_thaotrinh_news_48k-d&bit_rate=128000"

api = before_url + text + ten_nguoi_doc2

kq = requests.get(api).json()["download"]
file_name = str(kq).split("/")
print(file_name[4])