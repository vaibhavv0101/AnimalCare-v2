from app.extensions import db
from app.models.animal import Animal


def create_animal(data):

    animal = Animal(**data)

    db.session.add(animal)

    db.session.commit()

    return animal

from app.models.animal import Animal


def get_all_animals():
    return Animal.query.order_by(Animal.created_at.desc()).all()

def get_animal_by_id(animal_id):
    return Animal.query.get(animal_id)

def update_animal(animal_id, data):

    animal = Animal.query.get(animal_id)

    if animal is None:
        return None

    for key, value in data.items():
        setattr(animal, key, value)

    db.session.commit()

    return animal

def update_animal(animal_id, data):

    animal = Animal.query.get(animal_id)

    if animal is None:
        return None

    for key, value in data.items():
        setattr(animal, key, value)

    db.session.commit()

    return animal

def delete_animal(animal_id):

    animal = Animal.query.get(animal_id)

    if animal is None:
        return False

    db.session.delete(animal)
    db.session.commit()

    return True