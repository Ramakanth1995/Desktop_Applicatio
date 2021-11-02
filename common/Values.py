import os

BITMAP_IMAGE = os.path.normpath(os.getcwd() + "/images/favicon.ico")
LOGIN_PHOTO = os.path.normpath(os.getcwd() + "/images/indian.gif")
MAIN_WINDOW_PHOTO = os.path.normpath(os.getcwd() + "/images/groceries_main.jpg")
ITEM_TYPE = [
    'VEGETABLE',
    'BEVERAGE',
    'DAIRY PRODUCT',
    'KITCHENWARE',
    'BABY CARE',
    'BREAD & BAKERY',
    'BISCUITS'
    'CAKES',
    'DESSERT',
    'FLOUR',
    'RICEITEM',
    'CEREALS',
    'DRYFRUITS & NUTS',
    'COSMETICS',
    'FLOWERS',
    'FRUITS',
    'HOUSE-CLEANING',
    'HOUSEWARES',
    'SOFTDRINK',
    'SPICES'
]

DATABASE_NAME = 'db_name'
DATABASE_SECTION = 'DATABASE'
GENERAL_SECTION = 'GENERAL'
CONFIG_FILE_NAME = 'config.ini'
HOSTNAME = 'host_name'
PORT = 'port_number'
USERNAME = 'user'
USER_NAME = 'Username'
PASSWORD = 'password'
ITEM_CODE_MAX_RANGE = 'item_code_max_range'
SQL_FILE = os.path.normpath(os.getcwd() + "/grocery.sql")
CGST = 9
SGST = 9
SECRET_KEY = "grostor"
LENGTH_OF_RANDOM_PASSWORD = 10
PASSWORD_REGEX = "[^@]+@[^@]+\.[^@]+"  #checks @ symbol and at least one . symbol
SENDER_EMAIL = 'sender_email'
SENDER_EMAIL_PASSWORD = 'sender_email_password'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_SERVER_PORT = 587

