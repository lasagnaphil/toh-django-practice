from django.test import TestCase, Client
from .models import Hero
from django.forms.models import model_to_dict
import json

# Create your tests here.
class HeroTestCase(TestCase):
    def setUp(self):
        Hero.objects.create(name='Superman')
        Hero.objects.create(name='Batman')
        Hero.objects.create(name='Joker')

        self.client = Client()

    def test_hero_str(self):
        batman = Hero.objects.get(name='Batman')
        self.assertEqual(str(batman), 'Batman')

    def test_hero_list_get(self):
        response = self.client.get('/api/hero')
        
        data = json.loads(response.content.decode())
        self.assertEqual(data[0]['name'], 'Superman')
        self.assertEqual(data[1]['name'], 'Batman')
        self.assertEqual(data[2]['name'], 'Joker')

    def test_hero_list_post(self):
        response = self.client.post('/api/hero', data=json.dumps({'name': 'Spiderman'}), content_type='application/json')
        
        self.assertEqual(Hero.objects.get(id=4).name, 'Spiderman')
        self.assertEqual(response.status_code, 201)

    def test_hero_list_delete_not_allowed(self):
        response = self.client.delete('/api/hero')

        self.assertEqual(response.status_code, 405)

    def test_hero_detail_get(self):
        response = self.client.get('/api/hero/1')

        data = json.loads(response.content.decode())
        self.assertEqual(data['name'], 'Superman')
        self.assertEqual(response.status_code, 200)

    def test_hero_detail_get_not_found(self):
        response = self.client.get('/api/hero/4')
        
        self.assertEqual(response.status_code, 404)

    def test_hero_detail_post(self):
        response = self.client.post('/api/hero/1', data=json.dumps({'name': 'Spiderman'}), content_type='application/json')

        self.assertEqual(response.status_code, 405)

    def test_hero_detail_put(self):
        response = self.client.put('/api/hero/1', json.dumps({'name': 'Spiderman'}), content_type='application/json')

        self.assertEqual(Hero.objects.get(id=1).name, 'Spiderman')
        self.assertEqual(response.status_code, 204)

    def test_hero_detail_put_not_found(self):
        response = self.client.put('/api/hero/4', json.dumps({'name': 'Spiderman'}), content_type='application/json')

        self.assertEqual(response.status_code, 404)

    def test_hero_detail_delete(self):
        response = self.client.delete('/api/hero/1')
        
        try:
            hero = Hero.objects.get(id=1)
        except Hero.DoesNotExist:
            hero = None

        self.assertEqual(hero, None)

    def test_hero_detail_delete_not_found(self):
        response = self.client.delete('/api/hero/4')

        self.assertEqual(response.status_code, 404)
