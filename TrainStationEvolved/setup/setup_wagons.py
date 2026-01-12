def create_wagons():
    from app import app, db
    from models import Wagon, CargoWagon, PassengerWagon

    with app.app_context():
        existing_wagons = {w.name for w in Wagon.query.all()}

        new_cargo_wagons = [
            {"name":"Wood Cart", "id_material": 1, "model":"/models/wagon/wood0woodcart.png", "level_unlocking": 1, "profit":0, "xp_buy":5},
        ]

        new_pass_wagons = [
            {"name":"Mail Car", "model":"/models/wagon/mail0mailcar.png", "level_unlocking": 1, "xp_buy":3, "mail": 200, "profit":0},
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