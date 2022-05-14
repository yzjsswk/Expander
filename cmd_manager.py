import os
import tkinter
from PIL import Image, ImageTk



class command:
    def __init__(self, name, note, body):
        self.name = name
        self.note = note
        self.body = body

class cmd_manager:
    def __init__(self, cmd_path):
        self.work_path = os.getcwd()
        if os.path.isabs(cmd_path):
            self.cmd_path = cmd_path
        else:
            self.cmd_path = os.path.join(self.work_path, cmd_path)
        if not os.path.exists(self.cmd_path):
            os.mkdir(self.cmd_path)
            print('command dir made.')
        self.group_list = []
        for name in os.listdir(self.cmd_path):
            full_path = os.path.join(self.cmd_path, name)
            if os.path.isdir(full_path):
                self.group_list.append(name)
        self.cur_group = "null"
        self.div_list = []
        self.cmd = []
        self.cmd_map = {}
        self.div = {}

    def load_cmd(self, file_content):
        op = ""
        note = """"""
        body = """"""
        flag = True
        for row in file_content:
            if len(row) > 1 and row[0] == '#' and row[1] == '#':
                note += row[2:].lstrip()
                continue
            if flag:
                op = row.strip()
                flag = False
            else:
                body += row
        return command(op, note, body)
    
    def load_group(self, group_name):
        if not group_name in self.group_list:
            print(f'group {group_name} not exists.')
            return
        self.div_list.clear()
        self.cmd.clear()
        self.cmd_map.clear()
        txt_list = []
        group_path = os.path.join(self.cmd_path, group_name)
        for div_name in os.listdir(group_path):
            div_path = os.path.join(group_path, div_name)
            if os.path.isdir(div_path):
                self.div_list.append(div_name)
                for cmd_name in os.listdir(div_path):
                    cmd_path = os.path.join(div_path, cmd_name)
                    if os.path.isfile(cmd_path) and cmd_path.endswith(('.txt')):
                        txt_list.append(cmd_path)
                        self.div[cmd_name] = div_name
            else:
                if os.path.isfile(div_path) and div_path.endswith(('.txt')):
                    txt_list.append(div_path)
                    self.div[div_name] = '未分类'
        for txt_path in txt_list:
            with open(txt_path, encoding = 'utf-8') as cmd_file:
                cmd = self.load_cmd(cmd_file.readlines())
                self.cmd.append(cmd)
                self.cmd_map[cmd.name] = len(self.cmd) - 1
        self.cur_group = group_name
        print(f'read {len(self.cmd)} commands.')
        print(f"group change to '{group_name}'.")

    def cmd_call(self, origin_cmd: str):
        parts = origin_cmd.split(':')
        op = parts[0]
        if len(parts) > 1:
            args = parts[1].split(',')
        else:
            args = []
        if op == 'help':
            return self.cmd_note(args[0])
        if not op in self.cmd_map:
            return f"command '{op}' not found."
        body = self.cmd[self.cmd_map[op]].body
        arg_id = 0
        for arg in args:
            body = body.replace('{%d}'%arg_id, arg)
            arg_id = arg_id + 1
        return body

    def cmd_note(self, cmd_name):
        if not cmd_name in self.cmd_map:
            return f"command '{cmd_name}' not found."
        return self.cmd[self.cmd_map[cmd_name]].note

class cmd_view:
    def __init__(self, cmd, div):
        pass
