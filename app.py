from flask import Flask, request, render_template,redirect, url_for
import requests
from gtts import gTTS
from random import randrange
import sqlite3
app = Flask(__name__)

from datetime import datetime

# datetime object containing current date and time
def get_key():

    now = datetime.now()

    now = str(now).split(" ")
    key1 = "".join(now[0].split("-"))
    key2 = "".join(("".join(now[1].split(":")).split(".")))
    key = key2 + key1
    return key
@app.route('/')
def my_form():
    return render_template('index.html')

@app.route('/login',methods=["POST"])
def log_in():
    emails = request.form["email"]
    passwd = request.form["psw"]
    with sqlite3.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("select email from khach_hang ")
        rows = cur.fetchall()
        for i in rows:
            if i[0] == emails:
                cur.execute("select * from khach_hang  where email == (?)",(emails,))
                rows2 = cur.fetchall()
                if passwd == rows2[0][2]:
                    profile = {"email":rows2[0][0],"mskh":rows2[0][1]}
                    return profile
        return "Username or pass sai"
@app.route('/signup')
def signup():
    return render_template("register.html")
@app.route('/addnew',methods=["POST"])
def addnew():
        email = request.form["email"]
        passwd = request.form["psw"]
        passwd_repeat = request.form["pswr"]
        mskh = "kh" + get_key()+"sh"
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("select email from khach_hang")
            rows = cur.fetchall()
            print(rows)
            for i in rows:
                if i[0] == email:
                    msg = "Email đã được sử dụng"
                    return render_template("resualt.html", msg=msg)
            cur.execute("INSERT INTO khach_hang (email,mskh,passwd) VALUES (?,?,?)",(email,mskh,passwd))
            con.commit()
        msg = "TẠo tài khoản thành công. Mời bạn quay lại trang đăng nhập!"
        return render_template("resualt.html", msg=msg)
@app.route('/list')
def list():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from khach_hang")

    rows = cur.fetchall();
    return render_template("list.html", rows=rows)
@app.route('/', methods=['POST'])
def my_form_post():
    if request.form.get("submit_vi"):
        text = request.form['text-to-speech-input']
        if text == "":
            return render_template("index.html")
        text_return = text
        list_text = text.split()
        text = list_text[0]
        for i in range(1, len(list_text)):
            text = text + "+" + list_text[i]
        before_url = "https://vbee.vn/api/v1/convert-tts?input_text="
        ten_nguoi_doc1 = "&voice=vbee-tts-voice-hn_female_ngochuyen_news_48k-h&bit_rate=128000"

        ten_nguoi_doc2 = "&voice=sg_female_thaotrinh_news_48k-d&bit_rate=128000"

        api = before_url + text + ten_nguoi_doc1

        kq = requests.get(api).json()["download"]
        filename = str(kq).split("/")[4]+".mp3"
        file_name_save = "static/" + filename
        with open(file_name_save, "wb") as file:
            audio = requests.get(kq)
            file.write(audio.content)
        return render_template("index.html",filename = filename,text = text_return)
    else:
        text = request.form['text-to-speech-input']
        if text == "":
            return render_template("index.html")
        tts = gTTS(text)
        random = randrange(1000000,1000000000)
        filename = "a"+ str(random)+".mp3"
        file_save = "static/"+filename
        tts.save(file_save)
        return render_template("index.html",filename = filename,text= text)
@app.route("/mp3/<filename>")
def stream_mp3(filename):
    return redirect(url_for('static', filename=filename), code=301)
if __name__ == '__main__':
    app.run()
