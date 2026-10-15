class Horse:
    def __init__(self, horse_id, name, breed, age, health_status, activity):
        self.horse_id = str(horse_id).strip()
        self.name = name.strip()
        self.breed = breed.strip()
        self.age = int(age)
        self.health_status = health_status
        self.activity = activity

    def update(self, name, breed, age, health_status, activity):
        self.name = name.strip()
        self.breed = breed.strip()
        self.age = int(age)
        self.health_status = health_status
        self.activity = activity

    def to_dict(self):
        return {
            "horse_id": self.horse_id,
            "name": self.name,
            "breed": self.breed,
            "age": self.age,
            "health_status": self.health_status,
            "activity": self.activity,
        }
