import sqlite3
from datetime import datetime

conn = sqlite3.connect('personal_finance.db')
c = conn.cursor()

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

def add_income_expense(IEC_id, card_id, amount):
    c.execute("INSERT INTO IET (IEC_id, card_id, amount) VALUES (?, ?, ?)", (IEC_id, card_id, amount))
    conn.commit()

def get_all_transactions(start_date=None, end_date=None):
    if start_date and end_date:
        c.execute("SELECT IET.id, IEC.title, IET.amount, IET.date_time, bank_card.name "
                  "FROM IET "
                  "JOIN IEC ON IET.IEC_id = IEC.id "
                  "JOIN bank_card ON IET.card_id = bank_card.id "
                  "WHERE IET.date_time BETWEEN ? AND ?",
                  (start_date, end_date))
    else:
        c.execute("SELECT IET.id, IEC.title, IET.amount, IET.date_time, bank_card.name "
                  "FROM IET "
                  "JOIN IEC ON IET.IEC_id = IEC.id "
                  "JOIN bank_card ON IET.card_id = bank_card.id")
    return c.fetchall()

def delete_transaction(transaction_id):
    c.execute("DELETE FROM IET WHERE id = ?", (transaction_id,))
    conn.commit()

def update_transaction(transaction_id, new_amount):
    c.execute("UPDATE IET SET amount = ? WHERE id = ?", (new_amount, transaction_id))
    conn.commit()

create_tables()