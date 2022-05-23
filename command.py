class command:
    def __init__(self, row=(), name="", group="", type="", help="", body=""):
        if len(row) > 0:
            self.name = row[0]
            self.group = row[1]
            self.type = row[2]
            self.help = row[4]
            self.body = row[3]
        else:
            self.name = name
            self.group = group
            self.type = type
            self.help = help
            self.body = body

    def get_rows_of_help(self):
        return self.help.strip().split('\n')

    def get_rows_of_body(self):
        return self.body.strip().split('\n')
    