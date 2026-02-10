def create_locos():
    from app import app, db
    from models import Locomotive

    with app.app_context():
        existing_locomotives = {l.name for l in Locomotive.query.all()}

        new_locomotives = [
            {"name":"LNER A1 Peppercorn", "id_type":1, "model":"/models/loco/a1Peppercorn.png", "power":9, "xp_buy":15, "xp_send":5, "tax_send":120, "price":1200},
            {"name":"RAe TEE II", "id_type":3, "model":"/models/loco/raetee.jpg", "power":10, "xp_buy":400, "xp_send":1000, "tax_send":350, "price":6500, "level_unlocking": 68},
            {"name":"UP Big Boy", "id_type":1, "model":"/models/loco/bigboy.png", "power":14, "xp_buy":450, "xp_send":1200, "tax_send":1400, "price":8500, "level_unlocking": 75},
        ]

        for loco in new_locomotives:
            if loco["name"] not in existing_locomotives:
                new = Locomotive(**loco)
                db.session.add(new)

        db.session.commit()