# Django Ecommerce

<br/>

### Table of Contents
- [Requirements](#requirements-for-running-project)
  * [Software Installation](#requirements-for-running-project)
  * [Accounts Required](#requirements-for-running-project)
- [Steps for running project](#steps-for-running-project)
  * [One Time Setup](#)
    * [Clone Project](#clone-repository)
    * [Environment Setup](#environment-setup)
    * [Create DB in postgresql](#create-db)
    * [Fill .env file](#fill-env-file)
    * [Installation of Dependencies](#installation-of-dependencies)
    * [Migrations and SuperUser](#migrations-and-superuser)
  * [Running Server](#running-django-server)
    * [Django](#running-django-server)
    * [Celery](#running-celery)
    * [Elasticsearch](#elasticsearch)
- [Load Initial Data (optional)](#initial-data)

<br/>

### Requirements for running project 
- Software Installation:
  * [python >3.5.x](https://www.python.org/downloads/)
  * [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)
  * [git-bash](https://git-scm.com/downloads)
  * [Redis](https://redis.io/download)
  * [postgresql](https://www.postgresql.org/download/)
  * [ElasticSearch](https://www.elastic.co/downloads/elasticsearch)
- Accounts Required:
  * [Gmail account with less secure apps on](https://www.google.com/intl/en-GB/gmail/about/#)
  * [Cloudinary Account](https://cloudinary.com/)

<br/>

###### Before running the project make sure that postgresql, elasticsearch and redis servers are running.
### Steps for running project:

##### Clone Repository:
```bash
git clone https://github.com/rishank-shah/django-ecommerce.git
cd django-ecommerce
cp .env.example .env
```

##### Environment Setup:

```bash
pip install virtualenv
virtualenv venv
```

##### Create DB
###### Create a DB in postgresql and enter the same DB name in the .env file

##### Fill .env file:
###### Fill the .env file with the correct database, cloudinary, email credentials, elasticsearch and redis url.

##### Installation of Dependencies:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

##### Migrations and SuperUser
```bash
source venv/bin/activate
source .env
python manage.py migrate
python manage.py createsuperuser
```

##### Running Django Server:

```bash
source venv/bin/activate
source .env
python manage.py runserver
```

##### Running Celery:
###### For running celery open another terminal navigate to ```django-ecommerce``` folder and execute the following commands
```bash
source venv/bin/activate
source .env
celery -A ecommerce_project worker -l info
```

##### ElasticSearch:
###### If you are facing an error while saving products in admin, navigate to ```django-ecommerce``` folder and execute the following commands
```bash
source venv/bin/activate
source .env
python manage.py search_index --rebuild
```
###### Press ```y``` and enter


### Initial Data
###### You can load some initial data from fixture ```load_product_data.json```
###### Please Note Images will not be displayed as your cloudinary account will be different
```bash
source venv/bin/activate
source .env
python manage.py loaddata load_product_data.json
```

<br/>

#### If all commands run successfully website will be running on PORT 8000 on localhost [http://localhost:8000](http://localhost:8000)
