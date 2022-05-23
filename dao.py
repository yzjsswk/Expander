import sqlite3
import os
import command

class data_access_object:
    def __init__(self, db_path):
        if not os.path.exists(db_path):
            print('database not found.')
            return
        self.con = sqlite3.connect(db_path, check_same_thread=False)
        self.cr = self.con.cursor()

    def delete_all_rows(self, table_name):
        self.cr.execute(f"delete from {table_name}")

    def commit(self):
        self.con.commit()

    def close(self):
        self.con.close()

class dao_code(data_access_object):
    table_name = 'code'

    def create_table(self):
        #self.cr.execute('drop table code')
        self.cr.execute('''
            create table code (
                c_name comment '命令名' char(10) not null,
                c_group comment '命令组名' char(10) not null, 
                type comment '分类',
                body comment '展开体',
                help comment '注释',
                note comment '备注',
                primary key(c_name, c_group)
            );
        ''')
    
    def insert_one_row(self, name, group, type="", body="", help="", note=""):
        self.cr.execute(f"insert into {self.table_name} values(?,?,?,?,?,?)", (name, group, type, body, help, note))

    def insert_many_rows(self, data):
        self.cr.executemany(f"insert into {self.table_name} values(?,?,?,?,?,?)", data)

    def get_groups(self):
        self.cr.execute(f"select distinct c_group from {self.table_name}")
        res = self.cr.fetchall()
        return [x[0] for x in res]

    def get_cmds_of_group(self, group):
        self.cr.execute(f"select * from {self.table_name} where c_group = '{group}'")
        res = self.cr.fetchall()
        return [command.command(row=x) for x in res]

    def get_types_of_group(self, group):
        self.cr.execute(f"select distinct type from {self.table_name} where c_group = '{group}'")
        res = self.cr.fetchall()
        return [x[0] for x in res]

    def is_exists(self, name, group):
        self.cr.execute(f"select count(*) from {self.table_name} where c_name = '{name}' and c_group = '{group}'")
        res = self.cr.fetchall()
        return res[0][0] != 0
    
    def delete_one_row(self, name, group):
        self.cr.execute(f"delete from {self.table_name} where c_name = '{name}' and c_group = '{group}'")
        
    def get_body_of_cmd(self, name, group):
        if not self.is_exists(name, group):
            return f"command '{name}' not found."
        self.cr.execute(f"select body from {self.table_name} where c_name = '{name}' and c_group = '{group}'")
        res = self.cr.fetchall()
        return res[0][0]
        
    def get_help_of_cmd(self, name, group):
        if not self.is_exists(name, group):
            return f"command '{name}' not found."
        self.cr.execute(f"select help from {self.table_name} where c_name = '{name}' and c_group = '{group}'")
        res = self.cr.fetchall()
        return res[0][0]

class dao_account(data_access_object):
    table_name = 'account'

    def insert_one_row(self, service='无', password='无', phone='无', email='无', nickname='无', note='无'):
        self.cr.execute(f"insert into {self.table_name} values('{service}', '{password}', '{phone}', '{email}', '{nickname}', '{note}')" )
    
    def insert_many_rows(self, data):
        self.cr.executemany(f"insert into {self.table_name} values(?,?,?,?,?,?)", data)

