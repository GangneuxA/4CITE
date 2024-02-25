import unittest
from app.routes import app ,db
from app.models import chambres, user , hotel

class TestChambresGet(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app_context = app.app_context()
        self.app_context.push()
        self.client = app.test_client()

    def test_get_chambres_no_query_params(self):
        with self.client:
            hotel_obj = hotel(name="Hotel ABC", location="City XYZ", description="A luxurious hotel")
            db.session.add(hotel_obj)
            db.session.commit()

            chambre1 = chambres(numero="101", nb_personne=2, hotel_id=hotel_obj.id)
            chambre2 = chambres(numero="102", nb_personne=2, hotel_id=hotel_obj.id)
            chambre3 = chambres(numero="103", nb_personne=3, hotel_id=hotel_obj.id)
            chambre4 = chambres(numero="104", nb_personne=3, hotel_id=hotel_obj.id)
            chambre5 = chambres(numero="105", nb_personne=4, hotel_id=hotel_obj.id)
            db.session.add_all([chambre1, chambre2, chambre3, chambre4, chambre5])
            db.session.commit()

            response = self.client.get('/chambres?hotel_id='+str(hotel_obj.id))
            data = response.get_json()
            for i in [chambre1, chambre2, chambre3, chambre4, chambre5,hotel_obj]:
                db.session.delete(i)
            db.session.commit()

            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 5)

    def test_get_chambres_with_limit_query_param(self):
        with self.client:
            hotel_obj = hotel(name="Hotel ABC", location="City XYZ", description="A luxurious hotel")
            db.session.add(hotel_obj)
            db.session.commit()

            listchambre=[]
            for i in range(15):
                chambre = chambres(numero=f"Chambre {i}", nb_personne=2, hotel_id=hotel_obj.id)
                listchambre.append(chambre)
                db.session.add(chambre)
            db.session.commit()

            response = self.client.get('/chambres?limit=15')
            data = response.get_json()

            for i in listchambre:
                db.session.delete(i)
            db.session.delete(hotel_obj)
            db.session.commit()

            self.assertEqual(response.status_code, 200)
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 15)

    def test_get_chambres_non_existing_hotel(self):
        with self.client:
            response = self.client.get('/chambres?hotel_id=999')

            self.assertEqual(response.status_code, 200)
            data = response.get_json()

            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 0)
    
if __name__ == '__main__':
    unittest.main()
    app.run()