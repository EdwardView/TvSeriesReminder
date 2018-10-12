import os
import smtplib
import sqlite3

# SMTP SERVER SETTINGS
# Username and Password can also be set as environment variable of name TSR_SMTP_USER and TSR_SMTP_PASS
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_user = ''
smtp_password = ''
smtp_from_addr = ''   # Leave blank to keep it same as user

def send_email(recipient, msg):
    """
    Sends email
    :param recipient: Recipient of email
    :param msg: body of email
    :return:
    """
    # set environment variable TSR_SMTP_USER or set global variable above
    user = os.environ.get("TSR_SMTP_USER",smtp_user)

    # set environment variable TSR_SMTP_PASS or set global variable above
    passwd = os.environ.get("TSR_SMTP_PASS",smtp_password)

    # set environment variable TSR_SMTP_FROM_ADDR or set global variable above
    fromaddr = os.environ.get("TSR_SMTP_FROM_ADDR",smtp_from_addr) or user

    to = [recipient]
    subject = "Tv Series Schedule"
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s 
                """ % (fromaddr, ", ".join(to), subject, msg)

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.ehlo()
    server.starttls()
    server.login(user, passwd)
    server.sendmail(fromaddr, to, message)
    server.close()


class TempDB:
    def __init__(self):
        self.conn = sqlite3.connect('users.db')
        self.c = self.conn.cursor()
        self.initdb()

    def get_formatted_data(self):
        """
        :return: List of dictionary with email and requested tv shows
        """
        formatted_data = []
        all_users = self.get_all_user()
        for user in all_users:
            formatted_data.append({'email': user[0],'tvseries':[i.strip() for i in user[1].split(",")]})
        return formatted_data

    def insert_users(self,db_buffer):
        """
        inserting new email to db, if email exists fallback to updating tv series list
        :param db_buffer: List of tuples with email and tv series data for each user
        :return:
        """
        q = "INSERT INTO users VALUES ( ? ,? )"
        with self.conn:
            for i in db_buffer:
                try:
                    self.c.execute(q, i)
                except sqlite3.IntegrityError:
                    self.update_user(i)

    def get_all_user(self):
        """
        :return: ALl users data in db
        """
        self.c.execute("SELECT * FROM users")
        return self.c.fetchall()

    def update_user(self,db_buffer):
        """
        Updates tv series list for old users
        :param db_buffer:
        :return:
        """
        q = """UPDATE users SET tvseries = ?
                WHERE email = ? """
        with self.conn:
            self.c.execute(q, db_buffer)

    def initdb(self):
        try:
            with self.conn:
                self.c.execute("""CREATE TABLE users(
                        email text NOT NULL UNIQUE,
                        tvseries text NOT NULL
                            )""")
        except sqlite3.OperationalError:
            pass

