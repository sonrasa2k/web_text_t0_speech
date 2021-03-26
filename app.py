from flask import Flask, request, render_template,redirect, url_for
import requests
from gtts import gTTS
from random import randrange
app = Flask(__name__)




@app.route('/')
def my_form():
    return render_template('index_final.html')

@app.route('/', methods=['POST'])
def my_form_post():
    if request.form.get("submit_vi"):
        text = request.form['text']
        if text == "":
            return render_template("index_final.html")
        text_return = text
        list_text = text.split()
        text = list_text[0]
        for i in range(1, len(list_text)):
            text = text + "+" + list_text[i]
        before_url = "https://vbee.vn/api/v1/convert-tts?input_text="
        ten_nguoi_doc1 = "&voice=vbee-tts-voice-hn_female_ngochuyen_news_48k-h&bit_rate=128000"

        ten_nguoi_doc2 = "&voice=sg_female_thaotrinh_news_48k-d&bit_rate=128000"

        api = before_url + text + ten_nguoi_doc2

        kq = requests.get(api).json()["download"]
        filename = str(kq).split("/")[4]+".mp3"
        file_name_save = "static/" + filename
        with open(file_name_save, "wb") as file:
            audio = requests.get(kq)
            file.write(audio.content)
        return render_template("index_final.html",filename = filename,text = text_return)
    else:
        text = request.form['text']
        if text == "":
            return render_template("index_final.html")
        tts = gTTS(text)
        random = randrange(1000000,1000000000)
        filename = "a"+ str(random)+".mp3"
        file_save = "static/"+filename
        tts.save(file_save)
        return render_template("index_final.html",filename = filename,text= text)
@app.route("/mp3/<filename>")
def stream_mp3(filename):
    return redirect(url_for('static', filename=filename), code=301)
if __name__ == '__main__':
    app.run()
