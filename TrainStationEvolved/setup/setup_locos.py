def create_destinations():
    from app import app, db
    from models import Locomotive

    with app.app_context():
        existing_locomotives = {l.name for l in Locomotive.query.all()}

        new_locomotives = [
            {"name":"LNER A1 Peppercorn", "id_type":1, "model":"/models/loco/a1Peppercorn.png", "power":9, "xp_buy":15, "xp_send":5},
        ]

        for loco in new_locomotives:
            if loco["name"] not in existing_locomotives:
                new = Locomotive(**loco)
                db.session.add(new)

        db.session.commit()