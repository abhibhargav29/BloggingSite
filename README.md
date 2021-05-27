# Blog Site with Face Recognition

## Create Database
<p align="justify">
The CreateDatabase sql script needs to be run before to make our database and the corresponding tables that store the details of the user and the blog posts. The database is 
created with the name of blogs and if such a database pre-exists, it is automatically deleted and replaced by this new database.
</p>

## BlogSite.py
<p align="justify">
This is the python file with all the code of rendering templates and the connection of database with the front end, our front end is the templates and this file renders those 
templates at appropriate times. It also contains the functions for validating and registering faces using face_recognition library. The validation is done by matching 75% of 
facial features.

## Templates
<p align="justify">
This folder has html files that are actually our front end that interact with our python code using flask. We use jinja2 syntax for using the variables from the code. 
The variable interchange between code and front end is facilitated by GET and POST requests in flask's various functions.
</p>

<p align="justify">
<ins>Base.html:</ins>
This is our base html template every other template basically inherits from this class. The base class has all the basic things like styling, initializing bootstrap, use of 
containers, setting up enoding and stuff like that. It also has the navigation bar which will be displayed for every page.
</p>

<p align="justify">
<ins>LogIn.html:</ins>
This is the home page as well and opens up first, We can login by entering username and password or register as a new user and then log in.
</p>

<p align="justify">
 <ins>CheckFace.html:</ins>
 This is the page that pops up if the user has allowed face detection on his/her account. It has a video stream and user can capture an image and check if it verifies with the 
 saved embeddings.
</p>
 
<p align="justify">
<ins>Register.html:</ins>
This is the page of registering new user with name username and password. After clicking on Register, the user will be saved and can then login.
</p>

<p align="justify">
<ins>Capture.html:</ins>
This page captures the image of newly registered person and saves their face embeddings for future recognition. The user can skip if they don't want face recognition. 
</p>

<p align="justify">
<ins>Main.html:</ins>
This is the main page of our site that has all the posts as well as an option to make a new post for the user who is logged in. Each post can be deleted or edited by the user 
 who created it. The posts are displayed in the order they were posted, that is oldest to latest.
</p>

<p align="justify">
<ins>Edit.html:</ins>
This is the edit window where a user can edit the post title or content.
</p>

## Final Web App
<p align="justify">
You can see the final app deployed on heroku here: https://blogging-site29.herokuapp.com/, Try to view it in desktop view or on laptop screen as some pages are not optimized 
for phone screen. The app is connected to the cloud database clearDb that is provided by heroku itself as an add-on service.
</p>
