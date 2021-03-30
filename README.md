# Django Ecommerce

### Requirements for running project 
- [python > 3.5.x](https://www.python.org/downloads/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)
- [git-bash](https://git-scm.com/downloads)
- [postgresql](https://www.postgresql.org/download/)
- [Gmail account with less secure apps on](https://www.google.com/intl/en-GB/gmail/about/#)

##### NOTE : If running on windows please use git-bash

### Steps for running project
```
git clone https://github.com/rishank-shah/django-ecommerce.git
cd django-ecommerce
cp .env.example .env
```
##### Fill the .env file with the correct database and email credentials then in terminal execute following commands

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
source .env
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

##### If all commands run successfully website will be running on PORT 8000 on localhost [http://localhost:8000](http://localhost:8000)
