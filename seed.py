from models import connect_db, db, Cupcake

def seed_db(app):
    connect_db(app)
    db.drop_all()
    db.create_all()
    c1 = Cupcake(
        flavor="cherry",
        size="large",
        rating=5,
    )
    c2 = Cupcake(
        flavor="chocolate",
        size="small",
        rating=9,
        image="https://www.bakedbyrachel.com/wp-content/uploads/2018/01/chocolatecupcakesccfrosting1_bakedbyrachel.jpg"
    )
    db.session.add_all([c1, c2])