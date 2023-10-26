import requests
from faker import Faker
from faker.providers import internet
import json
import random

fake = Faker()
fake.add_provider(internet)


class Bot(object):
    def __init__(self, number_of_users, max_posts_per_user, max_likes_per_user, url):
        self.number_of_users = number_of_users
        self.max_posts_per_user = max_posts_per_user
        self.max_likes_per_user = max_likes_per_user
        self.url = url

    def create_user(self):
        user_data = {
            "email": fake.email(),
            "password": fake.password(
                length=8,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ),
        }
        response = requests.post(url=f"{self.url}api/user/register/", data=user_data)
        if response.status_code == 201:
            login_response = requests.post(
                url=f"{self.url}api/user/token/",
                data={
                    "email": user_data.get("email"),
                    "password": user_data.get("password"),
                },
            )
            auth_data = json.loads(login_response.content)
            return auth_data
        return None

    def jwt_verify(self, auth_data):
        jwt_access = auth_data.get("access")
        jwt_refresh = auth_data.get("refresh")
        jwt_verification = requests.post(
            url=self.url + "api/user/token/verify/",
            headers={"Authorization": f"Bearer {jwt_access}"},
            data={"token": jwt_access},
        )
        if jwt_verification.status_code != 200:
            response = requests.post(
                url=self.url + "api/user/token/refresh/",
                headers={"Authorization": f"Bearer {jwt_refresh}"},
            )
            auth_data = json.loads(response.content)
            jwt_access = auth_data.get("access")
            jwt_refresh = auth_data.get("refresh")
        return jwt_access, jwt_refresh

    def create_posts(self, auth_data):
        post_counter = 0
        for _ in range(random.randint(1, int(self.max_posts_per_user))):
            jwt_access, jwt_refresh = self.jwt_verify(auth_data=auth_data)
            user_response = requests.get(
                url=self.url + "api/user/me/",
                headers={"Authorization": f"Bearer {jwt_access}"},
            )
            user_data = json.loads(user_response.content)
            author = user_data.get("id")
            post_data = {
                "author": author,
                "title": fake.sentence(
                    nb_words=6, variable_nb_words=True, ext_word_list=None
                ),
                "description": fake.text(max_nb_chars=250, ext_word_list=None),
            }

            response = requests.post(
                url=self.url + "api/blog/posts/",
                headers={"Authorization": f"Bearer {jwt_access}"},
                data=post_data,
            )
            if response.status_code == 201:
                post_counter += 1
        return post_counter

    def create_likes(self, auth_data):
        jwt_access, jwt_refresh = self.jwt_verify(auth_data=auth_data)
        user_response = requests.get(
            url=self.url + "api/user/me/",
            headers={"Authorization": f"Bearer {jwt_access}"},
        )
        user_data = json.loads(user_response.content)
        response = requests.get(
            url=self.url + "api/blog/posts/",
            headers={"Authorization": f"Bearer {jwt_access}"},
        )
        posts = json.loads(response.content)
        actions = 0
        while actions < random.randint(1, int(self.max_likes_per_user)):
            user = user_data.get("id")
            posts_results = posts["results"]
            post = posts_results[random.randint(0, len(posts_results) - 1)].get("id")
            post_data = {
                "user": user,
                "post": post,
            }

            response = requests.post(
                url=self.url + f"api/blog/posts/<int:pk>/add_like/",
                headers={"Authorization": f"Bearer {jwt_access}"},
                data=post_data,
            )

            if response.status_code == 401:
                jwt_access, jwt_refresh = self.jwt_verify(auth_data=auth_data)
                requests.post(
                    url=self.url + f"api/blog/likes",
                    headers={"Authorization": f"Bearer {jwt_access}"},
                )
            actions += 1
        return actions
