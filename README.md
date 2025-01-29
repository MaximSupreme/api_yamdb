# YaMDb art review website



## DESCRIPTION:

- _This is a website for user reviews of various works of art. All users can rate different types of art such as movies, books or music, comment on other people's reviews and express their opinions._
- _This project also uses ***JWT authentication*** for providing better experience and secure interaction with API._



## BACKEND STACK:

- _Languages: **Python**._
- _Frameworks: **Django**, **Django REST framework**._
- _Databases: **SQLite**._



## LOCAL DEPLOYATION:

**To deploy this project on your computer:**
- _Clone this repository to your ***working directory***._
- _Create a virtual environment:_
```bash
python(3) -m (venv name) venv
```
- _Install requirements through pip:_
```bash
pip install -r requirements.txt
```
- _Apply migrations:_
```bash
python(3) manage.py migrate
```
- _Run server:_
```bash
python(3) manage.py runserver
```



## API request examples:

- _To **registrate** on a website - `POST /auth/signup/`._
- _To **fetch** a JWT Token - `POST /auth/token/`._
- _To **fetch** list of all categories - `GET /categories/`._
- _To **post** a new category - `POST /categories/`._
- _To **delete** a category - `DELETE /categories/` with body `{slug}`._
- _To **fetch** list of all genres - `GET /genres/`._
- _To **post** a new genre - `POST /genres/`._
- _To **delete** a genre - `DELETE /genres/` with body `{slug}`._
- _To **fetch** list of all titles - `GET /titles/`._
- _To **post** a new title - `POST /titles/`._
- _To **fetch** information about certain title - `GET /titles/` with body `{title_id}`._
- _To **patch** a certain information about title - `PATCH /titles/` with body `{title_id}`._
- _To **delete** a title - `DELETE /titles/` with body `{title_id}`._
- _To **fetch** list of all reviews - `GET /titles/` with body `{title_id}/reviews/`._
- _To **post** a new review - `POST /titles/` with body `{title_id}/reviews/`._
- _To **fetch** information about certain review - `GET /titles/` with body `{title_id}/reviews/{review_id}/`._
- _To **patch** a certain information about review - `PATCH /titles/` with body `{title_id}/reviews/{review_id}/`._
- _To **delete** a review - `DELETE /titles/` with body `{title_id}/reviews/{review_id}/`._
- _To **fetch** list of all comments - `GET /titles/` with body `{title_id}/reviews/{review_id}/comments/`._
- _To **post** a new comment to certain review - `POST /titles/` with body `{title_id}/reviews/{review_id}/comments/`._
- _To **fetch** information about certain comment - `GET /titles/` with body `{title_id}/reviews/{review_id}/comments/{comment_id}/`._
- _To **patch** a certain information about comment - `PATCH /titles/` with body `{title_id}/reviews/{review_id}/comments/`._
- _To **delete** a comment - `DELETE /titles/` with body `{title_id}/reviews/{review_id}/comments/`._





## CREATORS:

***Maksim Chernikov a.k.a. MaximSupreme***
***ChloeShark***
***Nikolay a.k.a. RemDef***
