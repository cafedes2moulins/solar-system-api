from app import db



class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    position = db.Column(db.Integer)

    def to_dict(self):
        planet_dict={
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "position": self.position
        }
        return planet_dict

    
    @classmethod
    def from_dict(cls, planet_dict):
        if "name" in planet_dict and "description" in planet_dict and "position" in planet_dict:
            new_planet = cls(name=planet_dict["name"],
                description= planet_dict["description"],
                position=planet_dict["position"])

            return new_planet