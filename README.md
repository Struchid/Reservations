# DjangoAPI
Trying out Django framework and its REST API

The repo consists of a simple POST/GET/DELETE request functionality using Python3, Django + Django REST framework, PostgreSQL DBMS.<br>
Fixtures are used to load test data while migrating.<br>
Flake8 used to ensure PEP8 guidelines are followed correctly.<br>
Some unit tests were added to test the API requests as well.<br>


-------------------------------------------------------------
Current issue:<br>
Trying to run unit tests while using PostgreSQL raises a duplicate key exception - not quite sure why it tries to use the same ID twice. Same tests work like a charm on sqlite DBMS instead
Current workaround - using sqlite for running tests instead. 
Still looking for a way to solve this issue.

Exception:<br>
django.db.utils.IntegrityError: duplicate key value violates unique constraint "meeting_room_pkey"<br>
DETAIL:  Key (id)=(1) already exists.

Related resources:<br>
https://code.djangoproject.com/ticket/17415<br>
https://code.djangoproject.com/ticket/16353#no1<br>
https://devdreamz.com/question/630030-django-db-utils-integrityerror-duplicate-key-value-violates-unique-constraint<br>
https://searene.github.io/2016/01/10/django-db-utils-IntegrityError-duplicate-key-value-violates-unique-constraint/<br>
