from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import firebase_db as database

app = Flask(__name__)
app.secret_key = 'securekey'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = database.get_user(username)
        if user and check_password_hash(user[0], password):
            session['user'] = username
            session['role'] = user[1]
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        if not database.get_user(username):
            hashed_password = generate_password_hash(password)
            database.create_user(username, hashed_password, role)
            return redirect('/')
    return render_template('register.html')

@app.route('/home')
def home():
    if 'user' not in session:
        return redirect('/')
    inventory = database.get_inventory()
    return render_template('index.html', inventory=inventory, role=session['role'])

@app.route('/add', methods=['POST'])
def add():
    if 'user' not in session or session['role'] != 'admin':
        return redirect('/')
    name = request.form['name']
    price = float(request.form['price'])
    stock = int(request.form['stock'])
    inventory = database.get_inventory()
    existing = next((item for item in inventory if item['name'] == name), None)
    if existing:
        new_stock = existing['stock'] + stock
        database.update_inventory(name, price, new_stock)
    else:
        database.add_inventory(name, price, stock)
    return redirect('/home')

@app.route('/sell', methods=['POST'])
def sell():
    if 'user' not in session:
        return redirect('/')
    name = request.form['name']
    quantity = int(request.form['quantity'])
    selling_price = float(request.form['selling_price'])
    discount = float(request.form['discount'])
    tax = float(request.form['tax'])
    customer_name = request.form['customer_name']
    customer_phone = request.form['customer_phone']
    seller = session['user']
    inventory = database.get_inventory()
    for item in inventory:
        if item['name'] == name and item['stock'] >= quantity:
            updated_stock = item['stock'] - quantity
            database.update_inventory(name, item['price'], updated_stock)
            total_sale_price = selling_price * quantity
            total_discount = (discount / 100) * total_sale_price
            total_tax = (tax / 100) * total_sale_price
            final_price = total_sale_price - total_discount + total_tax
            sale_data = {
                'name': name,
                'quantity': quantity,
                'selling_price': selling_price,
                'discount': discount,
                'tax': tax,
                'final_price': final_price,
                'date': datetime.now().isoformat(),
                'customer_name': customer_name,
                'customer_phone': customer_phone,
                'seller': seller
            }
            database.record_sale(sale_data)
            customer_entry = {
                'name': name,
                'quantity': quantity,
                'final_price': final_price,
                'date': datetime.now().isoformat(),
                'phone': customer_phone
            }
            database.add_customer_history(customer_name, customer_entry)
            break
    return redirect('/home')

@app.route('/report')
def report():
    if 'user' not in session:
        return redirect('/')
    inventory = database.get_inventory()
    sales = database.get_sales()
    daily_sales = sum(s['final_price'] for s in sales)
    cost_price_total = 0
    for s in sales:
        for item in inventory:
            if item['name'] == s['name']:
                cost_price_total += item['price'] * s['quantity']
                break
    net_profit = daily_sales - cost_price_total
    for sale in sales:
        if isinstance(sale['date'], str):
            sale['date'] = datetime.fromisoformat(sale['date']) 
    return render_template('report.html', sales=sales, total_revenue=daily_sales, total_expenses=cost_price_total, net_profit=net_profit)

@app.route('/customer_history/<customer_name>')
@app.route('/customer_history', methods=['GET', 'POST'])
def customer_history(customer_name=None):
    if 'user' not in session:
        return redirect('/')
    customer_data = []
    if request.method == 'POST':
        search_input = request.form['customer_input'].lower()
        customers = database.get_all_customers()
        for name, data in customers.items():
            if name.lower() == search_input:
                customer_name = name
                customer_data = list(data.values())
                break
            elif data:
                for entry in data.values():
                    if entry.get('phone') == search_input:
                        customer_name = name
                        customer_data = list(data.values())
                        break
    elif customer_name:
        customer_data = database.get_customer_history(customer_name)
    for entry in customer_data:
        if isinstance(entry.get('date'), str):
            entry['date'] = datetime.fromisoformat(entry['date'])
    
    return render_template('customer_history.html', customer_name=customer_name, customer_data=customer_data)

@app.route('/analytics')
def analytics():
    if 'user' not in session:
        return redirect('/')
    sales = database.get_sales()
    
    from collections import defaultdict
    import calendar

    monthly_totals = defaultdict(float)
    product_counts = defaultdict(int)

    for sale in sales:
        if isinstance(sale['date'], str):
            date = datetime.fromisoformat(sale['date'])
        else:
            date = sale['date']
        month = date.strftime('%b')
        monthly_totals[month] += sale['final_price']
        product_counts[sale['name']] += sale['quantity']

    month_order = list(calendar.month_abbr)[1:]
    sorted_months = [m for m in month_order if m in monthly_totals]
    monthly_data = [monthly_totals[m] for m in sorted_months]
    sorted_products = sorted(product_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    product_names = [p[0] for p in sorted_products]
    product_values = [p[1] for p in sorted_products]

    return render_template("analytics.html",
                           months=sorted_months,
                           revenues=monthly_data,
                           top_products=product_names,
                           product_counts=product_values)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
