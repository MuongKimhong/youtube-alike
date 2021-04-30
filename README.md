# youtube-alike

## install dependencies for backend
```
$ pip install -r requirements.txt
```
* noted: this project requires [redis](https://redis.io/) server to run channels for real time notification.

## install dependencies for frontend
```
$ cd frontend
$ npm install
```

## migrate database and start backend development server
```
$ cd ..
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py runserver
```

## start frontend development server
```
$ cd frontend
$ npm run serve
```
