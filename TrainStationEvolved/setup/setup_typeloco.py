def create_typeloco():
    from app import app, db
    from models import TypeLoco

    with app.app_context():
        existing_types = {t.name for t in TypeLoco.query.all()}

        new_types = [
            {"name":"Steam", "profit":100, "icon":"/icon/typeloco/steam.png"},
            {"name":"Diesel", "profit":145, "icon":"/icon/typeloco/diesel.png"},
            {"name":"Electric", "profit":100, "icon":"/icon/typeloco/electric.png"},
            {"name":"Maglev", "profit":100, "icon":"/icon/typeloco/maglev.png"},
            {"name":"Hyperloop", "profit":100, "icon":"/icon/typeloco/hyperloop.png"},
        ]

        for typeloco in new_types:
            if typeloco["name"] not in existing_types:
                new = TypeLoco(**typeloco)
                db.session.add(new)

        db.session.commit()