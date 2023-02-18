# iglike_framework

environment: python3.8↑

---

##### Git Flow
1. Clone first
```shell
$ git clone https://github.com/ycs18153/iglike_framework.git
```

2. Create 'develop' branch in local,
And make the consistency of remote and local `develop` content.

```shell
$ git checkout -b develop
$ git pull origin develop
```
3. Start implement the new feature
```shell
$ git checkout -b feature/the-description-of-the-new-function develop
```

4. Make a commit
```shell
$ git commit -m 'feat: put the topic of your changes down here'
```
*p.s. you can still make more description from the third line which is after pressing shift+enter twice*
[For more guides plz click here](https://wadehuanglearning.blogspot.com/2019/05/commit-commit-commit-why-what-commit.html)

5. Push your commit
```shell
$ git branch --set-upstream-to origin/feature/the-description-of-the-new-function
$ git push
```
*p.s. for the first time push a new branch you need to set upstream before you push*

---

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
