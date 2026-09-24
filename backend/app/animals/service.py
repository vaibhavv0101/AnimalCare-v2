from app.extensions import db
from app.models.animal import Animal


# ============================================================
# CREATE ANIMAL
# ============================================================

def create_animal(data):
    """
    Create a new animal record.
    """

    animal = Animal(**data)

    db.session.add(animal)
    db.session.commit()

    return animal


# ============================================================
# GET ALL ANIMALS
# ============================================================

def get_all_animals():
    """
    Return all animals ordered by newest first.
    """

    return Animal.query.order_by(
        Animal.created_at.desc()
    ).all()


# ============================================================
# GET ANIMAL BY ID
# ============================================================

def get_animal_by_id(animal_id):
    """
    Return a single animal by ID.
    """

    return db.session.get(Animal, animal_id)


# ============================================================
# UPDATE ANIMAL
# ============================================================

def update_animal(animal_id, data):
    """
    Update an existing animal.
    """

    animal = db.session.get(Animal, animal_id)

    if animal is None:
        return None

    for key, value in data.items():

        # Only update valid Animal attributes
        if hasattr(animal, key):
            setattr(animal, key, value)

    db.session.commit()

    return animal


# ============================================================
# DELETE ANIMAL
# ============================================================

def delete_animal(animal_id):
    """
    Delete an animal by ID.
    """

    animal = db.session.get(Animal, animal_id)

    if animal is None:
        return False

    db.session.delete(animal)
    db.session.commit()

    return True