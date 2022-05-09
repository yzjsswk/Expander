from pynput.keyboard import Key, Controller as KB
from pynput import *
from threading import Thread
import pyperclip as clip 
import os


root = ""
buff = ""
expand = {}
txt_path_list = []
exit = False

def load_commond(file_content):
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


def read_commonds():
    global txt_path_list
    for path in txt_path_list:
        with open(path) as f:
            load_commond(f.readlines())
    

def key_press_event(key):
    global root, buff, expand, txt_path_list
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
        if key == Key.space:
            cnt = len(buff)
            if cnt > 3 and buff[0] == '@' and buff[1] == '@' and buff[2] == '@':
                kb = KB()
                for _ in range(cnt+1):
                    kb.press(Key.backspace)
                    kb.release(Key.backspace)
                package_name = buff[3:]
                path = root + '\commands' + '\\' + package_name
                if os.path.exists(path):
                    txt_path_list.clear()
                    expand.clear()
                    get_txt_path(path)
                    read_commonds()
                    print(f"namespace change to '{package_name}'.")
                else:
                    print(f"path not exists: {path}.")
                buff = ""
            elif cnt > 2 and buff[0] == '@' and buff[1] == '@':
                kb = KB()
                for _ in range(cnt+1):
                    kb.press(Key.backspace)
                    kb.release(Key.backspace)
                tag = buff[2:].split('_')
                op = tag[0]
                paras = tag[1:]
                #print(op)
                #print(paras)
                if op in expand:
                    #ori = clip.paste()
                    content = expand[op]
                    for para in paras:
                        content = content.replace('{}', para, 1)
                    clip.copy(content)
                    kb.press(Key.ctrl)
                    kb.press('v')
                    kb.release('v')
                    kb.release(Key.ctrl)
                    kb.press(Key.ctrl)
                    kb.release(Key.ctrl)
                    #clip.copy(ori)
                else:
                    print(f"commond '{op}' not found.")
                    buff = ""
            else:
                buff = ""
        elif key == Key.shift_l or key == Key.shift_r:
            pass
        elif len(buff) > 0 and key == Key.backspace:
            buff = buff[:-1]
        else:
            buff = ""
    #print(buff)

def key_release_event(key):
    global exit
    if key == Key.esc or exit == True:
        exit = True
        return False

def mouse_click_event(x, y, button, pressed):
    buff = ""
    if exit == True:
        return False

def keyboard_listener():
    with keyboard.Listener(on_press = key_press_event, on_release = key_release_event) as listener:
        listener.join()   

def mouse_listener():
    with mouse.Listener(on_click = mouse_click_event) as listener:
        listener.join()


root = os.getcwd()
print(f"当前目录: {root}")


thread_keyboard = Thread(target = keyboard_listener)
thread_mouse = Thread(target = mouse_listener)

thread_keyboard.start()
thread_mouse.start()

print("start listening.")



