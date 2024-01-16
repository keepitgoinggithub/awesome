import json

class Request:

    def __init__(self, project, date, total, jira, table, contents ): 
        self.project = project 
        self.date = date 
        self.total = total
        self.jira = jira 
        self.table = table
        self.contents = contents
    def __repr__(self): 
        return repr((self.project, self.date, self.total,self.jira, self.table, self.contents))

    
class Content:
    def __init__(self, serial_no, condition, records): 
        self.serial_no = serial_no 
        self.condition = condition
        self.records = records
    def __repr__(self): 
        return repr((self.serial_no,self.condition,self.records)) 

class Record:
    def __init__(self, field, value):
        self.field = field
        self.value = value
    def __repr__(self): 
        return repr((self.field, self.value))

'''
record = Record('fee_status','0','2')
#print(record)
content = Content(1,"EBAO-8888","t_policy_fee","fee_id=12345678",record)
#print(content)
request = Request('EBAO', '2023-12', 50, content)
json_str = json.dumps(request, default=lambda o: o.__dict__, sort_keys=False, indent=2)
print(json_str)
'''
