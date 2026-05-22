# test_cafe.py - Unit Tests for Cafe Management System
# COMSATS University Islamabad, Attock Campus | Course: SQE
# Run: python -m unittest test_cafe -v

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import cafe_management as cafe


def reset_state():
    """Reset all global state before each test"""
    cafe.customers.clear()
    cafe.orders.clear()
    cafe.feedbacks.clear()
    cafe.receipts.clear()
    cafe.customer_id_counter = 1
    cafe.order_id_counter = 1


# ════════════════════════════════════════
#  TEST SUITE 1 - MENU
# ════════════════════════════════════════

class TestMenu(unittest.TestCase):

    def setUp(self):
        cafe.MENU["Espresso"] = 300
        cafe.MENU["Latte"] = 400

    def test_get_price_valid_item(self):
        """Known item should return correct price"""
        self.assertEqual(cafe.get_price("Espresso"), 300)

    def test_get_price_another_item(self):
        """Latte price should be 400"""
        self.assertEqual(cafe.get_price("Latte"), 400)

    def test_get_price_unknown_item_returns_zero(self):
        """Unknown item should return 0"""
        self.assertEqual(cafe.get_price("Burger"), 0)

    def test_add_menu_item_success(self):
        """Adding a new item should succeed"""
        result = cafe.add_menu_item("Green Tea", 250)
        self.assertTrue(result)
        self.assertEqual(cafe.get_price("Green Tea"), 250)

    def test_add_menu_item_none_name_fails(self):
        """Adding item with None name should return False"""
        result = cafe.add_menu_item(None, 250)
        self.assertFalse(result)

    def test_add_menu_item_zero_price_fails(self):
        """Adding item with 0 price should return False"""
        result = cafe.add_menu_item("FreeItem", 0)
        self.assertFalse(result)

    def test_add_menu_item_negative_price_fails(self):
        """Negative price should return False"""
        result = cafe.add_menu_item("NegItem", -50)
        self.assertFalse(result)

    def test_remove_existing_item(self):
        """Removing an existing item should return True"""
        result = cafe.remove_menu_item("Espresso")
        self.assertTrue(result)

    def test_remove_nonexistent_item(self):
        """Removing a non-existent item should return False"""
        result = cafe.remove_menu_item("FakeItem")
        self.assertFalse(result)

    def test_calculate_price_with_tax(self):
        """Price with tax = price * 1.17"""
        result = cafe.calculate_price_with_tax("Espresso")
        self.assertAlmostEqual(result, 300 * 1.17, places=1)


# ════════════════════════════════════════
#  TEST SUITE 2 - CUSTOMERS
# ════════════════════════════════════════

class TestCustomers(unittest.TestCase):

    def setUp(self):
        reset_state()

    def test_add_customer_returns_dict(self):
        """add_customer should return a dictionary"""
        c = cafe.add_customer("Ali", 25, "03001234567")
        self.assertIsNotNone(c)
        self.assertEqual(c["name"], "Ali")

    def test_add_customer_assigns_id(self):
        """First customer should get ID 1"""
        c = cafe.add_customer("Sara", 30, "03009876543")
        self.assertEqual(c["id"], 1)

    def test_add_multiple_customers_unique_ids(self):
        """Each customer should have a unique ID"""
        c1 = cafe.add_customer("Ali", 25, "111")
        c2 = cafe.add_customer("Sara", 30, "222")
        self.assertNotEqual(c1["id"], c2["id"])

    def test_search_customer_found(self):
        """Search should return the correct customer"""
        cafe.add_customer("Ahmed", 22, "03001111111")
        result = cafe.search_customer("Ahmed")
        self.assertIsNotNone(result)
        self.assertEqual(result["name"], "Ahmed")

    def test_search_customer_case_insensitive(self):
        """Search should be case-insensitive"""
        cafe.add_customer("Rafia", 21, "03002222222")
        result = cafe.search_customer("rafia")
        self.assertIsNotNone(result)

    def test_search_customer_not_found(self):
        """Non-existent customer should return None"""
        result = cafe.search_customer("Ghost")
        self.assertIsNone(result)

    def test_delete_existing_customer(self):
        """Deleting existing customer should return True"""
        c = cafe.add_customer("Samrina", 23, "03003333333")
        result = cafe.delete_customer(c["id"])
        self.assertTrue(result)

    def test_delete_nonexistent_customer(self):
        """Deleting invalid ID should return False"""
        result = cafe.delete_customer(999)
        self.assertFalse(result)

    def test_get_total_customers_count(self):
        """Count should match number of added customers"""
        cafe.add_customer("A", 20, "111")
        cafe.add_customer("B", 21, "222")
        cafe.add_customer("C", 22, "333")
        self.assertEqual(cafe.get_total_customers(), 3)

    def test_delete_reduces_count(self):
        """Delete should reduce count by 1"""
        c = cafe.add_customer("X", 20, "000")
        cafe.add_customer("Y", 21, "001")
        cafe.delete_customer(c["id"])
        self.assertEqual(cafe.get_total_customers(), 1)


# ════════════════════════════════════════
#  TEST SUITE 3 - ORDERS
# ════════════════════════════════════════

class TestOrders(unittest.TestCase):

    def setUp(self):
        reset_state()

    def test_place_order_returns_dict(self):
        """Placing an order should return an order dict"""
        o = cafe.place_order("Ali", "Espresso", 2, "Take-Away", 300)
        self.assertIsNotNone(o)

    def test_place_order_correct_total(self):
        """Total = price_per_item * quantity"""
        o = cafe.place_order("Ali", "Espresso", 2, "Take-Away", 300)
        self.assertEqual(o["total_price"], 600)

    def test_home_delivery_adds_charge(self):
        """Home-Delivery should add Rs. 200 delivery charge"""
        o = cafe.place_order("Sara", "Latte", 1, "Home-Delivery", 400, "Kamra")
        self.assertEqual(o["total_price"], 600)

    def test_place_order_default_status_pending(self):
        """New order status should be Pending"""
        o = cafe.place_order("Ahmed", "Americano", 1, "Dine-In", 350)
        self.assertEqual(o["status"], "Pending")

    def test_serve_order_changes_status(self):
        """Serving an order should change status to Served"""
        o = cafe.place_order("Rafia", "Cappuccino", 1, "Take-Away", 420)
        result = cafe.serve_order(o["id"])
        self.assertTrue(result)
        self.assertEqual(o["status"], "Served")

    def test_serve_nonexistent_order_returns_false(self):
        """Invalid order ID should return False"""
        self.assertFalse(cafe.serve_order(999))

    def test_cancel_pending_order(self):
        """Cancelling a pending order should succeed"""
        o = cafe.place_order("Samrina", "Matcha", 1, "Dine-In", 380)
        result = cafe.cancel_order(o["id"])
        self.assertTrue(result)
        self.assertEqual(o["status"], "Cancelled")

    def test_cancel_served_order_fails(self):
        """Cannot cancel an already served order"""
        o = cafe.place_order("Ali", "Latte", 1, "Dine-In", 400)
        cafe.serve_order(o["id"])
        self.assertFalse(cafe.cancel_order(o["id"]))

    def test_get_pending_orders_excludes_served(self):
        """Pending list should not include served orders"""
        cafe.place_order("A", "Espresso", 1, "Take-Away", 300)
        o2 = cafe.place_order("B", "Latte", 1, "Dine-In", 400)
        cafe.serve_order(o2["id"])
        self.assertEqual(len(cafe.get_pending_orders()), 1)

    def test_get_total_orders(self):
        """Total should count all orders regardless of status"""
        cafe.place_order("A", "Espresso", 1, "Take-Away", 300)
        cafe.place_order("B", "Latte", 1, "Dine-In", 400)
        self.assertEqual(cafe.get_total_orders(), 2)


# ════════════════════════════════════════
#  TEST SUITE 4 - BILLING
# ════════════════════════════════════════

class TestBilling(unittest.TestCase):

    def setUp(self):
        reset_state()

    def test_calculate_bill_single_order(self):
        """Bill of one order = its total_price"""
        o = cafe.place_order("Ali", "Espresso", 2, "Take-Away", 300)
        self.assertEqual(cafe.calculate_bill([o]), 600)

    def test_calculate_bill_multiple_orders(self):
        """Bill should sum all order totals"""
        o1 = cafe.place_order("Ali", "Espresso", 1, "Take-Away", 300)
        o2 = cafe.place_order("Ali", "Latte", 1, "Dine-In", 400)
        self.assertEqual(cafe.calculate_bill([o1, o2]), 700)

    def test_apply_student_discount(self):
        """Student gets 10% off"""
        self.assertEqual(cafe.apply_discount(1000, "student"), 900.0)

    def test_apply_senior_discount(self):
        """Senior gets 15% off"""
        self.assertEqual(cafe.apply_discount(1000, "senior"), 850.0)

    def test_apply_member_discount(self):
        """Member gets 20% off"""
        self.assertEqual(cafe.apply_discount(1000, "member"), 800.0)

    def test_apply_unknown_discount_no_change(self):
        """Unknown type should give 0% discount"""
        self.assertEqual(cafe.apply_discount(1000, "vip"), 1000.0)

    def test_generate_receipt_saves_record(self):
        """Receipt should appear in receipts list"""
        o = cafe.place_order("Sara", "Americano", 1, "Dine-In", 350)
        cafe.generate_receipt("Sara", [o])
        self.assertEqual(len(cafe.receipts), 1)

    def test_total_earnings_sum(self):
        """Total earnings = sum of all receipt final totals"""
        o1 = cafe.place_order("Ali", "Espresso", 1, "Take-Away", 300)
        o2 = cafe.place_order("Sara", "Latte", 1, "Dine-In", 400)
        cafe.generate_receipt("Ali", [o1])
        cafe.generate_receipt("Sara", [o2])
        self.assertEqual(cafe.get_total_earnings(), 700)

    def test_earnings_with_discount(self):
        """Earnings should reflect discounted price"""
        o = cafe.place_order("Ahmed", "Americano", 1, "Dine-In", 1000)
        cafe.generate_receipt("Ahmed", [o], "student")
        self.assertEqual(cafe.get_total_earnings(), 900.0)

    def test_receipt_no_discount_full_price(self):
        """No discount means final_total equals subtotal"""
        o = cafe.place_order("Ali", "Espresso", 1, "Take-Away", 500)
        r = cafe.generate_receipt("Ali", [o])
        self.assertEqual(r["final_total"], 500)


# ════════════════════════════════════════
#  TEST SUITE 5 - FEEDBACK
# ════════════════════════════════════════

class TestFeedback(unittest.TestCase):

    def setUp(self):
        reset_state()

    def test_add_valid_feedback(self):
        """Valid rating (1-5) should be accepted"""
        self.assertTrue(cafe.add_feedback("Ali", 5, "Excellent!"))

    def test_add_minimum_rating(self):
        """Rating of 1 is valid"""
        self.assertTrue(cafe.add_feedback("Sara", 1, "Very bad"))

    def test_add_rating_above_five_fails(self):
        """Rating > 5 should be rejected"""
        self.assertFalse(cafe.add_feedback("Ahmed", 6, "Out of range"))

    def test_add_rating_below_one_fails(self):
        """Rating < 1 should be rejected"""
        self.assertFalse(cafe.add_feedback("Rafia", 0, "Zero"))

    def test_feedback_count_increases(self):
        """Valid feedbacks should increase the count"""
        cafe.add_feedback("A", 4, "Good")
        cafe.add_feedback("B", 3, "Okay")
        self.assertEqual(cafe.get_feedback_count(), 2)

    def test_average_rating_correct(self):
        """Average should be (4+2)/2 = 3.0"""
        cafe.add_feedback("Ali", 4, "Good")
        cafe.add_feedback("Sara", 2, "Bad")
        self.assertEqual(cafe.get_average_rating(), 3.0)

    def test_average_rating_no_feedback_returns_zero(self):
        """No feedback should return average of 0"""
        self.assertEqual(cafe.get_average_rating(), 0)

    def test_positive_feedback_filter(self):
        """Positive = rating >= 4"""
        cafe.add_feedback("Ali", 5, "Amazing")
        cafe.add_feedback("Sara", 2, "Bad")
        cafe.add_feedback("Ahmed", 4, "Good")
        self.assertEqual(len(cafe.get_positive_feedback()), 2)

    def test_negative_feedback_filter(self):
        """Negative = rating <= 2"""
        cafe.add_feedback("Ali", 5, "Amazing")
        cafe.add_feedback("Sara", 1, "Terrible")
        cafe.add_feedback("Ahmed", 2, "Poor")
        self.assertEqual(len(cafe.get_negative_feedback()), 2)

    def test_all_five_stars_average(self):
        """All 5-star ratings should average to 5.0"""
        cafe.add_feedback("A", 5, "Perfect")
        cafe.add_feedback("B", 5, "Loved it")
        self.assertEqual(cafe.get_average_rating(), 5.0)


# ════════════════════════════════════════
if __name__ == "__main__":
    unittest.main(verbosity=2)
