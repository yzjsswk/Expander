import os
import tkinter
from PIL import Image, ImageTk

class doll:
    def __init__(self, width, height, pic_path):
        self.w, self.h = width, height
        self.x, self.y = 0, 0

        self.root = tkinter.Tk()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.w}x{self.h}+{screen_width//2}+{screen_height//2}")
        self.root.overrideredirect(True)
        #ball.attributes("-alpha", 0.4)
        self.root.attributes("-topmost", True)
        self.root.wm_attributes("-transparentcolor", "snow")
    
        self.can = tkinter.Canvas(self.root)
        self.can.configure(width = self.w)
        self.can.configure(height = self.h)
        self.can.configure(bg = "snow")
        self.can.configure(highlightthickness = 0)

        self.pictures = self.load_pictures(pic_path)
        self.pic_cnt = len(self.pictures)
        self.cur_pic = 0
        self.show_pic(self.cur_pic)

        self.can.pack()
        self.can.bind("<B1-Motion>", self.move_event)
        self.can.bind("<Button-1>", self.left_click_event)
        self.can.bind("<Button-3>", self.right_click_event)

    def load_picture(self, file_path):
        if not file_path.endswith(('png', 'PNG', 'jpg', 'JPG', 'jpeg', 'JPEG')):
            print('File ingored: ' + file_path)
            return 0
        pic = Image.open(file_path)
        pw = pic.width
        ph = pic.height
        k = self.w / max(pw, ph)
        #pic = pic.crop((0, 0, size, size))
        pic = pic.resize((int(pw*k), int(ph*k)), Image.BICUBIC)
        return pic        

    def load_pictures(self, dic_path):
        file_list = os.listdir(dic_path)
        pictures = []
        for file_name in file_list:
            pic = self.load_picture(dic_path + file_name)
            if pic != 0:
                pictures.append(pic)
        print(len(pictures), 'pictures loaded.')
        return pictures

    def show_pic(self, pid):
        if pid < 0 or pid >= self.pic_cnt:
            return
        global pic
        pic = ImageTk.PhotoImage(self.pictures[pid])
        self.can.create_image((self.w//2, self.h//2), image = pic)

    def move_event(self, event):
        new_x = (event.x - self.x) + self.root.winfo_x()
        new_y = (event.y - self.y) + self.root.winfo_y()
        s = f"{self.w}x{self.h}+" + str(new_x) + "+" + str(new_y)
        self.root.geometry(s)
        #print("s = ",s)
        #print(root.winfo_x(),root.winfo_y())
        #print(event.x,event.y)

    def left_click_event(self, event):
        self.x, self.y = event.x, event.y
        #print("event.x, event.y = ",event.x,event.y)
    
    def right_click_event(self, event):
        self.cur_pic = (self.cur_pic+1) % self.pic_cnt
        self.show_pic(self.cur_pic)
