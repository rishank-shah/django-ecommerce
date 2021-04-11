# Django Ecommerce

### Requirements for running project 
- [python > 3.5.x](https://www.python.org/downloads/)
- [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)
- [git-bash](https://git-scm.com/downloads)
- [postgresql](https://www.postgresql.org/download/)
- [Gmail account with less secure apps on](https://www.google.com/intl/en-GB/gmail/about/#)
- [Cloudinary Account](https://cloudinary.com/)
- [ElasticSearch](https://www.elastic.co/downloads/elasticsearch)
- [Redis](https://redis.io/download)

##### NOTE : If running on windows please use git-bash

### Steps for running project
```
git clone https://github.com/rishank-shah/django-ecommerce.git
cd django-ecommerce
cp .env.example .env
```
##### Fill the .env file with the correct database, cloudinary, email credentials, elasticsearch and redis url then in terminal execute following commands
##### Now Start ElasticSearch Server and execute the following commands

```
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
source .env
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

#### Now for running celery open another terminal navigate to ```django-ecommerce``` folder
```
source venv/bin/activate
source .env
celery -A ecommerce_project worker -l info
```

##### If all commands run successfully website will be running on PORT 8000 on localhost [http://localhost:8000](http://localhost:8000)
