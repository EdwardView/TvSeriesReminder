import multiprocessing
from imdb import IMDB_API
from utility import send_email, TempDB



def input_data():
    """
    :return: New/Updated user data to be stored in db
    """
    db_buffer = []
    print("To quit/skip entering data leave Email address blank")
    email = input("Email address:")
    while(email):
        tvseries = input("TV Series:")
        db_buffer.append((email, tvseries))
        email = input("Email address:")
    return db_buffer


def inform_user(user):
    """
    Collects information about next episode of each tv series requested by user and
    Sends Email
    :param user: Dictionary with email and requested tvshows
    :return:
    """
    imdb = IMDB_API()
    template = "Tv series name: {}\nStatus:{}\n\n"
    email_body = ""
    for series in user.get("tvseries"):
        series = series.strip()
        email_body += template.format(series, imdb.getnextepisode(series))
    send_email(user.get("email"), email_body)


def main():
    """
    Driver for the scripts
    :return:
    """
    db = TempDB()
    db_buffer = input_data()
    if db_buffer:
        db.insert_users(db_buffer)
    user_data = db.get_formatted_data()
    for user in user_data:
        #processing each user simultaneously
        p = multiprocessing.Process(target=inform_user, args=(user,))
        p.start()



if __name__ == '__main__':
    main()
