import sqlite3
from datetime import datetime

conn = sqlite3.connect('personal_finance.db')
c = conn.cursor()

bank_names = {}
catgory_names = {}
all_records = []
all_search_records = []
all_card_informations = []


def is_valid_date(date_string):
    try:
        # Attempt to parse the date string
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        
        # Check if the parsed date matches the original string (to catch invalid dates like February 31st)
        if date_obj.strftime('%Y-%m-%d') != date_string:
            return False
        
        # Check if the month is between 1 and 12
        if not (1 <= date_obj.month <= 12):
            return False
        
        return True
    except ValueError:
        return False

def compare_dates(date_str1, date_str2):
    # Convert the date strings to datetime objects
    date_obj1 = datetime.strptime(date_str1, "%Y-%m-%d")
    date_obj2 = datetime.strptime(date_str2, "%Y-%m-%d")

    # Compare the dates
    if date_obj1 < date_obj2:
        return True
    else:
        return False



def create_tables():
    c.execute('''CREATE TABLE IF NOT EXISTS IEC
                 (id INTEGER PRIMARY KEY, type INTEGER NOT NULL CHECK(type IN (1, -1)), title TEXT NOT NULL UNIQUE, priority INTEGER CHECK(priority IN (1,2,3)))''')

    c.execute('''CREATE TABLE IF NOT EXISTS bank_card
                 (id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE, balance INTEGER NOT NULL)''')

    c.execute('''CREATE TABLE IF NOT EXISTS IET
                 (id INTEGER PRIMARY KEY, IEC_id INTEGER NOT NULL, card_id INTEGER, amount INTEGER NOT NULL, date_time NUMERIC NOT NULL DEFAULT CURRENT_DATE,
                 FOREIGN KEY (IEC_id) REFERENCES IEC(id), FOREIGN KEY (card_id) REFERENCES bank_card(id))''')

    c.execute('''CREATE TRIGGER IF NOT EXISTS update_balance
                 AFTER INSERT ON IET
                 BEGIN
                     UPDATE bank_card
                     SET balance = balance + ((SELECT amount FROM IET WHERE id = NEW.id)*(SELECT type FROM IEC WHERE id = NEW.IEC_id))
                     WHERE id = NEW.card_id;
                 END''')

    c.execute('''CREATE TRIGGER IF NOT EXISTS update_balance_on_delete
                 AFTER DELETE ON IET
                 BEGIN
                     UPDATE bank_card
                     SET balance = balance + (CASE 
                         WHEN (SELECT type FROM IEC WHERE id = OLD.IEC_id) = 1 THEN -OLD.amount
                         WHEN (SELECT type FROM IEC WHERE id = OLD.IEC_id) = -1 THEN OLD.amount
                     END)
                     WHERE id = OLD.card_id;
                 END''')

    c.execute('''CREATE TRIGGER IF NOT EXISTS update_balance_on_update
                 AFTER UPDATE OF amount ON IET
                 FOR EACH ROW
                 BEGIN
                     UPDATE bank_card
                     SET balance = balance + (SELECT CASE 
                         WHEN (SELECT type FROM IEC WHERE id = NEW.IEC_id) = 1 
                             THEN NEW.amount - OLD.amount
                         WHEN (SELECT type FROM IEC WHERE id = NEW.IEC_id) = -1
                             THEN OLD.amount - NEW.amount
                     END)
                     WHERE id = NEW.card_id;
                 END''')

    conn.commit()

def get_bank_names():
    global bank_names
    
    q = c.execute("select name,id from bank_card")    
    for item in q.fetchall():
        bank_names[item[0]] = item[1]

def get_category_names():
    global catgory_names
    
    q = c.execute("select title,id from IEC")
    for item in q.fetchall():
        catgory_names[item[0]] = item[1]    

def get_info():
    get_bank_names()
    get_category_names()
    get_all_record()
    bank_card_informations()

def add_income_expense(category:str, card_name:str, amount:str,date:str=""):
    
    if (card_name not in bank_names) or (category not in catgory_names) or (amount == ""):
        return False
    
    try:
        amount = int(amount)
    except:
        return False
    
    Dflag = is_valid_date(date)

    if (date != "") and (not Dflag):
        return False
    
    
    IEC_id = catgory_names[category]
    card_id = bank_names[card_name]

    
    if Dflag:
        c.execute("INSERT INTO IET (IEC_id, card_id, amount,date_time) VALUES (?, ?, ?,?)", (IEC_id, card_id, amount,date))
    else:

        c.execute("INSERT INTO IET (IEC_id, card_id, amount) VALUES (?, ?, ?)", (IEC_id, card_id, amount))

    conn.commit()
    
    return True

def add_bank_card(bank_name,balance):
    if (bank_name == None) or (balance == None) or (bank_name in bank_names):
        return False
    
    try:
        balance = int(balance)
    except:
        return False
    
    c.execute("INSERT INTO bank_card(name,balance) VALUES (?,?)",(bank_name,balance))
    conn.commit()
    
    # update bank dict
    get_bank_names()
    
    return True

def add_categroy(type,title,priority):
    if (type == None) or (title == None) or (priority == None) or (title in catgory_names):
        return False
    
    if type == "Income":
        type = 1
    else:
        type = -1
    

    c.execute("INSERT INTO IEC(type,title,priority) VALUES (?,?,?)",(type,title,int(priority)))
    conn.commit()
    
    # get category info

    get_category_names()
    return True

def get_all_search_result(category:str,start_date:str="", end_date:str=""):
    
    global all_search_records
    if category == "" :
        return [False] #there is error
    
    
    if (end_date != "" or start_date != ""):
        
        if ((is_valid_date(start_date) and is_valid_date(end_date)) and compare_dates(start_date,end_date)):
        
            c.execute("SELECT IET.amount, IEC.title, bank_card.name, IET.date_time "
            "FROM IET "
            "JOIN IEC ON IET.IEC_id = IEC.id "
            "JOIN bank_card ON IET.card_id = bank_card.id "
            "WHERE (IET.date_time BETWEEN ? AND ?) AND (IEC.title = ?) "
            "ORDER BY IET.date_time DESC",
            (start_date, end_date, category))
        else:
            return [False]

    else:
        c.execute("SELECT IET.amount,IEC.title, bank_card.name ,IET.date_time "
          "FROM IET "
          "JOIN IEC ON IET.IEC_id = IEC.id "
          "JOIN bank_card ON IET.card_id = bank_card.id "
          "WHERE IEC.title is ?"
          "ORDER BY IET.date_time DESC", (category,))

    all_search_records = c.fetchall()
    return [True,all_search_records]

def get_all_record():
    
    global all_records
    c.execute("SELECT IET.id,IET.amount,IEC.title, bank_card.name ,IET.date_time "
            "FROM IET "
            "JOIN IEC ON IET.IEC_id = IEC.id "
            "JOIN bank_card ON IET.card_id = bank_card.id ORDER BY IET.date_time DESC")
    all_records =  c.fetchall()
    return all_records

def bank_card_informations():
    global all_card_informations
    c.execute("SELECT bank_card.name, " 
              "SUM(CASE WHEN IEC.type = -1 THEN IET.amount ELSE 0 END) AS total_withdrawals, "
              "SUM(CASE WHEN IEC.type = 1 THEN IET.amount ELSE 0 END) AS total_deposits, "
              "bank_card.balance "
              "FROM IET "
              "JOIN IEC ON IET.IEC_id = IEC.id "
              "JOIN bank_card ON IET.card_id = bank_card.id "
              "GROUP BY bank_card.name")
    all_card_informations =  c.fetchall()
    return all_card_informations

def delete_transaction(transaction_id):
    c.execute("DELETE FROM IET WHERE id = ?", (transaction_id,))
    conn.commit()

def update_transaction(transaction_id, new_amount:int):
    c.execute("UPDATE IET SET amount = ? WHERE id = ?", (new_amount, transaction_id))
    conn.commit()
def update_transaction_Date(transaction_id, date):
    c.execute("UPDATE IET SET date_time = ? WHERE id = ?", (date, transaction_id))
    conn.commit()

def Edit_IET(ID,na,nd):

    
    Dflag = is_valid_date(nd)
    if (nd != "") and (not Dflag):
        return False
    
    if nd != "" :
        update_transaction_Date(ID,nd)
    
    if na != "":
        try:
            na = int(na)
        except:
            return False
        update_transaction(ID,na)   
    return True

def get_all_Income_Expence(category:str,start_date:str="", end_date:str=""):
    global all_search_records 

    if category == "All_income":
        category = 1
    elif category == "All_expence":
        category = -1
        

    if (end_date != "" or start_date != ""):
        
        if ((is_valid_date(start_date) and is_valid_date(end_date)) and compare_dates(start_date,end_date)):
        
            c.execute("SELECT IET.amount, IEC.title, bank_card.name, IET.date_time "
            "FROM IET "
            "JOIN IEC ON IET.IEC_id = IEC.id "
            "JOIN bank_card ON IET.card_id = bank_card.id "
            "WHERE (IET.date_time BETWEEN ? AND ?) AND (IEC.type = ?) "
            "ORDER BY IET.date_time DESC",
            (start_date, end_date,category))
        else:
            return [False]

    else:
        c.execute("SELECT IET.amount,IEC.title, bank_card.name ,IET.date_time "
          "FROM IET "
          "JOIN IEC ON IET.IEC_id = IEC.id "
          "JOIN bank_card ON IET.card_id = bank_card.id "
          "WHERE IEC.type is ?"
          "ORDER BY IET.date_time DESC", (category,))

    all_search_records = c.fetchall()
    return [True,all_search_records]

    
create_tables()
get_info()