import tkinter
from tkinter import END, ttk
import dao
import command

class cmd_manager:
    def __init__(self, dao: dao.dao_code, cur_group: str):
        self.dao = dao
        self.cur_group = cur_group

        self.root = tkinter.Tk()
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.w = 800
        self.h = 600
        self.root.maxsize(width=self.w, height=self.h)
        self.root.minsize(width=self.w, height=self.h)
        self.root.geometry(f"{self.w}x{self.h}+{(self.screen_width-self.w)//2}+{(self.screen_height-self.h)//2}")
        self.root.title(f"Commands In Group '{cur_group}'")
        self.tv = ttk.Treeview (
            self.root,
            columns = ("help"),
            #show = 'headings',
            height = 26
        )
        self.tv.column("#0", width=100, anchor='center')
        self.tv.column("help", width=670, anchor='w')
        self.tv.heading("#0", text="命令")
        self.tv.heading("help", text="说明")
        self.tv.pack(pady=15)
        self.tv.bind('<Double-1>', self.show)
        self.refresh()
        self.root.mainloop()

    def refresh(self):
        for row in self.tv.get_children():
            self.tv.delete(row)
        
        self.cmds = self.dao.get_cmds_of_group(self.cur_group)
        self.types = self.dao.get_types_of_group(self.cur_group)
        self.type_to_tvID = {}
        self.tvID_to_type = {}
        for type in self.types:
            id = self.tv.insert('', 'end', text=type, open=True)
            self.type_to_tvID[type] = id
            self.tvID_to_type[id] = type
        self.tvID_to_cmdIndex = {}
        for i, cmd in enumerate(self.cmds):  
            id = self.tv.insert(self.type_to_tvID[cmd.type], 'end', text=cmd.name, values=(cmd.get_rows_of_help()[0],))
            self.tvID_to_cmdIndex[id] = i

    
    def selected_thing(self, selection):
        if len(selection) > 0:
            selection = selection[0]
        if selection in self.tvID_to_type:
            return "type", selection
        if selection in self.tvID_to_cmdIndex:
            return "cmd", selection
        return "nothing", selection

    def show(self, event):
        what_is_selected, selected_tvid = self.selected_thing(self.tv.selection())
        if what_is_selected == "cmd":
            selected_cmd = self.cmds[self.tvID_to_cmdIndex[selected_tvid]]
        else:
            selected_cmd = command.command()

        tl = tkinter.Toplevel(self.root)
        w, h = 600, 700
        tl.maxsize(width=w, height=h)
        tl.minsize(width=w, height=h)
        tl.geometry(f"{w}x{h}+{(self.screen_width-w)//2}+{(self.screen_height-h)//2}")
        tl.title("Edit")

        text_name = tkinter.Entry(tl)
        text_name.place(x=70, y=20)
        text_name.insert(0, selected_cmd.name)
        label_name = tkinter.Label(tl, text="命令: ")
        label_name.place(x=30, y=20)

        text_type = tkinter.Entry(tl)
        text_type.place(x=340, y=20)
        text_type.insert(0, selected_cmd.type)
        label_type = tkinter.Label(tl, text="分类: ")
        label_type.place(x=300, y=20)

        text_help = tkinter.Text(tl, width=75, height=15)
        text_help.place(x=35, y=80)
        text_help.insert(0.0, selected_cmd.help)
        label_help = tkinter.Label(tl, text="说明: ")
        label_help.place(x=30, y=50)

        text_body = tkinter.Text(tl, width=75, height=25)
        text_body.place(x=35, y=320)
        text_body.insert(0.0, selected_cmd.body)
        label_body = tkinter.Label(tl, text="展开体: ")
        label_body.place(x=30, y=290)

        def clear():
            #text_name.delete(0, END)
            #text_type.delete(0, END)
            text_help.delete(0.0, END)
            text_body.delete(0.0, END)
        button_clear = tkinter.Button(tl, text="清空内容", command=clear)
        button_clear.place(x=35, y=660)

        def delete():
            name = text_name.get().strip()
            if self.dao.is_exists(name, self.cur_group):
                self.dao.delete_one_row(name, self.cur_group)
                self.dao.commit()
                tl.destroy()
                self.refresh()
            else:
                print('error')

        def modify():
            name = text_name.get().strip()
            type = text_type.get().strip()
            help = text_help.get(0.0, END)
            body = text_body.get(0.0, END)
            if self.dao.is_exists(name, self.cur_group):
                self.dao.delete_one_row(name, self.cur_group)
            self.dao.insert_one_row(name, self.cur_group, type, body, help, "")
            self.dao.commit()
            tl.destroy()
            self.refresh()

        button_del = tkinter.Button(tl, text="删除命令", command=delete)
        button_del.place(x=515, y=660)

        button_mod = tkinter.Button(tl, text="提交", command=modify)
        button_mod.place(x=460, y=660) 


        tl.mainloop()



