# DjangoAPI
Trying out Django framework and its REST API

The repo consists of a simple POST/GET/DELETE request functionality using Python3, Django + Django REST framework, PostgreSQL DBMS. 
Fixtures are used to load test data while migrating. 
Some unit tests are added too.


-------------------------------------------------------------
Current issue:
Trying to run unit tests while using PSQL raises a duplicate key exception - not quite sure why it tries to use the same ID twice. Same tests work like a charm on sqlite DBMS instead
Current workaround - using sqlite for running tests instead. 
Still looking for a way to solve this issue.

Exception:
"""
django.db.utils.IntegrityError: duplicate key value violates unique constraint "meeting_room_pkey"
DETAIL:  Key (id)=(1) already exists.
"""

Related resources:
https://code.djangoproject.com/ticket/17415
https://code.djangoproject.com/ticket/16353#no1
https://devdreamz.com/question/630030-django-db-utils-integrityerror-duplicate-key-value-violates-unique-constraint
https://searene.github.io/2016/01/10/django-db-utils-IntegrityError-duplicate-key-value-violates-unique-constraint/
