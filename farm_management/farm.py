from flask import jsonify
class Farm:
    def __init__(self, farm_id, name, description, location, area, price, owner, start_date, end_date, contact, farm_type, rating):
        self.farm_id = farm_id
        self.name = name
        self.description = description
        self.location = location
        self.area = area
        self.price = price
        self.owner = owner
        self.start_date = start_date
        self.end_date = end_date 
        self.contact = contact
        self.farm_type = farm_type
        self.rating = rating

    # def make_json(self):
    #     return {
    #         "farm_id": self.farm_id,
    #         "name": self.name,
    #         "description": self.description,
    #         "location": self.location,
    #         "area": self.area,
    #         "price": self.price,
    #         "owner": self.owner,
    #         "occupied_dates": self.occupied_dates,
    #         "contact": self.contact,
    #         "farm_type": self.farm_type,
    #         "rating": self.rating
    #     }