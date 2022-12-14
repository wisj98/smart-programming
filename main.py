import sys
import subprocess
import os

try: import requests
except:
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pip'])
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'requests'])
    import requests
try: import PIL
except:
    subprocess.check_call([sys.executable,'-m', 'pip', 'install', '--upgrade', 'pillow'])
    import PIL
from PIL import Image, ImageTk

import tkinter as tk
import tkinter.font as font
from tkinter.filedialog import askopenfilename

import facerecognize as fr
import tools as tool

#창 기본 설정
window = tk.Tk() #창 생성
window.title("얼굴인식") #창의 이름
window.geometry("250x70+0+0") #가로x세로,창을 띄울 x,y좌표
window.resizable(False,False) #창사이즈 조절여부

#사진 선택창
def picselect() :
    root = tk.Tk()
    root.withdraw()
    filename = askopenfilename(parent=root,title="사진을 선택해주세요",filetypes=(("사진파일","*.jpg;*.png;*.webp"),("기타파일","*.*")))
    print(filename)
    if filename != '' :
        button_first.destroy()
        show_pic(filename)
        root.destroy()

#선택한 사진 보여주기
def show_pic(fileroot:str):
    err, data = fr.work(fileroot)
    if err == False :
        tk.messagebox.showerror(title="Can't recognize face perfectly", message=data)
        button_error = tk.Button(window,text= "다른 사진 등록하기", command=lambda:[tool.destroy(grid=[button_error]),picselect()], overrelief="solid", repeatdelay=1000, repeatinterval=100)
        button_error.grid(row=0,column=0)
        return None
    
    print(data) #'info','faces','landmark','gender','age','emotion','pose','celeb'
    x, y, z = tool.resizer(data['info']['size']['width'], data['info']['size']['height'], 1)
    window.geometry(str(x) + "x" +str(y+170))
    img = Image.open(fileroot)
    img = img.resize((x,y))
    resized_img = ImageTk.PhotoImage(img)
    canvas = tk.Canvas(window,width=x,height=y,background="gray")
    canvas.grid(row=0,column=0)
    canvas.image = resized_img
    canvas.create_image(x/2, y/2, image=canvas.image)
    #사진 분석 결과 출력
    gender = tool.v_label(data['faces'][0]['gender'], window)
    age = tool.v_label(data['faces'][0]['age'], window)
    emotion = tool.v_label(data['faces'][0]['emotion'], window)
    pose = tool.v_label(data['faces'][0]['pose'], window)
    celeb = tool.v_label(data['celeb'],window,True)
    gender.grid(row=1,column=0)
    age.grid(row=2,column=0)
    emotion.grid(row=3,column=0)
    pose.grid(row=4,column=0)
    celeb.grid(row=5,column=0)
    #눈,코,입 위치 on/off
    global txt, off
    off = False
    txt = "눈,코,입 on/off"
    def landmark_onoff() :
        global off, txt
        if off == True :off = False
        else :off = True 
    button_show = tk.Button(window,text = txt,command=lambda:[tool.show_landmark(canvas, data["faces"][0], [x,y,z],off),landmark_onoff()], overrelief="solid", repeatdelay=1000, repeatinterval=100)
    button_show.grid(row=6,column=0)
    #다른 사진 등록 표시
    def convert_remover() :
        convert_check = os.path.isfile("pic/convert/converted.jpg")
        if convert_check == True : os.remove("pic/convert/converted.jpg")
    button_re = tk.Button(window,text= "다른 사진 등록하기", command=lambda:[tool.destroy(grid=[gender,age,emotion,pose,celeb,canvas,button_re,button_show]),picselect(),convert_remover()], overrelief="solid", repeatdelay=1000, repeatinterval=100)
    button_re.grid(row=7,column=0)

#사진등록버튼
button_first = tk.Button(window,text = "사진 등록",command=picselect,background="chocolate2",activebackground="chocolate", overrelief="solid", width=10,height=1, repeatdelay=1000, repeatinterval=100)
button_first.grid(row=0,column=0)
button_first['font'] = font.Font(size=30)

#convert 폴더 생성
os.makedirs("pic/convert",exist_ok=True)

#창 켜진채로 유지
window.mainloop()