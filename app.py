from flask import Flask, request, render_template,redirect, url_for
import requests
from gtts import gTTS
from random import randrange
import sqlite3
app = Flask(__name__)
import hashlib
from datetime import datetime
import urlquote

VNPAY_HASH_SECRET_KEY = 'OBRPXNCQDNZTEXUXXJEDZOJOQJOVNTNZ'



# Hàm tạo URL thanh toán
class vnpay:
    requestData = {}
    responseData = {}

    def get_payment_url(self, vnpay_payment_url, secret_key):
        inputData = sorted(self.requestData.items())
        queryString = ''
        hasData = ''
        seq = 0
        for key, val in inputData:
            if seq == 1:
                queryString = queryString + "&" + key + '=' + urlquote(val)
                hasData = hasData + "&" + str(key) + '=' + str(val)
            else:
                seq = 1
                queryString = key + '=' + urlquote(val)
                hasData = str(key) + '=' + str(val)

        hashValue = self.__md5(secret_key + hasData)
        return vnpay_payment_url + "?" + queryString + '&vnp_SecureHashType=SHA256&vnp_SecureHash=' + hashValue

    def validate_response(self, secret_key):
        vnp_SecureHash = self.responseData['vnp_SecureHash']
        # Remove hash params
        if 'vnp_SecureHash' in self.responseData.keys():
            self.responseData.pop('vnp_SecureHash')

        if 'vnp_SecureHashType' in self.responseData.keys():
            self.responseData.pop('vnp_SecureHashType')
        # self.responseData.pop('vnp_SecureHash', None)
        # self.responseData.pop('vnp_SecureHashType',None)
        inputData = sorted(self.responseData.items())
        hasData = ''
        seq = 0

        for key, val in inputData:
            if str(key).startswith('vnp_'):
                if seq == 1:
                    hasData = hasData + "&" + str(key) + '=' + str(val)
                else:
                    seq = 1
                    hasData = str(key) + '=' + str(val)
        hashValue = self.__md5(secret_key + hasData)

        print(
            'Validate debug, HashData:' + secret_key + hasData + "\n HashValue:" + hashValue + "\nInputHash:" + vnp_SecureHash)

        return vnp_SecureHash == hashValue

    def __md5(self, input):
        byteInput = input.encode('utf-8')
        return hashlib.md5(byteInput).hexdigest()
def payment_ipn(request):
    inputData = request.GET
    if inputData:
        vnp = vnpay()
        vnp.responseData = inputData.dict()
        order_id = inputData['vnp_TxnRef']
        amount = inputData['vnp_Amount']
        order_desc = inputData['vnp_OrderInfo']
        vnp_TransactionNo = inputData['vnp_TransactionNo']
        vnp_ResponseCode = inputData['vnp_ResponseCode']
        vnp_TmnCode = inputData['vnp_TmnCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_BankCode = inputData['vnp_BankCode']
        vnp_CardType = inputData['vnp_CardType']
        if vnp.validate_response(VNPAY_HASH_SECRET_KEY):
            # Check & Update Order Status in your Database
            # Your code here
            firstTimeUpdate = False
            if firstTimeUpdate:
                if vnp_ResponseCode == '00':
                    print('Payment Success. Your code implement here')
                else:
                    print('Payment Error. Your code implement here')

                # Return VNPAY: Merchant update success
                result = {'RspCode': '00', 'Message': 'Confirm Success'}
            else:
                # Already Update
                result = {'RspCode': '02', 'Message': 'Order Already Update'}

        else:
            # Invalid Signature
            result = {'RspCode': '97', 'Message': 'Invalid Signature'}
    else:
        result = {'RspCode': '99', 'Message': 'Invalid request'}

    return result

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
