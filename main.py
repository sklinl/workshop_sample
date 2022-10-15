import imp
from fastapi import FastAPI, Response
import uvicorn
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import smtplib
from fastapi import File, UploadFile
import numpy as np
import cv2 as cv
# import model.detection as det
from fastapi.middleware.cors import CORSMiddleware
import time



app = FastAPI(title='AI Alert sender')

origins = [
    "http://localhost",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

## config content
gmail_token = base64.b64decode("d3doem92YXlzY2VzenJ5aw==").decode('utf-8')


@app.get('/api/v1/alert')
def send_email(recipients: str = 'kevinlinsk19@gmail.com'):
    content = MIMEMultipart()  #建立MIMEMultipart物件
    content["subject"] = "[ALARM] Please check it for more detail"  #郵件標題
    content["from"] = "kevinlinsk19@gmail.com"  #寄件者
    content["to"] = (', ').join(recipients.split(',')) #收件者
    content.attach(MIMEText("你違規了"))  #郵件內容

    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login("kevinlinsk19@gmail.com", gmail_token)  # 登入寄件者gmail
            smtp.send_message(content)  # 寄送郵件

            print("Complete!")

        except Exception as e:
            print("Error message: ", e)

    return 'OK'


@app.post('/api/v3/alert')
async def post_image(file: UploadFile = File(...), recipients: str = 'kevinlinsk19@gmail.com'):

    contents = await file.read()
    nparr = np.fromstring(contents, np.uint8)
    ori_img = cv.imdecode(nparr, cv.IMREAD_COLOR)
    # result = det.predict(ori_img)

    content = MIMEMultipart()  #建立MIMEMultipart物件
    content["subject"] = "[ALARM] Please check it for more detail"  #郵件標題
    content["from"] = "kevinlinsk19@gmail.com"  #寄件者
    content["to"] = (', ').join(recipients.split(',')) #收件者
    content.attach(MIMEText("你違規了來自AI"))  #郵件內容
    # content.attach(MIMEImage(result))  # 郵件圖片內容


    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login("kevinlinsk19@gmail.com", gmail_token)  # 登入寄件者gmail
            smtp.send_message(content)  # 寄送郵件

            print("Complete!")

        except Exception as e:
            print("Error message: ", e)

    time.sleep(10)
    print("return message")
    # return Response(content=result, media_type="image/png")
    return 'ok'

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)