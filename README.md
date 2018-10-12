# TvSeriesReminder
Reminds about the next episode of all the favourite TV series of mutiple users.
Requires Email and comma seperated list of tv shows. 

# Modules

 1. ### [imdb.py](https://github.com/awesome-arjun11/TvSeriesReminder/blob/master/imdb.py)
	 Contains [IMDB_API](#imdb_api) class to extract the details about next episode using show name keyword.
 2. ### [utility.py](https://github.com/awesome-arjun11/TvSeriesReminder/blob/master/utility.py)
	Contains [send_email](#send_emailrecipient-msg) function to send the email to all users in the DB, and [TempDB](#tempdb) class to interect with a local sqlite database.
 3. ### [main.py](https://github.com/awesome-arjun11/TvSeriesReminder/blob/master/main.py)
	 Driver program to take [input](#input_data) and store data in db, [format and email episode information](#inform_user) to all users simultaneously using mutliprocessing.

# Documentation

 1. ## Classes
	* ### [IMDB_API](https://github.com/awesome-arjun11/TvSeriesReminder/blob/35b3d0e368d29a236e80760428dd045e05b3a61b/imdb.py#L8)
		* **IMDB_API.id_search(show_name)**:
			This function uses imdb's suggest api,which returns best suggestions based on keywords as json,its faster than scraping webpage for title id.  
**:param** show_name:
**:return:** IMDB title id as string

		* **IMDB_API.id_search_fallback(show_name)**:
			This is a fallback function which scrapes title id for the most popular match of given keyword.
**:param** show_name:
**:return:** IMDB title id as string

		* **IMDB_API.getnextepisode(show_name)**:
**:param** show_name: Tv series name string
**:return:** String to be emailed informing about given show's next episode.

	* ### [TempDB](https://github.com/awesome-arjun11/TvSeriesReminder/blob/35b3d0e368d29a236e80760428dd045e05b3a61b/utility.py#L42)
		* **TempDB.insert_users(db_buffer)**
			Inserts new email and tv series data to db, if email exists fallback to 	updating tv series list  
**:param** db_buffer: List of tuples with email and tv series data for each user

		* **TempDB.get_all_user()**
			**:return:** All users data in db

		* **TempDB.update_user(db_buffer)**
			Updates tv series list for old users
			**:param** db_buffer:
			
		* **TempDB.initdb()**
			Initialize sqlite db and create table if db not initialized

		* **TempDB.get_formatted_data()**
			**:return:** List of dictionary with email and requested tv shows

2. ## Functions
	* ### [send_email](https://github.com/awesome-arjun11/TvSeriesReminder/blob/35b3d0e368d29a236e80760428dd045e05b3a61b/utility.py#L13)(recipient, msg)
		Sends email  
		**:param** recipient: Recipient of email:param msg: body of emai
		>**Note:**  SMTP settings are required to be set in [utility.py](https://github.com/awesome-arjun11/TvSeriesReminder/blob/master/utility.py) as global variables (for now). Sensitive info like username and password can also be set through environment variables. **TSR_SMTP_USER** and **TSR_SMTP_PASS**

	* ### [input_data](https://github.com/awesome-arjun11/TvSeriesReminder/blob/35b3d0e368d29a236e80760428dd045e05b3a61b/main.py#L7)()
		Inputs email and tv series for multiple users.
		**:return:** New/Updated user data to be stored in db
		
	* ### [inform_user](https://github.com/awesome-arjun11/TvSeriesReminder/blob/35b3d0e368d29a236e80760428dd045e05b3a61b/main.py#L21)()
		Collects information about next episode of each tv series requested by 			user, formats it in email body and sends Email  
**:param** user: Dictionary with email and requested tvshows

	* ### [main](https://github.com/awesome-arjun11/TvSeriesReminder/blob/35b3d0e368d29a236e80760428dd045e05b3a61b/main.py#L37)()
		Driver for whole application.
		
