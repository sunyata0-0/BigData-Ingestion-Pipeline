import requests


class AirflowService:

    def __init__(self, url, username, password):

        self.url = url
        self.auth = (username, password)


    def trigger_dag(self, dag_id):

        response = requests.post(
            f"{self.url}/dags/{dag_id}/dagRuns",
            auth=self.auth,
            json={}
        )

        if response.status_code in (200, 201):
            return True, "Pipeline started."

        print("=" * 50)
        print("Status:", response.status_code)
        print(response.text)
        print("=" * 50)
        return False, response.text
