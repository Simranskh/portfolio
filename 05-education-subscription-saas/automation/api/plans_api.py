class PlansAPI:

    def __init__(self, client):
        self.client = client

    def get_plans(self):
        return self.client.get("/plans")

    def get_plan(self, plan_id):
        return self.client.get(
            f"/plans/{plan_id}"
        )