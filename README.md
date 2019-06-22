## 📦 Install

This app is dockerized, so you will only need to have docker and docker-compose installed in your machine. To execute this app you'll only need to go to the `ops` folder and then run the following commands:

```sh
cp env_example env
docker-compose up
```

You don't have to worry about the DB service nor dependencies of the project since docker will handle all of these issues.

Of course, if you are familiarized with the Django developing environment and you want the app and its services running completely in your machine then feel free to edit the settings and their corresponding configurations  to your local machine.

## 🚀 Usage

If you executed this app via docker simply navigate to `localhost:8005` and you can start using the app.

### Run The Tests
If you are a developer new to this project always run the tests before you start coding! You can do this and get a cool coverage report using these commands:
```
coverage run --source='.' manage.py test
coverage report
```
If you are going to check in some new code never forget to add tests along with the commit that test the functionality, otherwise it will be rejected.

### Author

👤 **Fermin Minetto**
- Github: [@ferminmine](https://github.com/ferminmine)
- Mail: [fermin.minetto@gmail.com](fermin.minetto@gmail.com)

### Show your support

Please ⭐️ this repository if you found this project interesting!