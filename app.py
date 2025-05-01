from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import database 

app = Flask(__name__)
app.secret_key = 'securekey'

inventory = []
sales = []
customers = {}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = database.get_user(username)
        if user and check_password_hash(user[1], password):
            session['user'] = username
            session['role'] = user[2]
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
    return render_template('index.html', inventory=inventory, role=session['role'])

@app.route('/add', methods=['POST'])
def add():
    if 'user' not in session or session['role'] != 'admin':
        return redirect('/')
    name = request.form['name']
    price = float(request.form['price'])
    stock = int(request.form['stock'])
    for item in inventory:
        if item['name'] == name:
            item['price'] = price
            item['stock'] += stock
            return redirect('/home')
    inventory.append({'name': name, 'price': price, 'stock': stock})
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

    for item in inventory:
        if item['name'] == name and item['stock'] >= quantity:
            item['stock'] -= quantity

            total_sale_price = selling_price * quantity
            total_discount = (discount / 100) * total_sale_price
            total_tax = (tax / 100) * total_sale_price
            final_price = total_sale_price - total_discount + total_tax

            sales.append({
                'name': name,
                'quantity': quantity,
                'selling_price': selling_price,
                'discount': discount,
                'tax': tax,
                'final_price': final_price,
                'date': datetime.now(),
                'customer_name': customer_name,
                'customer_phone': customer_phone,
                'seller': seller
            })

            if customer_name not in customers:
                customers[customer_name] = []
            customers[customer_name].append({
                'name': name,
                'quantity': quantity,
                'final_price': final_price,
                'date': datetime.now(),
                'phone': customer_phone 
            })

            return redirect('/home')
    return redirect('/home')

@app.route('/report')
def report():
    if 'user' not in session:
        return redirect('/')

    daily_sales = sum(s['final_price'] for s in sales)

    cost_price_total = 0
    for s in sales:
        for item in inventory:
            if item['name'] == s['name']:
                cost_price_total += item['price'] * s['quantity']
                break

    net_profit = daily_sales - cost_price_total

    return render_template('report.html', 
        sales=sales, 
        total_revenue=daily_sales, 
        total_expenses=cost_price_total, 
        net_profit=net_profit
    )


@app.route('/customer_history/<customer_name>')
@app.route('/customer_history', methods=['GET', 'POST'])
def customer_history(customer_name=None):
    if 'user' not in session:
        return redirect('/')

    customer_data = []
    if request.method == 'POST':
        search_input = request.form['customer_input'].lower()

        
        for name, data in customers.items():
            if name.lower() == search_input:
                customer_name = name
                customer_data = data
                break
            elif data and data[0].get('phone') == search_input:
                customer_name = name
                customer_data = data
                break
    elif customer_name:
        customer_data = customers.get(customer_name, [])

    return render_template('customer_history.html', customer_name=customer_name, customer_data=customer_data)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
