# Blog Site

## Create Database
The CreateDatabase sql script needs to be run before to make our database and the corresponding tables that store the details of the user and the blog posts. The database is 
created with the name of blogs and if such a database pre-exists, it is automatically deleted and replaced by this new database.

## BlogSite.py
This is the python file with all the code of rendering templates and the connection of database with the front end, our front end is the templates and this file renders those 
templates at appropriate times.

## Templates
This folder has html files that are actually out front end that interact with our python code using jinja2 and flask. We use jinja2 syntax for using the variables from the code. 
The variable interchange between code and front end is facilitated by GET and POST requests in flask's various functions

<ins>base.html:</ins>
This is our base html template every other template basically inherits from this class. The base class has all the basic things like styling, initializing bootstrap, use of 
containers, setting up enoding and stuff like that. It also has the navigation bar which will be displayed for every page.

<ins>Login.html:</ins>
This is the home page as well and opens up first, We can login by entering username and password or register as a new user and then log in.

<ins>Register.html:</ins>
This is the page of registering new user with name username and password. After clicking on Register, the user will be saved and can then login.

<ins>Main.html:</ins>
This is the main page of our site that has all the posts as well as an option to make a new post for the user who is logged in. Each post can be deleted or edited by the user who
created it.

<ins>Edit.html:</ins>
This is the edit window where a user can edit the post title or content.
