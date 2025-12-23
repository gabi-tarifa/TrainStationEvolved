def create_destinations():
    from app import app, db
    from models import Destination

    with app.app_context():
        existing_destinations = {c.name for c in Destination.query.all()}

        new_destinations = [
            {"name":"Farm", "timeTravelMinutes":5, "image":"/img/destinations/farm.png"},
            {"name":"Small Village", "timeTravelMinutes":10, "image":"/img/destinations/smallVillage.png"},
            {"name":"Rural Village", "timeTravelMinutes":15, "image":"/img/destinations/ruralVillage.png"},
            {"name":"Inner City", "timeTravelMinutes":20, "image":"/img/destinations/innerCity.png"},
            {"name":"Agricultural Complex", "timeTravelMinutes":30, "image":"/img/destinations/agriculturalComplex.png"},
            {"name":"Farmland State", "timeTravelMinutes":45, "image":"/img/destinations/farmlandState.png"},
            {"name":"Factory City", "timeTravelMinutes":60, "image":"/img/destinations/factoryCity.png"},
            {"name":"Metropolis Center", "timeTravelMinutes":2*60, "image":"/img/destinations/metropolisCenter.png"},
            {"name":"Market Town", "timeTravelMinutes":3*60, "image":"/img/destinations/marketTown.png"},
            {"name":"Country Town", "timeTravelMinutes":4*60, "image":"/img/destinations/countryTown.png"},
            {"name":"Periferic Station", "timeTravelMinutes":5*60, "image":"/img/destinations/perifericStation.png"},
            {"name":"Capital Trading Hall", "timeTravelMinutes":6*60, "image":"/img/destinations/capitalTradingHall.png"},
            {"name":"Logistics Hub", "timeTravelMinutes":8*60, "image":"/img/destinations/logisticsHub.png"},
            {"name":"Factory Complex", "timeTravelMinutes":10*60, "image":"/img/destinations/factoryComplex.png"},
            {"name":"Industrial District", "timeTravelMinutes":12*60, "image":"/img/destinations/industrialDistrict.png"},
            {"name":"Industrial City", "timeTravelMinutes":14*60, "image":"/img/destinations/industrialCity.png"},
            {"name":"Urban Corridor", "timeTravelMinutes":16*60, "image":"/img/destinations/urbanCorridor.png"},
            {"name":"Exterior Village", "timeTravelMinutes":20*60, "image":"/img/destinations/exteriorVillage.png"},
            {"name":"Metropolitan Outskirts", "timeTravelMinutes":24*60, "image":"/img/destinations/metropolitanOutskirts.png"},
            {"name":"Modern City Complex", "timeTravelMinutes":2*24*60, "image":"/img/destinations/modernCityComplex.png"},
            {"name":"Megacity", "timeTravelMinutes":3*24*60, "image":"/img/destinations/megacity.png"},
            {"name":"Megalopolis", "timeTravelMinutes":4*24*60, "image":"/img/destinations/megalopolis.png"},
            {"name":"Global Metropolis", "timeTravelMinutes":5*24*60, "image":"/img/destinations/globalMetropolis.png"},
            {"name":"Utopia", "timeTravelMinutes":6*24*60, "image":"/img/destinations/utopia.png"},
            {"name":"Farlands", "timeTravelMinutes":7*24*60, "image":"/img/destinations/farlands.png"},
        ]

        for destination in new_destinations:
            if destination["name"] not in existing_destinations:
                new = Destination(**destination)
                db.session.add(new)

        db.session.commit()