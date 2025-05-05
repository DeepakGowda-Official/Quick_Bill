import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("private_key.json")#download the json file from firebase and place it under your main folder
firebase_admin.initialize_app(cred, {
    'databaseURL': ''#Place your Firebase Real time databse key here 
})

def get_user(username):
    ref = db.reference(f'users/{username}')
    user = ref.get()
    if user:
        return user['password'], user['role']
    return None

def create_user(username, password, role):
    ref = db.reference(f'users/{username}')
    ref.set({
        'password': password,
        'role': role
    })

def get_inventory():
    ref = db.reference('inventory')
    inventory = ref.get()
    if not inventory:
        return []
    return [{'name': k, 'price': v['price'], 'stock': v['stock']} for k, v in inventory.items()]

def add_inventory(name, price, stock):
    ref = db.reference(f'inventory/{name}')
    ref.set({
        'price': price,
        'stock': stock
    })

def update_inventory(name, price, stock):
    ref = db.reference(f'inventory/{name}')
    ref.update({
        'price': price,
        'stock': stock
    })

def record_sale(sale_data):
    ref = db.reference('sales')
    ref.push(sale_data)

def get_sales():
    ref = db.reference('sales')
    sales = ref.get()
    if not sales:
        return []
    return list(sales.values())

def add_customer_history(customer_name, entry):
    ref = db.reference(f'customers/{customer_name}')
    ref.push(entry)

def get_customer_history(customer_name):
    ref = db.reference(f'customers/{customer_name}')
    data = ref.get()
    if not data:
        return []
    return list(data.values())

def get_all_customers():
    ref = db.reference('customers')
    customers = ref.get()
    if not customers:
        return {}
    return customers
