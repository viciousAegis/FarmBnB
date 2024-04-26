from subscription.emailManager import EmailManager

class SubscriptionManager():
    def __init__(self, subscription_collection):
        self.emailManager = EmailManager()
        self.subscription_collection = subscription_collection
        # try to get the subscriptions from the database
        self.subscriptions = {}
        subscription = self.subscription_collection.find_one()
        print(subscription)
        if subscription is not None:
            self.subscriptions = subscription.get("subscriptions", {})
        else:
            self.subscription_collection.insert_one({"subscriptions": {}})

    def getSubscriptionsFromMongo(self):
        subscription = self.subscription_collection.find_one()
        print(subscription)

    def addSubscription(self, farm_id, user_email):
        print(f"Adding subscription for farm {farm_id} and user {user_email}")
        
        if farm_id not in self.subscriptions:
            self.subscriptions[farm_id] = []
        else:
            # check if the user is already subscribed
            if user_email in self.subscriptions[farm_id]:
                raise Exception("User is already subscribed")

        self.subscriptions[farm_id].append(user_email)
        print(self.subscriptions[farm_id])

        # update just the subscriptions key in the database
        self.subscription_collection.update_one({}, {"$set": {"subscriptions": self.subscriptions}}, upsert=True)

        self.getSubscriptionsFromMongo()

    def removeSubscription(self, farm_id, user_email):
        if farm_id in self.subscriptions:
            self.subscriptions[farm_id].remove(user_email)
        
        # update the database
        self.subscription_collection.update_one({}, {"$set": {"subscriptions": self.subscriptions}}, upsert=True)

        self.getSubscriptionsFromMongo()

    def getSubscriptionsByUser(self, user_email):
        subscriptions = []
        for farm_id, users in self.subscriptions.items():
            if user_email in users:
                subscriptions.append(farm_id)
        return subscriptions

    def getSubscriptionsByFarm(self, farm_id):
        print(farm_id)
        print(self.subscriptions.get(farm_id, []))
        return self.subscriptions.get(farm_id, [])
    
    def getSubscriptions(self):
        return self.subscriptions
    
    def notifySubscribers(self, farm_id, message):
        user_emails = self.getSubscriptionsByFarm(farm_id)

        for user_email in user_emails:
            self.emailManager.send_email(user_email, message)
            
            