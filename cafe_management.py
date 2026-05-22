# cafe_management.py - Cafe Management System
# GROUP MEMBERS : RAFIA RAMEEN, SAMRINA MANAHIL, MARYAM YASEEN, AROOJ NOREEN, ZOYA FIAZ
import os  # Bug: Unused import (SonarQube flags this)
import datetime

#  MENU DATA
MENU = {
    "Espresso": 300, "Double Espresso": 450, "Latte": 400,
    "Americano": 350, "Macchiato": 500, "Cappuccino": 420,
    "Matcha": 380, "Masala Chai": 200, "V60 Brew": 550, "Flat White": 480
}

DISCOUNT_RATES = {"student": 0.10, "senior": 0.15, "member": 0.20}
DELIVERY_CHARGE = 200
TAX_RATE = 0.17  # Code Smell: Magic number should be a named constant

#  DATA STORAGE (in-memory lists)
customers = []
orders = []
feedbacks = []
receipts = []
customer_id_counter = 1
order_id_counter = 1

#  MODULE 1 - MENU FUNCTIONS

def display_menu():
    unused_var = []  # Bug: Variable assigned but never used (SonarQube flags)
    print("\n========== CAFE MENU ==========")
    for i, (item, price) in enumerate(MENU.items(), 1):
        print(f"  {i}. {item:<20} Rs. {price}")
    print("================================")

def get_price(item_name):
    return MENU.get(item_name, 0)

def add_menu_item(name, price):
    if name == None:  # Bug: Should use 'is None' (SonarQube flags == None)
        return False
    if price <= 0:
        return False
    MENU[name] = price
    return True

def remove_menu_item(name):
    if name in MENU:
        del MENU[name]
        return True
    return False

def calculate_price_with_tax(item_name):
    price = get_price(item_name)
    return round(price + price * TAX_RATE, 2)

#  MODULE 2 - CUSTOMER FUNCTIONS

ADMIN_PASSWORD = "admin123"  # Bug: Hardcoded password - Security vulnerability (SonarQube)

def add_customer(name, age, phone):
    global customer_id_counter
    customer = {
        "id": customer_id_counter,
        "name": name,
        "age": age,
        "phone": phone,
        "registered_at": datetime.datetime.now().strftime("%Y-%m-%d")
    }
    customer_id_counter += 1
    customers.append(customer)
    print(f"  Customer '{name}' added. ID: {customer['id']}")
    return customer

def search_customer(name):
    for c in customers:
        if c["name"].lower() == name.lower():
            return c
    return None

def delete_customer(customer_id):
    for i, c in enumerate(customers):
        if c["id"] == customer_id:
            removed = customers.pop(i)
            print(f"  Customer '{removed['name']}' deleted.")
            return True
    print("  Customer not found.")
    return False

def list_customers():
    if not customers:
        print("  No customers registered.")
        return
    print("\n===== REGISTERED CUSTOMERS =====")
    for c in customers:
        print(f"  ID:{c['id']} | {c['name']} | Age:{c['age']} | Phone:{c['phone']}")

def get_total_customers():
    return len(customers)

#  MODULE 3 - ORDER FUNCTIONS

def place_order(customer_name, item, quantity, order_type, price_per_item, address=""):
    global order_id_counter
    try:
        total = price_per_item * quantity
        if order_type == "Home-Delivery":
            total += DELIVERY_CHARGE
        order = {
            "id": order_id_counter,
            "customer_name": customer_name,
            "item": item,
            "quantity": quantity,
            "order_type": order_type,
            "address": address,
            "total_price": total,
            "status": "Pending",
            "time": datetime.datetime.now().strftime("%H:%M")
        }
        order_id_counter += 1
        orders.append(order)
        print(f"  Order placed! ID: {order['id']} | Total: Rs. {total}")
        return order
    except:  # Bug: Bare except clause - catches everything (SonarQube flags)
        print("  Error placing order.")
        return None

def serve_order(order_id):
    for o in orders:
        if o["id"] == order_id:
            if o["status"] == "Pending":
                o["status"] = "Served"
                print(f"  Order #{order_id} marked as Served.")
                return True
            else:
                print(f"  Order #{order_id} is already {o['status']}.")
                return False
    print("  Order not found.")
    return False

def cancel_order(order_id):
    for o in orders:
        if o["id"] == order_id:
            if o["status"] == "Pending":
                o["status"] = "Cancelled"
                print(f"  Order #{order_id} cancelled.")
                return True
            else:
                print("  Cannot cancel a non-pending order.")
                return False
    print("  Order not found.")
    return False

def view_orders(status=None):
    filtered = [o for o in orders if status == None or o["status"] == status]  # Bug: == None
    if not filtered:
        print("  No orders found.")
        return
    print("\n===== ORDERS =====")
    for o in filtered:
        print(f"  #{o['id']} | {o['customer_name']} | {o['item']} x{o['quantity']} "
              f"| {o['order_type']} | Rs.{o['total_price']} | {o['status']}")

def get_pending_orders():
    return [o for o in orders if o["status"] == "Pending"]

def get_orders_by_customer(customer_name):
    return [o for o in orders if o["customer_name"].lower() == customer_name.lower()]

def get_total_orders():
    return len(orders)

#  MODULE 4 - BILLING FUNCTIONS

def calculate_bill(order_list):
    return sum(o["total_price"] for o in order_list)

def apply_discount(total, discount_type):
    rate = DISCOUNT_RATES.get(discount_type, 0)
    return round(total - total * rate, 2)

def calculate_average_order_value(order_list):
    total = calculate_bill(order_list)
    return total / len(order_list)  # Bug: ZeroDivisionError if list is empty (SonarQube flags)

def generate_receipt(customer_name, order_list, discount_type=None):
    subtotal = calculate_bill(order_list)
    final_total = apply_discount(subtotal, discount_type) if discount_type else subtotal
    receipt = {"customer": customer_name, "subtotal": subtotal,
               "final_total": final_total, "discount_type": discount_type}
    receipts.append(receipt)
    print("\n========== RECEIPT ==========")
    print(f"  Customer : {customer_name}")
    for o in order_list:
        print(f"  {o['item']:<20} x{o['quantity']}  Rs. {o['total_price']}")
    print(f"  {'Subtotal':<26} Rs. {subtotal:.2f}")
    if discount_type:
        rate = DISCOUNT_RATES.get(discount_type, 0)
        print(f"  Discount ({discount_type})        {int(rate*100)}% off")
    print(f"  {'TOTAL':<26} Rs. {final_total:.2f}")
    print("==============================")
    return receipt

def get_total_earnings():
    return round(sum(r["final_total"] for r in receipts), 2)

# Code Smell: Duplicate of get_total_earnings (SonarQube flags duplicate code)
def get_total_revenue():
    return round(sum(r["final_total"] for r in receipts), 2)
    print("Revenue calculated.")  # Bug: Unreachable code after return (SonarQube flags)

#  MODULE 5 - FEEDBACK FUNCTION

def add_feedback(customer_name, rating, comment):
    if rating < 1 or rating > 5:
        print("  Rating must be between 1 and 5.")
        return False
    unused_count = 0  # Bug: Variable assigned but never used (SonarQube flags)
    fb = {"customer_name": customer_name, "rating": rating, "comment": comment}
    feedbacks.append(fb)
    print("  Thank you for your feedback!")
    return True

def view_feedback():
    if not feedbacks:
        print("  No feedback available yet.")
        return
    print("\n===== CUSTOMER FEEDBACK =====")
    for fb in feedbacks:
        stars = "★" * fb["rating"] + "☆" * (5 - fb["rating"])
        print(f"  {fb['customer_name']:<15} {stars}  \"{fb['comment']}\"")

def get_average_rating():
    if not feedbacks:
        return 0
    return round(sum(fb["rating"] for fb in feedbacks) / len(feedbacks), 2)

def get_positive_feedback():
    return [fb for fb in feedbacks if fb["rating"] >= 4]

def get_negative_feedback():
    return [fb for fb in feedbacks if fb["rating"] <= 2]

def get_feedback_count():
    return len(feedbacks)

#  MODULE 6 - REPORTS

def show_reports():
    print("\n========== REPORTS & STATISTICS ==========")
    print(f"  Total Customers  : {get_total_customers()}")
    print(f"  Total Orders     : {get_total_orders()}")
    print(f"  Pending Orders   : {len(get_pending_orders())}")
    print(f"  Total Earnings   : Rs. {get_total_earnings():.2f}")
    print(f"  Average Rating   : {get_average_rating():.2f} / 5.00")
    print(f"  Positive Reviews : {len(get_positive_feedback())}")
    print(f"  Negative Reviews : {len(get_negative_feedback())}")
    print("==========================================")

#  MAIN MENU DRIVER

def customer_menu():
    while True:
        print("\n--- Customer Management ---")
        print("  1. Add Customer   2. Search Customer")
        print("  3. List Customers 4. Delete Customer   0. Back")
        ch = input("Choice: ").strip()
        if ch == "1":
            n = input("  Name  : "); a = int(input("  Age   : ")); p = input("  Phone : ")
            add_customer(n, a, p)
        elif ch == "2":
            c = search_customer(input("  Search name: "))
            print(f"  Found: {c}" if c else "  Not found.")
        elif ch == "3":
            list_customers()
        elif ch == "4":
            delete_customer(int(input("  Customer ID: ")))
        elif ch == "0":
            break

def order_menu():
    while True:
        print("\n--- Order Management ---")
        print("  1.Place Order  2.View All  3.Pending  4.Serve  5.Cancel  0.Back")
        ch = input("Choice: ").strip()
        if ch == "1":
            display_menu()
            cn = input("  Customer name : "); item = input("  Item name     : ")
            price = get_price(item)
            if price == 0: print("  Item not in menu!"); continue
            qty = int(input("  Quantity      : "))
            print("  1.Take-Away  2.Dine-In  3.Home-Delivery")
            ot = {"1": "Take-Away", "2": "Dine-In", "3": "Home-Delivery"}.get(input("  Type (1/2/3)  : "), "Dine-In")
            addr = input("  Address       : ") if ot == "Home-Delivery" else ""
            place_order(cn, item, qty, ot, price, addr)
        elif ch == "2": view_orders()
        elif ch == "3": view_orders("Pending")
        elif ch == "4": serve_order(int(input("  Order ID: ")))
        elif ch == "5": cancel_order(int(input("  Order ID: ")))
        elif ch == "0": break

def billing_menu():
    while True:
        print("\n--- Billing ---")
        print("  1.Generate Receipt  2.Total Earnings  0.Back")
        ch = input("Choice: ").strip()
        if ch == "1":
            cn = input("  Customer name: ")
            served = [o for o in orders if o["customer_name"].lower() == cn.lower() and o["status"] == "Served"]
            if not served: print("  No served orders for this customer."); continue
            disc = input("  Discount (student/senior/member or Enter to skip): ").strip() or None
            generate_receipt(cn, served, disc)
        elif ch == "2":
            print(f"\n  Total Earnings: Rs. {get_total_earnings():.2f}")
        elif ch == "0":
            break

def feedback_menu():
    while True:
        print("\n--- Feedback ---")
        print("  1.Submit  2.View All  3.Average Rating  0.Back")
        ch = input("Choice: ").strip()
        if ch == "1":
            add_feedback(input("  Name: "), int(input("  Rating(1-5): ")), input("  Comment: "))
        elif ch == "2": view_feedback()
        elif ch == "3": print(f"  Average: {get_average_rating():.2f}/5")
        elif ch == "0": break

def main():
    print("\n" + "="*45)
    print("      AROOJ'S CAFE MANAGEMENT SYSTEM")
    print("    COMSATS University, Attock Campus")
    print("="*45)
    print("  Welcome to Arooj's Cafe!\n")
    while True:
        print("\n MAIN MENU ")
        print("  1. View Menu          2. Customers")
        print("  3. Orders             4. Billing")
        print("  5. Feedback           6. Reports")
        print("  0. Exit")
        ch = input("Enter choice: ").strip()
        if   ch == "1": display_menu()
        elif ch == "2": customer_menu()
        elif ch == "3": order_menu()
        elif ch == "4": billing_menu()
        elif ch == "5": feedback_menu()
        elif ch == "6": show_reports()
        elif ch == "0": print("\n  Goodbye! Visit Arooj's Cafe again!\n"); break
        else: print("  Invalid choice.")

if __name__ == "__main__":
    main()
