create table users (
    id varchar(50) primary key,
    password varchar(50),
    salt integer
);

create table students (
    studentname varchar(50) not null unique
);

create table questions (
    question varchar(50),
    image varchar(50)
);


/*Accounts*/
/*Use accountcreation.py instead*/

/*Students - Use the web interface instead*/
/*INSERT INTO students (studentname) VALUES('John 117');*/

/*Question and image pairs*/
INSERT INTO questions VALUES('find the circumference of the circle if r = 2', 'q1.png');
INSERT INTO questions VALUES('find the value of s if the area of the square is 16', 'q2.png');
INSERT INTO questions VALUES('solve for x the figure above', 'q3.png');
INSERT INTO questions VALUES('solve for w in the figure above', 'q4.png');
