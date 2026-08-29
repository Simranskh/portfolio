class PaymentsAPI:

    def __init__(self, client):
        self.client = client

    def create(
        self,
        user_id,
        subscription_id,
        payment_method="card",
    ):
        return self.client.post(
            "/payments",
            params={
                "user_id": user_id,
                "subscription_id": subscription_id,
                "payment_method": payment_method,
            },
        )

    def history(self, user_id):
        return self.client.get(
            f"/payments/user/{user_id}"
        )