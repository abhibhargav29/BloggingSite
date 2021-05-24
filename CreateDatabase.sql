-- DELETE IF PRE EXISTING DATABASE IS THERE
DROP DATABASE IF EXISTS Blogs;

CREATE DATABASE Blogs;
USE Blogs;

-- TABLE THAT WILL HAVE THE USERS
CREATE TABLE Users(
    UserName VARCHAR(15) UNIQUE NOT NULL,
    Password VARCHAR(10) NOT NULL,
    RealName VARCHAR(20) NOT NULL
);

-- TABLE THAT WILL HAVE ALL THE BLOGS
CREATE TABLE BlogPosts(
    BlogId INT(5) PRIMARY KEY AUTO_INCREMENT,
    BlogTitle VARCHAR(50) NOT NULL,
    AuthorUserName VARCHAR(15) REFERENCES Users(UserName),
    BlogText TEXT NOT NULL,
    BlogDate DATETIME DEFAULT NOW()
);
