# iglike_framework

environment: python3.8↑


##### Backend setup
```
$ cd backend
$ pip install -r requirements.txt

Lunach Backend
$ python main.py (or python3.9 main.py)
```

##### frontend setup
```
$ cd frontend
$ npm install

Lunach frontend
Option 1: test in computer
$ HTTPS=true npm start  //Obtain HTTPS url

Option 2: test in line app on mobile
$ npm start //Obtain HTTP url

in other terminal
$ ngrok http 3000 --host-header="localhost:3000"
then copy the url and paste to Endpoint URL & Callback URL of liff on LINE Developer
```