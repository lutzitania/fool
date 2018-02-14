cd c:\
mkdir lutzdevinterview
cd lutzdevinterview
python -m venv lutzdev
call lutzdev\scripts\activate
pip install django~=1.11.0
git init
git remote add origin https://github.com/lutzitania/fool
git fetch origin
git reset --hard origin/master
python manage.py migrate
python manage.py runserver