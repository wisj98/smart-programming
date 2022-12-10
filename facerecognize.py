import os
import sys
import json
import tkinter
import requests
from PIL import Image
import re

client_id = "njmaxMgpwOc8xwgzf62J"
client_secret = "okQtVnmetS"
url_face = "https://openapi.naver.com/v1/vision/face"
url_famous = "https://openapi.naver.com/v1/vision/celebrity"

def work(pic:str) :
    #얼굴분석결과
    if pic[-4:] == "webp":
        im = Image.open(pic).convert('RGB')
        im.save('pic/convert/converted.jpg', 'jpeg')
        pic = 'pic/convert/converted.jpg'
    files = {'image': open(pic, 'rb')}
    headers = {'X-Naver-Client-Id': client_id, 'X-Naver-Client-Secret': client_secret }
    response = requests.post(url_face,  files=files, headers=headers)
    rescode = response.status_code
    if(rescode==200):
        data = json.loads(response.text)
    else:
        print("Error Code:" + str(rescode))
        return False, "err: " + str(rescode)
    #유명인매치결과
    files = {'image': open(pic, 'rb')}
    response = requests.post(url_famous,  files=files, headers=headers)
    rescode = response.status_code
    if(rescode==200):
        data_famous = json.loads(response.text)
    else:
        print("Error Code:" + str(rescode))
        return False, "err:" + str(rescode)
    try: data['celeb'] = data_famous['faces'][0]['celebrity'] 
    except IndexError:
        return False, "err: 얼굴을 인식할 수 없습니다."
    if data['info']['faceCount'] > 1:
        return False, "err: 얼굴이 2개 이상입니다...."

    return True, data 

if __name__ == '__main__' :
    work('test.jpg')
