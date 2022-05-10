import os
from threading import Thread
import pyperclip as clip
import pynput.keyboard as keyboard
import pynput.mouse as mouse
import tkinter
from PIL import Image, ImageTk


root = ""
buff = ""
expand = {}
txt_path_list = []
exit = False
version = "2022/5/10"

def load_command(file_content):
    global expand
    op = ""
    content = """"""
    flag = True
    for row in file_content:
        if len(row) > 1 and row[0] == '#' and row[1] == '#':
            continue
        if flag:
            op = row.strip()
            flag = False
        else:
            content += row
    expand[op] = content

def get_txt_path(dic_path):
    global txt_path_list
    for name in os.listdir(dic_path):
        full_path = os.path.join(dic_path, name)
        if os.path.isdir(full_path):
            get_txt_path(full_path)
        elif full_path.endswith(('txt')):
            txt_path_list.append(full_path)


def read_commands():
    global txt_path_list, expand, version
    expand.clear()
    expand['version'] = version
    for path in txt_path_list:
        with open(path) as f:
            load_command(f.readlines())
    print("read {} commands.".format(len(expand)-1))

def key_press_event(key):
    global root, buff, expand, txt_path_list, exit
    if type(key) == keyboard._win32.KeyCode:
        val = key.char
        if val == None:
            buff = ""
            return
        if val >= 'a' and val <= 'z':
            buff += val
        if val >= 'A' and val <= 'Z':
            buff += val
        if val >= '0' and val <= '9':
            buff += val
        if val == '@' or val == '_':
            buff += val
    else:
        if key == keyboard.Key.space:
            cnt = len(buff)
            if cnt > 3 and buff[0] == '@' and buff[1] == '@' and buff[2] == '@':
                kb = keyboard.Controller()
                for _ in range(cnt+1):
                    kb.press(keyboard.Key.backspace)
                    kb.release(keyboard.Key.backspace)
                package_name = buff[3:]
                path = root + '\commands' + '\\' + package_name
                if os.path.exists(path):
                    txt_path_list.clear()
                    get_txt_path(path)
                    read_commands()
                    print(f"namespace change to '{package_name}'.")
                else:
                    print(f"path not exists: {path}.")
                buff = ""
            elif cnt > 2 and buff[0] == '@' and buff[1] == '@':
                kb = keyboard.Controller()
                for _ in range(cnt+1):
                    kb.press(keyboard.Key.backspace)
                    kb.release(keyboard.Key.backspace)
                tag = buff[2:].split('_')
                op = tag[0]
                paras = tag[1:]
                #print(op)
                #print(paras)
                if op in expand:
                    #ori = clip.paste()
                    content = expand[op]
                    para_id = 0
                    for para in paras:
                        content = content.replace('{%d}'%para_id, para)
                        para_id = para_id + 1
                    clip.copy(content)
                    kb.press(keyboard.Key.ctrl)
                    kb.press('v')
                    kb.release('v')
                    kb.release(keyboard.Key.ctrl)
                    kb.press(keyboard.Key.ctrl)
                    kb.release(keyboard.Key.ctrl)
                    #clip.copy(ori)
                elif op == 'exit':
                    print("exit.")
                    exit = True
                    ms = mouse.Controller()
                    ms.move(0, 1)
                    return False
                elif op == 'hide':
                    ball.withdraw()
                elif op == 'show':
                    ball.deiconify()
                else:
                    print(f"command '{op}' not found.")
                    buff = ""
            else:
                buff = ""
        elif key == keyboard.Key.shift_l or key == keyboard.Key.shift_r:
            pass
        elif len(buff) > 0 and key == keyboard.Key.backspace:
            buff = buff[:-1]
        else:
            buff = ""
    #print(buff)

'''
def key_release_event(key):
    global exit
    if exit == True:
        return False
'''

def mouse_click_event(x, y, button, pressed):
    global buff
    buff = ""

def mouse_move_event(x, y):
    global exit
    if exit == True:
        return False

def keyboard_listener():
    with keyboard.Listener(on_press = key_press_event) as listener:
        listener.join()   

def mouse_listener():
    with mouse.Listener(on_click = mouse_click_event, on_move = mouse_move_event) as listener:
        listener.join()


root = os.getcwd()
print(f"当前目录: {root}")

expand['version'] = version

thread_keyboard = Thread(target = keyboard_listener)
thread_mouse = Thread(target = mouse_listener)

thread_keyboard.start()
thread_mouse.start()

print("start listening.")


#---------------------------------

x, y = 0, 0
w, h = 200, 200

def load_picture(file_path):
    global w, h
    if not file_path.endswith(('png', 'PNG', 'jpg', 'JPG', 'jpeg', 'JPEG')):
        print('File ingored: ' + file_path)
        return 0
    pic = Image.open(file_path)
    pw = pic.width
    ph = pic.height
    k = w / max(pw, ph)
    #pic = pic.crop((0, 0, size, size))
    pic = pic.resize((int(pw*k), int(ph*k)), Image.BICUBIC)
    return pic        

def load_pictures(dic_path):
    file_list = os.listdir(dic_path)
    pictures = []
    for file_name in file_list:
        pic = load_picture(dic_path + file_name)
        if pic != 0:
            pictures.append(pic)
    print(len(pictures), 'pictures loaded.')
    return pictures

def check_exit():
    global exit
    if exit == True:
        ball.quit()
    ball.after(1000, check_exit)

def move(event):
    global x,y,w,h
    new_x = (event.x-x)+ball.winfo_x()
    new_y = (event.y-y)+ball.winfo_y()
    s = f"{w}x{h}+" + str(new_x)+"+" + str(new_y)
    ball.geometry(s)
    #print("s = ",s)
    #print(root.winfo_x(),root.winfo_y())
    #print(event.x,event.y)

def button_1(event):
    global x,y
    x,y = event.x,event.y
    #print("event.x, event.y = ",event.x,event.y)

def button_2(event):
    global pic_cnt, cur_pic, pic, pictures
    if pic_cnt > 0:
        cur_pic = (cur_pic + 1) % pic_cnt
        pic = ImageTk.PhotoImage(pictures[cur_pic])        
        canvas.create_image((w//2, h//2), image = pic)

ball = tkinter.Tk()
screen_width = ball.winfo_screenwidth()
screen_height = ball.winfo_screenheight()
ball.geometry(f"{w}x{h}+{screen_width//2}+{screen_height//2}")
ball.overrideredirect(True)
#ball.attributes("-alpha", 0.4)
ball.attributes("-topmost", True)
ball.wm_attributes("-transparentcolor", "snow")


canvas = tkinter.Canvas(ball)
canvas.configure(width = w)
canvas.configure(height = h)
canvas.configure(bg = "snow")
canvas.configure(highlightthickness = 0)

pictures = load_pictures("pictures/")
pic_cnt = len(pictures)
cur_pic = 0
if(pic_cnt > 0):
    pic = ImageTk.PhotoImage(pictures[cur_pic])
canvas.create_image((w//2, h//2), image = pic)

canvas.pack()

canvas.bind("<B1-Motion>", move)
canvas.bind("<Button-1>", button_1)
canvas.bind("<Button-3>", button_2)

ball.after(1000, check_exit)
ball.mainloop()

