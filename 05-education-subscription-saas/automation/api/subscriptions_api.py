class SubscriptionsAPI:

    def __init__(self, client):
        self.client = client

    def create(self, user_id, plan_id):
        return self.client.post(
            "/subscriptions",
            params={
                "user_id": user_id,
                "plan_id": plan_id,
            },
        )

    def get_user_subscription(self, user_id):
        return self.client.get(
            f"/subscriptions/user/{user_id}"
        )

    def cancel(self, subscription_id):
        return self.client.post(
            f"/subscriptions/{subscription_id}/cancel"
        )

    def expire(self):
        return self.client.post(
            "/subscriptions/expire"
        )