from emailManager import EmailManager

class SubscriptionManager():
    def __init__(self):
        self.subscriptions = {}
        self.emailManager = EmailManager()
    
    def addSubscription(self, farm_id, user_id):
        print(f"Adding subscription for farm {farm_id} and user {user_id}")
        if farm_id not in self.subscriptions:
            self.subscriptions[farm_id] = []
        self.subscriptions[farm_id].append(user_id)
        print(self.subscriptions[farm_id])

    def removeSubscription(self, farm_id, user_id):
        if farm_id in self.subscriptions:
            self.subscriptions[farm_id].remove(user_id)

    def getSubscriptionsByUser(self, user_id):
        subscriptions = []
        for farm_id, users in self.subscriptions.items():
            if user_id in users:
                subscriptions.append(farm_id)
        return subscriptions

    def getSubscriptionsByFarm(self, farm_id):
        print(farm_id)
        print(self.subscriptions.get(farm_id, []))
        return self.subscriptions.get(farm_id, [])
    
    def getSubscriptions(self):
        return self.subscriptions
    
    def notifySubscribers(self, user_emails, message):
        for user_email in user_emails:
            self.emailManager.send_email(user_email, message)
            
            
