# Quiz Application Capstone Project

Quiz Application project using Django and Bootstrap.

This project is created in order to fulfill the project requirements to pass the CS50 Web Programming with Python & JavaScript course offered by HarvardX via EdX. The main function of this project is to enable any users to freely create a quiz and take any quizzes made by another users (as long as the topic has already been created by admins).
The features included in this project, other than its main functions which is freely creating and taking quizzes, are:
- Following. Enable users to follow any other users. There is a page that make users can see quizzes only made by their following's (similar to how twitter works).
- Topic differentiation. Enable users to find, create, and take a particular quiz based on the available topic they want.

## Distinctiveness and Complexity 
#### There is not a chat feature in this project. Therefore I am certain it can't be categorized as social network project.
#### This project is also not a commercial site, because the main functions of this project requires a completely different set of logics in the views and models compared to the commercial project.
*** Though admittedly, there are some simple logics/functions here that derived from those projects such as handling image and the following system. But I take it as a learning resources/references rather than straight up copy. ***

#### This project utilizes django (plain and obvious) and javascript to manipulate some things such as when a user wanted to create a new quiz, they will be asked to input how many questions they want. There is also timer feature implemented by javascript.

#### This project utilizes bootstrap to handle responsiveness as shown in the project demonstration video.

#### Folders and Files contained in this projects are:
  - capstone => containing all the default file settings of the project (__pycache__ folder, __init__, asgi.py, settings.py, urls.py, wsgi.py)
  - media => containing all the media files. Divided into 2 categories. Banner folder for a banner and profile folder for users' profile picture.
            *Note: example folder is just reference. Not really important. The picture inside contains an output of a logic that I created but didn't use.
  - quizApp => containing all the necessary parts of the projects (__pycache__, migrations, static, templates, .gitignore, db.sqlite3. manage.py, ReadME)
    - migrations => there is really nothing to say.
    - static => contains the static folders (bootstrap offline folder and quizApp containing all the CS and JavaScript files)
    - templates => contains the template HTML for the projects.
      - boostrap-5.0 => offline bootstraping
      - quizApp => CSS and JavaScript files
         - answer.js => javascript for answer.html
         - make_quiz.js => javascript for make_quiz.html. Generating questions form
         - styles.css => all the styling needed for templates. Diffentiated with class/id naming and commented template.html name
         - test.js => javascript for test.html.
    - init__.py => python folder initialization
    - admin.py => displaying admin interface
    - apps.py => app configuration
    - models.py => models for the projects.
    - tests.py => not used
    - urls.py => url configuration
    - utils.py => contains function for grading
    - views.py => controlling the template/view

How to run the application:
1. Download the all the files.
2. Go into the directory where manage.py exists.
3. Go into the command line of that directory.
4. Run 'python manage.py runserver'
5. Go to 'http://127.0.0.1:8000'

Additional information: 
When the quiz is underway, DO NOT REFRESH THE PAGE. The logic I implemented for Participant models is to create a new record for Participant (hence, new id) every time the test.html is accessed. So it will multiple the Participant data for how much refreshing the page is done. Other than filling the database with unnecessary data, it will also cause the average score to skew so bad because the default score for a new Participant record is 0 until the test is submitted and the grading started (in the test function in views.py).
The code is, unfortunately, not really clean because of so many self-notes and failure references that I made and just uncomment for the future. So I would like to apologize on that part.
