from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)

def connect_db(app):
    """connects to the db"""

    db.app = app
    db.init_app(app)


class Cupcake(db.Model):

    __tablename__ = 'cupcakes'

    def __repr__(self):
        c = self

        return f'Id: {c.id}, Flavor: {c.flavor}, Size: {c.size}, Rating: {c.rating}, Image: {c.image}'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    flavor = db.Column(db.Text, nullable=False)

    size = db.Column(db.Text, nullable=False)

    rating = db.Column(db.Float, nullable=False)

    image = db.Column(db.Text, nullable=False, default="https://tinyurl.com/demo-cupcake")

    @property
    def dict_version(self):

        result = {
            "id":self.id,
            "flavor":self.flavor,
            "size":self.size,
            "rating":self.rating,
            "image":self.image
        }

        return result


    @classmethod
    def commit(cls, cupcake):

        db.session.add(cupcake)
        db.session.commit()


    @classmethod
    def get(cls, all=False, id=None):
        """
        Cupcake.get(all=False, id=None)

        Returns either all cupcakes or one specific one
        Called as:

        Cupcake.get(id=cupcake_id) 

        or

        Cupcake.get(all=True)

        """

        if all:

            cupcakes = cls.query.all()

            response = {
                "cupcakes": []
            }

            for cupcake in cupcakes:
                
                response["cupcakes"].append(cupcake.dict_version)

                return response


        else:

            cupcake = cls.query.get_or_404(id)

            response = {
                "cupcake": cupcake.dict_version
            }

    
    @classmethod
    def post(cls, flavor, size, rating, image):

        cupcake = cls(flavor=flavor, size=size, rating=rating, image=image)

        cls.commit(cupcake)

        response = {
            "Post":cupcake.dict_version
        }
        
    
    

    @classmethod
    def patch(cls, id, flavor=None, size=None, rating=None, image=None):

        cupcake = cls.query.get_or_404(id)

        original = cupcake.dict_version

        cupcake.flavor = flavor if flavor is not None else cupcake.flavor

        cupcake.size = size if size is not None else cupcake.size

        cupcake.rating = rating if rating is not None else cupcake.rating

        cupcake.image = image if image is not None else cupcake.image

        cls.commit(cupcake)

        updated = cupcake.dict_version

        response = {"Patch":[original, updated]}

        return response

        


    @classmethod
    def delete(cls, id):

        cupcake = cls.get(id=id)

        response = cupcake.dict_version

        db.session.delete(cupcake)
        db.session.commit()

        return {"Delete":response}



        





                
    



