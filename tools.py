import tkinter

global off

def resizer(x:int, y:int, z:float) :
    if x >= 400 and y >= 400:
        return resizer(x/2, y/2, z/2)
    if x <=300 and y <= 300:
        return resizer(x*1.3, y*1.3, z*1.3)
    return int(x),int(y),float(z)

def v_label(data:dict, window: tkinter.Tk, celeb = False):
    confidence = int(data['confidence'] * 100)
    dic = {'male':'남성', 'female':'여성','child':'어린이', 'angry':'분노', 'disgust':'역겨움', 'fear':'두려움', 'laugh':'즐거움',
    'neutral':'무표정', 'sad':'슬픔','surprise':'놀람','smile':'미소','talking':'대화중','part_face':'얼굴의 일부분',
    'false_face':'가짜얼굴','sunglasses':'썬글라스 낀 얼굴', 'frontal_face': '정면 얼굴', 'left_face':'왼쪽얼굴',
    'right_face': '오른쪽얼굴', 'rotate_face':'돌아간 얼굴'}
    if data['value'] in dic:
        value = dic[data['value']]
    elif celeb :
        value = data['value']
    else :
        value = data['value'] + "살"
    content = value + " "+ str(confidence) + "%"
    return tkinter.Label(window, text = content)

def show_landmark(canvas:tkinter.Canvas, face:dict, info:list,off:bool):
    
    if face["landmark"] != None :
        face_x1 = face["roi"]["x"] * info[2]
        face_y1 = face["roi"]["y"] * info[2]
        face_x2 = face_x1 + face["roi"]["width"] * info[2]
        face_y2 = face_y1 + face["roi"]["height"] * info[2]
        lefteye_x = face["landmark"]["leftEye"]["x"] * info[2]
        lefteye_y = face["landmark"]["leftEye"]["y"] * info[2]
        righteye_x = face["landmark"]["rightEye"]["x"] * info[2]
        righteye_y = face["landmark"]["rightEye"]["y"] * info[2]
        nose_x = face["landmark"]["nose"]["x"] * info[2]
        nose_y = face["landmark"]["nose"]["y"] * info[2]
        leftmouse_x = face["landmark"]["leftMouth"]["x"] * info[2]
        leftmouse_y = face["landmark"]["leftMouth"]["y"] * info[2]
        rightmouse_x = face["landmark"]["rightMouth"]["x"] * info[2]
        rightmouse_y = face["landmark"]["rightMouth"]["y"] * info[2]
        if off:
            canvas.delete('landmark')
        else:
            canvas.create_rectangle(lefteye_x,lefteye_y,lefteye_x + 3,lefteye_y + 3,fill = "red",outline="red",width=1, tags = "landmark")
            canvas.create_rectangle(righteye_x,righteye_y,righteye_x + 3,righteye_y + 3,fill = "red", outline="red",width=1, tags = "landmark")
            canvas.create_rectangle(nose_x,nose_y,nose_x + 3,nose_y + 3,fill = "red", outline="red",width=1, tags = "landmark")
            canvas.create_rectangle(leftmouse_x,leftmouse_y,leftmouse_x + 3,leftmouse_y + 3,fill = "red", outline="red",width=1, tags = "landmark")
            canvas.create_rectangle(rightmouse_x,rightmouse_y,rightmouse_x + 3,rightmouse_y + 3,fill = "red", outline="red",width=1, tags = "landmark")
            canvas.create_rectangle(face_x1,face_y1,face_x2,face_y2,outline="black",width=1, tags = "landmark")
    else :
        tkinter.messagebox.showerror(title="Can't recognize face perfectly", message="눈코입을 인식할 수 없어용.")

def destroy(pack = [],grid = [], place = []):
    for a in pack  :
        a.destroy()
    for a in grid  :
        a.destroy()
    for a in place :
        a.destroy()