def create_materials():
    from app import app, db
    from models import Material, RawMaterial, FactoryMaterial

    with app.app_context():
        existing_mats = {m.name for m in Material.query.all()}

        new_raw_mats = [
            {"name":"Wood", "icon":"/icon/material/wood.png", "unlocking_level": 1},
            {"name":"Coal", "icon":"/icon/material/coal.png", "unlocking_level": 6},
            {"name":"Iron Ore", "icon":"/icon/material/ironore.png", "unlocking_level": 6},
            {"name":"Oil Barrel", "icon":"/icon/material/oilbarrel.png", "unlocking_level": 23},
            {"name":"Uranium", "icon":"/icon/material/uranium.png", "unlocking_level": 39},
        ]

        new_fac_mats = [
            {"name":"Timber", "icon":"/icon/material/timber.png", "unlocking_level": 4},
            {"name":"Steel", "icon":"/icon/material/steel.png", "unlocking_level": 7},
            {"name":"Nails", "icon":"/icon/material/nails.png", "unlocking_level": 10},
            {"name":"Wooden Chair", "icon":"/icon/material/steel.png", "unlocking_level": 15},
            {"name":"Wooden Box", "icon":"/icon/material/steel.png", "unlocking_level": 18},
            {"name":"Wooden Table", "icon":"/icon/material/steel.png", "unlocking_level": 21},
            {"name":"Refined Diesel", "icon":"/icon/material/steel.png", "unlocking_level": 25},
            {"name":"Refined U-235", "icon":"/icon/material/steel.png", "unlocking_level": 45},
            {"name":"Gasoline", "icon":"/icon/material/steel.png", "unlocking_level": 28},
        ]

        for raw_mats in new_raw_mats:
            if raw_mats["name"] not in existing_mats:
                new = RawMaterial(**raw_mats)
                db.session.add(new)
                
        for fac_mats in new_fac_mats:
            if fac_mats["name"] not in existing_mats:
                new = FactoryMaterial(**fac_mats)
                db.session.add(new)

        db.session.commit()