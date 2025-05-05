# 🛒 QuickBill: Smart Inventory & Billing Web App (Flask-Based)

🎯 **Streamline billing, manage stock, and simplify sales—all from your browser!**

---

## 🌟 Why QuickBill?

Small-scale stores often struggle with **manual billing**, **confusing inventory records**, and **no digital tracking**—leading to errors and inefficiencies. Large ERP tools are **too bulky, expensive**, and often overkill for their needs.

📌 **QuickBill is different!** It’s a **lightweight**, **web-based**, and **cloud-driven** solution that brings digital billing to your fingertips—with a clean UI and robust backend support!

---

## 🚨 What Makes QuickBill Stand Out?

✅ Built using **Flask**, runs locally with **zero deployment cost**.  
✅ Designed with both **Admin and Staff roles** for secure access.  
✅ Supports **real-time product updates, bill generation**, and **stock checks**.  
✅ All product data handled via **Firebase**—no traditional database setup required! 
✅ Designed for **college mini-stores, stationery shops, and pop-up stalls**.

---

## 🌍 Key Features

✔️ **Dynamic Inventory:** Add, update, and sell products on the go.  
✔️ **Bill Generator:** Generates neat bills instantly with all item details.  
✔️ **Role-Based Login:** Admin and staff interfaces keep operations secure.  
✔️ **Firebase Data Handling:** Real-time data management using Firebase.  
✔️ **Smooth UI:** Gradient color designs for a clean and modern experience.

---

## 🧠 Barcode Feature – The Vision Ahead

> 📸 **Camera access is already integrated**—laying the foundation for future barcode integration.

While the complete barcode system isn't implemented yet, **QuickBill already supports camera access via the `sell` page**, making it ready for real-time barcode scanning!

---

### 🛠 How Full Barcode Integration Can Be Done

Here’s how barcode functionality can be added:

1️⃣ Install the required Python libraries:

sh

    pip install python-barcode Pillow"

2️⃣ On adding a new product, generate a barcode using python-barcode and store it in the static/barcodes/ folder.

3️⃣ Create a dedicated /barcodes page displaying each product and its barcode for scanning and printing.

4️⃣ Use QuaggaJS or ZXing JavaScript libraries to read barcodes from live camera feed, and auto-fill product details during billing.

---

### ❓ Why It's Not Fully Implemented (Yet)

Barcode scanners vary significantly based on industry & scale:

🔧 In automobile manufacturing, barcode readers are embedded with complex part codes.
🛒 In retail or groceries, barcodes follow UPC/EAN standards linked to centralized systems.
🏪 For small vendors, manual entry or QR scanning from mobile phones is more practical.

📌 So to keep QuickBill flexible, only a sample camera scanner interface is provided—you can easily plug in your preferred scanning method depending on your domain.

## ⚡ How It Works?
1️⃣ Admin or User logs in with credentials.

2️⃣ Navigate to Home for product operations, or Sell for billing.

3️⃣ Products are added to the bill dynamically and quantities tracked.

4️⃣ Hit Generate Bill to display a cloud-based breakdown (via Firebase).

5️⃣ For barcode testing, open camera via the integrated scanner preview.

---

## 🛠 Tech Stack

Flask (Python) – Core backend framework

HTML5 + CSS3 – Frontend design

JavaScript – Camera access, dynamic forms

python-barcode & Pillow – (Optional) Barcode generation

QuaggaJS / ZXing – (Optional) For barcode scanning

Firebase – For real-time cloud-based data management

## 🧾 Sample Use Cases

🛍️ Stationery Store

🍔 College Canteens

🧪 Lab Inventory Management

💊 Medical Counters

🛒 Pop-up Retail Booths

💡 Customizable for both offline local use and scalable cloud integration (future-ready)!

---

### 📸 Screenshots

# 🔑 Login/Register Page with Role Selection
![image](https://github.com/user-attachments/assets/ff6f3ef2-7e1f-4f89-ae1d-b59c85c0d0c2)

# Admin Dashboard: Inventory Control
![image](https://github.com/user-attachments/assets/38ec74b1-e53b-4fa8-9c39-2e6052235cbc)

# Making a sale (Session-based)
![image](https://github.com/user-attachments/assets/ad662f84-db3c-4223-94cc-becb538e99f4)

# Sales Analysis report
![image](https://github.com/user-attachments/assets/c4315296-0605-4750-ad3f-b0f2489a63c3)

# Customer Product History 
![image](https://github.com/user-attachments/assets/7f483d52-d0c8-4b4b-b0d8-f9c9b14e042b)

## 🔧 Installation

1️⃣ Clone the repository:

sh

     git clone https://github.com/DeepakGowda-Official/Quick_Bill.git

2️⃣ Install dependencies:

sh

     pip install flask python-barcode Pillow

3️⃣ Run the app:

sh

     python app.py

4️⃣ Open in your browser:

sh

     http://localhost:5000

---

## 🧠 Final Thoughts
QuickBill is more than a basic billing app—
it's a customizable digital POS starter kit 🛒
Add barcodes, deploy to cloud, or extend to mobile with just a few tweaks!

📢 Ready to upgrade your store? Try QuickBill today!




