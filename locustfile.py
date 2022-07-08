from random import randint, choice
from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def home(self):
        self.client.get("/")

    @task
    def server_error(self):
        self.client.get("/server_error")

    @task
    def error_reponse(self):
        errors_codes = [401, 403, 404, 308, 500, 502, 503]
        error_code = choice(errors_codes)
        self.client.get(f"/error_reponse/{error_code}")

    @task
    def metrics_increment(self):
        increment_value = randint(1, 5)
        self.client.get(f"/sdmetrics_incr/{increment_value}")

    @task
    def metrics_decrement(self):
        increment_value = randint(1, 5)
        self.client.get(f"/sdmetrics_decr/{increment_value}")

    @task
    def metrics_gauge(self):
        new_value = randint(10, 200)
        self.client.get(f"/sdmetrics_gauge/{new_value}")

    @task
    def metrics_set(self):
        new_value = randint(10, 200)
        self.client.get(f"/sdmetrics_set/{new_value}")
