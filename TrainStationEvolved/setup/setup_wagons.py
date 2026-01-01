def create_materials():
    from app import app, db
    from models import Wagon, CargoWagon, PassengerWagon

    with app.app_context():
        existing_wagons = {w.name for w in Wagon.query.all()}

        new_cargo_wagons = [
            {"name":"Wood Cart", "model":"/models/wagon/wood0woodcart.png", "unlocking_level": 3, "profit":0},
        ]

        new_pass_wagons = [
            {"name":"Timber", "model":"/model/material/timber.png", "unlocking_level": 4},
        ]

        for cargo_wagons in new_cargo_wagons:
            if cargo_wagons["name"] not in existing_wagons:
                new = CargoWagon(**cargo_wagons)
                db.session.add(new)
                
        for pass_wagons in new_pass_wagons:
            if pass_wagons["name"] not in existing_wagons:
                new = PassengerWagon(**pass_wagons)
                db.session.add(new)

        db.session.commit()