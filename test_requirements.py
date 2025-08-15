import unittest
import re
from value_calc import example_calculations, FLIGHT_AWARD_CPM, HOTEL_CPM, GIFT_CARD_CPM
from recommender import recommend_best_redemptions
import app as webapp


class RequirementsTest(unittest.TestCase):
    def test_value_calculator_examples(self):
        examples = example_calculations()
        # Presence of categories
        self.assertIn('flight', examples)
        self.assertIn('hotel', examples)
        self.assertIn('gift_card', examples)
        # Required fields exist
        for key in ['flight', 'hotel', 'gift_card']:
            ex = examples[key]
            for field in ['cash_price_usd', 'taxes_fees_usd', 'miles_needed', 'value_per_mile_cents']:
                self.assertIn(field, ex)
                self.assertIsNotNone(ex[field])
        # Relative value heuristic: flights >= hotels >= gift cards with our CPM settings
        self.assertGreaterEqual(examples['flight']['value_per_mile_cents'], examples['hotel']['value_per_mile_cents'])
        self.assertGreaterEqual(examples['hotel']['value_per_mile_cents'], examples['gift_card']['value_per_mile_cents'])
        # CPM sanity
        self.assertGreater(FLIGHT_AWARD_CPM, HOTEL_CPM)
        self.assertGreater(HOTEL_CPM, GIFT_CARD_CPM)

    def test_recommendation_output(self):
        # Using mock fallback inside routing
        res = recommend_best_redemptions('JFK', 'LAX', '2025-09-01', miles_available=30000)
        self.assertIn('recommendations', res)
        recs = res['recommendations']
        self.assertIsInstance(recs, list)
        self.assertGreater(len(recs), 0)
        # Sorted by value_per_mile_cents desc
        values = [r.get('value_per_mile_cents', 0) for r in recs]
        self.assertEqual(values, sorted(values, reverse=True))

    def test_web_endpoints(self):
        app = webapp.app
        app.testing = True
        client = app.test_client()

        # GET /
        r = client.get('/')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Redemption Optimizer', r.data)

        # POST /recommend
        r = client.post('/recommend', data={
            'origin': 'JFK',
            'destination': 'LAX',
            'departure_date': '2025-09-01',
            'miles_available': '25000',
        })
        self.assertEqual(r.status_code, 200)
        self.assertRegex(r.data.decode('utf-8'), re.compile(r'Top\s+recommendations', re.IGNORECASE))

        # POST /feedback
        r = client.post('/feedback', data={
            'origin': 'JFK',
            'destination': 'LAX',
            'departure_date': '2025-09-01',
            'miles_available': '25000',
            'rating': '5',
            'comments': 'Great!'
        }, follow_redirects=True)
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Thanks for your feedback', r.data)


if __name__ == '__main__':
    unittest.main(verbosity=2) 