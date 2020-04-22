# **Awesome-Reads** [books(./static/images/book-clipart.png)]

This book review project is aimed at anyone who enjoys reading and talking about what they have read. Viewing & reviewing books, saving them in a library/list for future use,
finding new books and Authors, reading other peoples reviews, reading qoutes from books they are interested in. I'm an avid reader and was pretty motivated 

## **UX**

The Website is fully responsive and uses Mongo DB to hold users collection and a book reviews collection. The user is able to register and login and view reviews. Logged in users are able to Create, update (edit) and delete their own reviews. A user can also log out.

Each review on the home page can be clicked onto and that will load the single recipe page which shows the entire entry. If the user created the review on their page they will be able to edit and delete the review, and also profile when they need to.

The add review allows the logged in user to create a review and enter it onto the database.

### **Project Goals**  

wireframes 

## **User Stories**

> As a user I want to be able to save the books I wanted to read in the future.
>
> As a user I want to be able to like books that I'm interest in.
>
> As a user I want to be able to make a list of books I've already read.
>
> As a user I want to be able to make a profile.
>
> As a user I want to be able to save my reviews to my profile
>
> As a user I want to be able to view books reviewed by other people
>
> As a user I want to be able to save my review and others



## **Features**

1. Register and Login - I really enjoyed building the profile

2. The add review form

3. Features left to implement 



## **Technolgoies Used**

Flask
Flask Sessions
werkzeug.security
My Linux terminal, this time I only used the terminal to manage my project tree.
MongoDB
MONGODB GUI
Bootstrap
Virtualenv
GitHub
StackOverflow
YouTube
VsCode <3
DevTools - especially the responsive clicker.
& ATOM

## **Testing** 

First test after setting up I didnt connect to MONGO - square brackets instead of round on MONGO_URI

I used dummy data posts to check functionality.

Registration form wasn't rendering to the page - it was the way my route was set.

During development of my first MS3 I encountered quite a few errors, more than I can count actually. Mainly with globally installed files packages that were effecting my project workspace. I ended up having to restart the project 3 times over the last 2 weeks. The issue was down to me messing with other packages in a different workspace and not being aware of installing python packages globally and the effects it can have on the system. - I ended up wasting alot of time instead of just switching to gitpod and not practicing what I already kind of knew about Virtualenvs. And this is why my final project is now late for submission and just overrall rushed.

I swapped over to ATOM on my machine numerous times to try debug everything but still had the same issues.

Some modules not found because of venv.

The login page is tested throughout my tests as a number of my test operations require a logged in user.

All the error messages are working fine.

The registration page and logic are tested. I tested for mismatched passwords, duplicate user names, as well as successful registration.

The index page and reviews page is tested so that they load correctly. Some of my routes, reviews/ and my_account seem abit glitchy, sometimes they are speedy loading and other times they throw 404 errors.


## **Deployment**



## **Media & Resources**
//This was Inspiring
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates

//This dude - who had the style project,
I referred back here abit when I was unsure what way to do things.
Ishould reference the code but i never kept track of it, both projects are similiar.
http://book-bites.herokuapp.com/addreview

//Google images for the Jumbotron Image

//Corey Schafer for the walkthrough on forms
https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH

//Always dipping in and out of this site
https://www.fullstackpython.com/flask.html

//There was some virtualenv tutorials I used from here
https://realpython.com/

## **Acknowledgements**

Kevin and Xavier for always lending some time & advice

My Mentor

The Dude with the similiar project

Migue Grinberg - I even bought the MiniBlog course after discovering his work, after buying his book, Flask - Python for WebDevelopment

Corey Schaffer for his walkthroughs on Wtf-Forms and a better understanding of Flask

Reddit - for the humour that was needed during these 2 weeks.


## **Future Notes**

I feel this didnt go as well as I would have liked or needed in this part of the course. But like my last project it will, or another one will be going for resubmission. I messed it up myself by trying to use other packages alongside what we had learned, instead of just keeping it simple with the Database. 