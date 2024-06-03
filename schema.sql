-- IEC  = income expence categroy

CREATE TABLE IF NOT EXISTS IEC(
    "id" INTEGER,
    "type" INTEGER  NOT NULL CHECK("type" IN (1, -1)), -- 1 for income and -1 is for expence
    "title" TEXT NOT NULL UNIQUE,
    "priority" INTEGER CHECK("priority" IN (1,2,3)),
    PRIMARY KEY("id")
);

CREATE TABLE IF NOT EXISTS bank_card(
    "id" INTEGER,
    "name" TEXT NOT NULL UNIQUE,
    "balance" INTEGER NOT NULL,
    PRIMARY KEY("id")
);
-- IET = income expence table

CREATE TABLE IF NOT EXISTS IET(
    "id" INTEGER,
    "IEC_id" INTEGER NOT NULL,
    "card_id" INTEGER,
    "amount" INTEGER NOT NULL,
    "date_time" NUMERIC NOT NULL DEFAULT CURRENT_DATE,
    PRIMARY KEY("id"),
    FOREIGN KEY("IEC_id") REFERENCES "IEC"("id"),
    FOREIGN KEY("card_id") REFERENCES "bank_card"("id")
);

-- Create a trigger that updates the balance in bank_card table when a new income or expense is added
CREATE TRIGGER IF NOT EXISTS update_balance
AFTER INSERT ON IET
BEGIN
    UPDATE bank_card
    SET balance = balance + ((SELECT amount FROM IET WHERE id = NEW.id)*(SELECT "type" FROM IEC WHERE "id" = NEW.IEC_id))
    WHERE id = NEW.card_id;
END;

-- Create a trigger that updates the balance in bank_card table when a income or expense is deleted
CREATE TRIGGER IF NOT EXISTS update_balance_on_delete
AFTER DELETE ON IET
BEGIN
    UPDATE bank_card
    SET balance = balance + (CASE 
        WHEN (SELECT type FROM IEC WHERE id = OLD.IEC_id) = 1 THEN -OLD.amount
        WHEN (SELECT type FROM IEC WHERE id = OLD.IEC_id) = -1 THEN OLD.amount
    END)
    WHERE id = OLD.card_id;
END;
-- Create a trigger that updates the balance in bank_card table when a income or expense is changed on amount
CREATE TRIGGER IF NOT EXISTS update_balance_on_update
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
END;