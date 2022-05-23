from threading import Thread
import pyperclip as clip
import pynput.keyboard as keyboard
import pynput.mouse as mouse
from doll import * 
from cmd_manager import *
import dao

buff = ""
group = ""

exit = False

version = "2022/5/23"



def cmd_split(origin_cmd):
    parts = origin_cmd.split(':')
    op = parts[0]
    if len(parts) > 1:
        args = parts[1].split(',')
    else:
        args = []
    return op, args

def cmd_fill(body, args):
    arg_id = 0
    for arg in args:
        body = body.replace('{%d}'%arg_id, arg)
        arg_id = arg_id + 1
    return body

def cv_print(s):
    #ori = clip.paste()
    clip.copy(s)
    kc.press(keyboard.Key.ctrl)
    kc.press('v')
    kc.release('v')
    kc.release(keyboard.Key.ctrl)
    kc.press(keyboard.Key.ctrl)
    kc.release(keyboard.Key.ctrl)
    #clip.copy(ori)

def del_char(cnt):
    for _ in range(cnt):
        kc.press(keyboard.Key.backspace)
        kc.release(keyboard.Key.backspace)

def check_char(c):
    if c in ('@', ':', ','):
        return True
    if c >= 'a' and c <= 'z':
        return True
    if c >= 'A' and c <= 'Z':
        return True
    if c >= '0' and c <= '9':
        return True
    return False

def key_press_event(key):
    global dc, buff, group, exit
    if type(key) == keyboard._win32.KeyCode:
        val = key.char
        if val == None:
            buff = ""
            return
        if check_char(val):
            buff += val
    else:
        if key == keyboard.Key.space:
            cnt = len(buff)
            if cnt > 3 and buff[0] == '@' and buff[1] == '@' and buff[2] == '@':
                del_char(cnt+1)
                group = buff[3:]
            elif cnt > 2 and buff[0] == '@' and buff[1] == '@':
                del_char(cnt+1)
                op = buff[2:]
                if op == 'exit':
                    exit = True
                    mc.move(0, 1)
                    dc.close()
                    print("exit.")
                    return False
                elif op == 'hide':
                    win_doll.root.withdraw()
                elif op == 'show':
                    win_doll.root.deiconify()
                elif op == 'version':
                    cv_print(version)
                elif op == 'list':
                    cmd_manager(dc, group)
                else:
                    op, args = cmd_split(op)
                    if op == 'help':
                        if len(args) == 0:
                            content = ""
                        else:
                            content = dc.get_help_of_cmd(args[0], group)
                    else:
                        content = cmd_fill(dc.get_body_of_cmd(op, group), args)
                    cv_print(content)
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

def check_exit():
    global exit
    if exit == True:
        win_doll.root.quit()
    win_doll.root.after(1000, check_exit)



#-----main------

dc = dao.dao_code('yzjsswk.db')

kc = keyboard.Controller()
mc = mouse.Controller()

thread_keyboard = Thread(target = keyboard_listener)
thread_mouse = Thread(target = mouse_listener)

thread_keyboard.start()
thread_mouse.start()

print("start listening.")

win_doll = doll(200, 200, 'pictures/')
win_doll.root.after(1000, check_exit)
win_doll.root.mainloop()

