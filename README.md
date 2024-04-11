**This webapp was developed in Django.**

**1.Clone the project**
_git clone https://github.com/Nurtugang/imio_webapp.git
cd imio_webapp_

**2.Install dependencies**
List of requirements there: _req.txt_
_pip install -r req.txt_

**3.Configure the database**
Also this webapp works with remote database(**MYSQL SERVER**), that's why you need to **configure database first**.
You can do it there: _imioproject/db_conf.py_

**4.Migrate**
_python manage.py migrate_

**5.Admin-panel**
To have an access to Django admin-panel, after migration try to use this account: login:**nur**, password:**nur**
If it doesn't work, just create new superuser:
_python manage.py createsuperuser_

**6.Run webapp**
_python manage.py runserver_
