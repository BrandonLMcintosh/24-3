from unittest import TestCase
from app import app
from seed import seed_db
from models import db, Cupcake

url = '/api/cupcakes'

test_good_cupcake_json = {
    "flavor":"test_flavor",
    "size":"test_size",
    "rating":10
}

test_bad_cupcake_json = {
    "flavor":"test_flavor",
    "size":"test_size",
    "rating":"random string"
}

db.drop_all()
db.create_all()

class Test_app(TestCase):

    maxDiff = None

    def setUp(self):

        c1 = Cupcake(flavor="flavor1", size="size1", rating=1)
        c2 = Cupcake(flavor="flavor2", size="size2", rating=2)
        c3 = Cupcake(flavor="flavor3", size="size3", rating=3)

        db.session.add(c1)
        db.session.add(c2)
        db.session.add(c3)


        self.cup1 = Cupcake.query.get(1)
        self.cup2 = Cupcake.query.get(2)
        self.cup3 = Cupcake.query.get(3)

        self.cup1 = self.cup1.dict_version
        self.cup2 = self.cup2.dict_version
        self.cup3 = self.cup3.dict_version

        db.session.commit()
    

    def tearDown(self):

        db.drop_all()
        db.create_all()

        self.cup1 = None
        self.cup2 = None
        self.cup3 = None

        db.session.commit()


    def test_get_all(self):

        with app.test_client() as client:

            response = client.get(url)

            self.assertEqual(response.status_code, 200)

            data = response.json

            self.assertEqual(data, {
                'cupcakes': [
                    self.cup1,
                    self.cup2,
                    self.cup3
                ]
            })


    def test_get_all_after_add(self):

        with app.test_client() as client:

            client.post(url, json=test_good_cupcake_json)

            response = client.get(url)

            self.assertEqual(response.status_code, 200)

            data = response.json

            self.assertEqual(data, {
                'cupcakes': [
                    self.cup1,
                    self.cup2,
                    self.cup3,
                    {
                        'id':4,
                        'flavor':'test_flavor',
                        'size':'test_size',
                        'rating':10,
                        'image':self.cup3['image']
                    }
                ]
            })


    def test_get_all_after_delete(self):

        with app.test_client() as client:

            client.delete(f'{url}/1')

            response = client.get(url)

            self.assertEqual(response.status_code, 200)

            data = response.json

            self.assertEqual(data, {
                'cupcakes': [
                    self.cup2,
                    self.cup3
                ]
            })

        
    def test_get_one_exists(self):

        with app.test_client() as client:

            response = client.get(f'{url}/1')

            self.assertEqual(response.status_code, 200)

            data = response.json

            self.assertEqual(data, {
                'cupcake': self.cup1
            })


    def test_get_one_not_exists(self):

        with app.test_client() as client:

            response = client.get(f'{url}/1000')

            self.assertEqual(response.status_code, 404)


    def test_post_good_values(self):

        with app.test_client() as client:

            response = client.post(url, json=test_good_cupcake_json)

            self.assertEqual(response.status_code, 200)

            data = response.json

            del data['post']['id']
            del data['post']['image']

            self.assertEqual(data, {
                'post': {
                    'flavor':'test_flavor',
                    'rating':10,
                    'size':'test_size'
                }
            })


    def test_post_bad_values(self):

        with app.test_client() as client:

            response = client.post(url, json=test_bad_cupcake_json)

            self.assertEqual(response.status_code, 200)

            data = response.json

            del data['post']['image']
            del data['post']['id']

            self.assertEqual(data, {
                'post':{
                    'flavor':'test_flavor',
                    'rating':1,
                    'size':'test_size'
                }
            })


    def test_patch_good_values(self):

        with app.test_client() as client:

            response = client.patch(f'{url}/1', json=test_good_cupcake_json)

            self.assertEqual(response.status_code, 200)

            data = response.json

            del data['patch'][0]['id']
            del data['patch'][0]['image']
            del data['patch'][1]['id']
            del data['patch'][1]['image']

            self.assertEqual(data, {
                'patch':[{
                    'flavor':'flavor1',
                    'rating':1,
                    'size':'size1'
                },
                {
                    'flavor':'test_flavor',
                    'rating':10,
                    'size':'test_size'
                }
                ]
            })


    def test_patch_bad_values(self):

        with app.test_client() as client:

            response = client.patch(f'{url}/1', json=test_bad_cupcake_json)

            self.assertEqual(response.status_code, 200)

            data = response.json

            del data['patch'][0]['id']
            del data['patch'][0]['image']
            del data['patch'][1]['id']
            del data['patch'][1]['image']

            self.assertEqual(data, {
                'patch':[{
                    'flavor':'flavor1',
                    'rating':1,
                    'size':'size1'
                },
                {
                    'flavor':'test_flavor',
                    'rating':1,
                    'size':'test_size'
                }
                ]
            })


    def test_patch_not_exists(self):

        with app.test_client() as client:

            response = client.get(f'{url}/1000', json=test_good_cupcake_json)

            self.assertEqual(response.status_code, 404)


    def test_delete_exists(self):

        with app.test_client() as client:

            response = client.delete(f'{url}/1')

            self.assertEqual(response.status_code, 200)

            data = response.json

            self.assertEqual(data, {
                'delete': self.cup1
            })


    def test_delete_not_exists(self):

        with app.test_client() as client:

            response = client.delete(f'{url}/1000')

            self.assertEqual(response.status_code, 404)