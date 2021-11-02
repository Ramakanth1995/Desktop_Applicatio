CREATE DATABASE GROCERY;
USE GROCERY;
CREATE TABLE IF NOT EXISTS grocerylist (
    Item_No INT,
    Item_Name VARCHAR(255) DEFAULT NULL,
    Quantity_Remain INT DEFAULT NULL,
    Item_Cost VARCHAR(100) DEFAULT NULL,
    Expiry_Date VARCHAR(255),
    Manufactured_By VARCHAR(255) DEFAULT NULL,
	Item_Type VARCHAR(255) DEFAULT NULL,
	Item_Code VARCHAR(30) DEFAULT NULL
);
INSERT INTO grocerylist VALUES (1, 'Milk', 25, '23.00', '12/10/2018', 'Prairie', 'DAIRY PRODUCT', 'DAIRY-1234567890');
INSERT INTO grocerylist VALUES (2, 'Sandwich Wheat ', 93, '9.99', '08/31/2019', 'Essential Everyday', 'BREAD & BAKERY', 'BREAD-1478523690');
INSERT INTO grocerylist VALUES (4, 'Chocalate', 343, '15.33', '12/04/2019', 'Tempteys', 'DAIRY PRODUCT', 'DAIRY-3698521470');
INSERT INTO grocerylist VALUES (5, 'Cake', 113, '12.99', '12/12/2019', 'Hersheys', 'CAKES', 'CAKES-0123654987');
INSERT INTO grocerylist VALUES (6, 'Marie ', 122, '2.99', '12/01/2019', 'Britannia', 'BISCUITS', 'BISCU-7896543210');
INSERT INTO grocerylist VALUES (7, 'Biscuits', 258, '64.25', '25/12/2018', 'Karachi', 'BISCUITS', 'BISCU-2587533571');
INSERT INTO grocerylist VALUES (9, 'Perfume', 12, '152.32', '28/08/2019', 'Fogg', 'COSMETICS', 'COSME-1599514753');
INSERT INTO grocerylist VALUES (10, 'Kaju', 47, '850.85', '25/04/2020', 'Haldi', 'DRYFRUITS & NUTS', 'DRYFR-1236549875');
INSERT INTO grocerylist VALUES (11, 'Knifes', 15, '84.47', '21/04/2020', 'WeCool', 'KITCHENWARE', 'KITCH-0147852369');
INSERT INTO grocerylist VALUES (13, 'Apple', 25, '25.00', '12/11/2018', 'ITC', 'FRUITS', 'FRUIT-1587423240');
INSERT INTO grocerylist VALUES (14, 'Basmati', 12, '95.00', '25/09/2019', 'India Gate', 'RICEITEM', 'RICEI-8574698525');
CREATE TABLE IF NOT EXISTS customer (
    name varchar(50),
    address varchar(300),
	phone varchar(15)
);
INSERT INTO customer VALUES('Hemanth','shardanagar','9125847120');
INSERT INTO customer VALUES('apurva','springfield,illinois','8745631278');
INSERT INTO customer VALUES('apurva','springfield, illinois','8845712369');
INSERT INTO customer VALUES('sumiit','srinagar','7548961234');
INSERT INTO customer VALUES('Rakshitha','shardanagar','7744112233');
INSERT INTO customer VALUES('Kumar','Bangalore','7894561230');
INSERT INTO customer VALUES('Teja','Karnataka','1478529630');
INSERT INTO customer VALUES('Shilpa','s','4567891236');
INSERT INTO customer VALUES('sowmya','illinois','7852369871');
INSERT INTO customer VALUES('sana','india','9100415587');
INSERT INTO customer VALUES('tarun','sprinfield','6975412770');
INSERT INTO customer VALUES('somya','Chicago','6975412445');
INSERT INTO customer VALUES('shreya','illinois','8423579612');
INSERT INTO customer VALUES('sana','hyd','8966554471');
INSERT INTO customer VALUES('rohit','asas','7814526987');
INSERT INTO customer VALUES('Kiran','Hyderabad','4569321247');
INSERT INTO customer VALUES('srinija','springfield,illinois','9875310252');
INSERT INTO customer VALUES('somya','springfield,illinois','9875310252');
CREATE TABLE IF NOT EXISTS bill (
    cusname varchar(50),
	cusphone varchar(15),
    cusaddress varchar(50),
    items varchar(50),
    totalcost varchar(50),
    billingdate varchar(50),
    billno varchar(50),
    bill varchar(5000)
);
COMMIT;
create TABLE IF NOT EXISTS login
(
  username           varchar(50)            not null,
  salt               blob                   not null,
  hash               blob                   not null,
  email_id           varchar(100)           not null,
  is_admin           tinyint(1) default '0' null,
  currently_loggedin tinyint(1) default '0' null,
  created_time       varchar(50)            not null,
  is_active          tinyint(1) default '1' null,
  constraint login_email_id_uindex
  unique (email_id)
);
COMMIT;
INSERT INTO login VALUES ('admin', 0x243262243132244754586552304C76756946784B6B302F634762374C4F, 0x243262243132244754586552304C76756946784B6B302F634762374C4F666467667A62376856316F684F564C3472534C4E64344D33646E78342F464B, 'ramakanth406ail.com', 1, 0, '2018-09-17 18:14:31.052558',1);
COMMIT;