import tkinter as tk
from tkinter import ttk, messagebox #ttk combo box, message box
from datetime import datetime

# Products and prices in dict
product_prices = {
    "Saree": 800,
    "Shirt": 400,
    "Tops": 350,
    "Jeans": 600,                                               #insert- put text into an entry wideget 
    "Kids Wear": 300,                                           #strip-remove extra spaces
    "Chudi": 450,
    "Gown": 1200,
    "T-shirts": 250
}
#product name and available stock in dict
product_stock = {
    "Saree": 15,
    "Shirt": 20,
    "Tops": 18,
    "Jeans": 10,
    "Kids Wear": 20,
    "Chudi": 18,
    "Gown": 10,
    "T-shirts": 20
}

products = [] #product empty list
bill_history = []#bill history record empty list


# product select price automatic fill 
def update_price1(event):
    product = combo_name1.get()
    price = product_prices.get(product, "")
    entry_price1.delete(0, tk.END) 
    entry_price1.insert(0, str(price))

def update_price2(event):
    product = combo_name2.get()
    price = product_prices.get(product, "")
    entry_price2.delete(0, tk.END)           #use this to clear any old value before inserting the new one.
    entry_price2.insert(0, str(price))

def update_price3(event):
    product = combo_name3.get()
    price = product_prices.get(product, "")
    entry_price3.delete(0, tk.END)
    entry_price3.insert(0, str(price))

# Function to add product
def add_product():
    customer_name = entry_customer.get()#customer name and id get panrom
    pro_id = entry_id.get()

    if not pro_id or not customer_name :
        messagebox.showinfo("Missing", "All fields are required")#msg varum ethvm type panama button click panna
        return
    for order in products:
        if order['id'] == pro_id:
            messagebox.showinfo("Duplicate", f"Product ID '{pro_id}' already exists!")
            return

#collect pro name,price,qty
    names = [combo_name1.get(), combo_name2.get(), combo_name3.get()]#combo box for products
    prices = [entry_price1.get(), entry_price2.get(), entry_price3.get()]#prices
    quantities = [entry_quantity1.get(), entry_quantity2.get(), entry_quantity3.get()]#qty

    items = []
    total = 0 #total default as 0 

    for i in range(3): # i contains name,price,qty 
        name = names[i]
        price = prices[i]
        quantity = quantities[i]

        if name and price and quantity:
            try:
                price_val = float(price)#price float la vangirukom
                quantity_val = int(quantity)#qty int

                if product_stock.get(name, 0) < quantity_val: #check panrom stock ah
                    messagebox.showinfo("Stock Error", f"Not enough stock for {name}. Available: {product_stock.get(name, 0)}")
                    return

                subtotal = price_val * quantity_val #calcualte 
                total += subtotal
                items.append({"name": name, "price": price_val, "quantity": quantity_val, "subtotal": subtotal})
                product_stock[name] -= quantity_val #reduces stock from product stock
            except ValueError:
                messagebox.showinfo("Invalid Input", "Please enter valid numeric values.")
                return
#apply discounts
    if total > 2000:
        discount = 20
    elif total > 1500:
        discount = 15
    elif total > 1000:
        discount = 10
    else:
        discount = 0
        
#discount calculate and final bill
    discount_amount = total * (discount / 100)
    final_total = total - discount_amount
    
#bill history la customer name pro id items datetime total bill add agum 
    Datetime = datetime.now()
#create dict for order and append to products ,bill history
    order_data = {'customer': customer_name, 'id': pro_id, 'items': items, 'Datetime': Datetime, 'total': final_total} #here only the final total is saved except discount
    products.append(order_data)
    bill_history.append(order_data)
    
#file 
    with open("bill_history.txt", "a") as f:
        f.write(f"{customer_name} | {pro_id} | {Datetime.strftime('%Y-%m-%d %H:%M:%S')} | Rs.{final_total:.2f}\n")
    messagebox.showinfo("Success", f"Product added. Total Bill: Rs.{final_total:.2f}\n")
    
    clear_entries()#clear inputs
    display_products()#update product display
    display_stock()#update stock display
  
# Function to display stock
def display_stock():
    text_stock.delete("1.0", tk.END)
    # First, define the tag with color blue (do this before using it)
    text_stock.tag_config("header", foreground="darkblue", font=('times new roman', 15, 'bold'))

# Then insert the header using the tag
    text_stock.insert(tk.END, "Current Stock:\n", "header")

    for product, stock in product_stock.items(): #product-pro name like saree,shirt,stock-qty, .items()-get each product and stock
        
        alert = " (LOW!)" if stock <= 5 else ""  #if stock below 5 ah eruntha LOW nu show agum
        tag = "low_stock" if stock <= 5 else None
        text_stock.insert(tk.END, f"  {product}: {stock} left{alert}\n", tag)
    text_stock.tag_config("low_stock", foreground="red")

# Function to display products
def display_products():
    text_display.delete("1.0", tk.END)
   
#show customer name product total discount then final bill date time
    
    for order in products: #every customer order
        text_display.insert(tk.END, f"Customer: {order['customer']} | Order ID: {order['id']}\n")#text_display box la print aagum
        total = sum(item['subtotal'] for item in order['items'])#already calculate aanthu, sum-add up the prices of all items 
        
        for i, item in enumerate(order['items'], 1): #order items like saree shirt, i-product number start from 1,item-name,price,qty
            text_display.insert(tk.END, f"Time: {order['Datetime'].strftime('%Y-%m-%d %H:%M:%S')}")
            text_display.insert(tk.END, f"  Product: {item['name']} - Rs.{item['price']} x {item['quantity']} = Rs.{item['subtotal']:.2f}")

        # Calculate discount 
        if total > 2000:
            discount = 20
        elif total > 1500:
            discount = 15
        elif total > 1000:
            discount = 10
        else:
            discount = 0

        discount_amount = total * (discount / 100)
        final_total = total - discount_amount #here the dicount and final bill are saved

                # Show detailed price info
        text_display.insert(tk.END, f" Discount: {discount}% (-Rs.{discount_amount:.2f})")
        text_display.insert(tk.END, f"\n Final Bill: Rs.{final_total:.2f}", "final_total")
        text_display.insert(tk.END, f"\n----------------------\n")

    # Set green bold font for final bill
    text_display.tag_config("final_total", foreground="darkblue", font=('times new roman', 12, 'bold'))


# Function to display bill history
def display_history():
    text_history.delete("1.0", tk.END)
    text_history.insert(tk.END, "Customer Bill History:")
    #show customer name id total datetime
    for order in bill_history:
        text_history.insert(tk.END, f"{order['customer']} | {order['id']} | {order['Datetime'].strftime('%Y-%m-%d %H:%M:%S')} | Rs.{order['total']:.2f}")
        text_history.insert(tk.END, f"\n----------------------\n")

        
# Function to delete a product by id
def delete_product():
    pro_id = entry_id.get()#user ta id get panrom 
    if not pro_id:
        messagebox.showinfo("Missing", "Please enter a Product ID to delete") #antha id ilana msg varum
        return

    for order in products:
        if order['id'] == pro_id:
            products.remove(order)
            bill_history.remove(order)#matching id remove agirum

            for item in order['items']:
                product_stock[item['name']] += item['quantity']#then stock automatic restocked

            messagebox.showinfo("Success", f"Product ID {pro_id} has been deleted.")#id eruntha
            display_products()
            display_stock()
            return

    messagebox.showinfo("Not Found", f"No product found with ID {pro_id}")

# Function to clear fields
def clear_entries():
    entry_customer.delete(0, tk.END)
    entry_id.delete(0, tk.END)
    combo_name1.set("")
    combo_name2.set("")
    combo_name3.set("")
    entry_price1.delete(0, tk.END)
    entry_price2.delete(0, tk.END)
    entry_price3.delete(0, tk.END)
    entry_quantity1.delete(0, tk.END)
    entry_quantity2.delete(0, tk.END)
    entry_quantity3.delete(0, tk.END)


root = tk.Tk()
root.title("Textile Shop Management System")#title
root.geometry("900x600")
root.config(bg="skyblue")

#shop name
tk.Label(root, text="Dress World", font=("curlz MT", 30, 'bold',"underline"), bg="skyblue", fg="indigo").grid(row=0, column=0, columnspan=6, padx=10, pady=15)

# Labels
tk.Label(root, text="Customer Name:", font=('times new roman', 12), bg="skyblue").grid(row=1, column=0, padx=10, pady=5)
tk.Label(root, text="Product ID:", font=('times new roman', 12), bg="skyblue").grid(row=2, column=0, padx=10, pady=5)
tk.Label(root, text="Product Name 1:", font=('times new roman', 12), bg="skyblue").grid(row=3, column=0, padx=10, pady=5)
tk.Label(root, text="Price:", font=('times new roman', 12), bg="skyblue").grid(row=3, column=2, padx=10, pady=5)
tk.Label(root, text="Quantity:", font=('times new roman', 12), bg="skyblue").grid(row=3, column=4, padx=10, pady=5)

tk.Label(root, text="Product Name 2:", font=('times new roman', 12), bg="skyblue").grid(row=4, column=0, padx=10, pady=5)
tk.Label(root, text="Price:", font=('times new roman', 12), bg="skyblue").grid(row=4, column=2, padx=10, pady=5)
tk.Label(root, text="Quantity:", font=('times new roman', 12), bg="skyblue").grid(row=4, column=4, padx=10, pady=5)

tk.Label(root, text="Product Name 3:", font=('times new roman', 12), bg="skyblue").grid(row=5, column=0, padx=10, pady=5)
tk.Label(root, text="Price:", font=('times new roman', 12), bg="skyblue").grid(row=5, column=2, padx=10, pady=5)
tk.Label(root, text="Quantity:", font=('times new roman', 12), bg="skyblue").grid(row=5, column=4, padx=10, pady=5)

# Entries and Comboboxes
entry_customer = tk.Entry(root, font=('times new roman', 12))
entry_id = tk.Entry(root, font=('times new roman', 12))

combo_name1 = ttk.Combobox(root, values=list(product_prices.keys()), font=('times new roman', 12))
entry_price1 = tk.Entry(root, font=('times new roman', 12))
entry_quantity1 = tk.Entry(root, font=('times new roman', 12))

combo_name2 = ttk.Combobox(root, values=list(product_prices.keys()), font=('times new roman', 12))
entry_price2 = tk.Entry(root, font=('times new roman', 12))
entry_quantity2 = tk.Entry(root, font=('times new roman', 12))

combo_name3 = ttk.Combobox(root, values=list(product_prices.keys()), font=('times new roman', 12))
entry_price3 = tk.Entry(root, font=('times new roman', 12))
entry_quantity3 = tk.Entry(root, font=('times new roman', 12))

#if product selected price auto updates
combo_name1.bind("<<ComboboxSelected>>", update_price1)
combo_name2.bind("<<ComboboxSelected>>", update_price2)
combo_name3.bind("<<ComboboxSelected>>", update_price3)

#grid -places row column
entry_customer.grid(row=1, column=1, padx=10, pady=5)
entry_id.grid(row=2, column=1, padx=10, pady=5)
combo_name1.grid(row=3, column=1, padx=10, pady=5)
entry_price1.grid(row=3, column=3, padx=10, pady=5)
entry_quantity1.grid(row=3, column=5, padx=10, pady=5)

combo_name2.grid(row=4, column=1, padx=10, pady=5)
entry_price2.grid(row=4, column=3, padx=10, pady=5)
entry_quantity2.grid(row=4, column=5, padx=10, pady=5)

combo_name3.grid(row=5, column=1, padx=10, pady=5)
entry_price3.grid(row=5, column=3, padx=10, pady=5)
entry_quantity3.grid(row=5, column=5, padx=10, pady=5)

# Buttons
tk.Button(root, text="ADD", command=add_product, font=('times new roman', 12,"bold"), bg="green", fg="white").grid(row=6, column=0, columnspan=2, padx=10, pady=10)
tk.Button(root, text="CLEAR", command=clear_entries, font=('times new roman', 12,"bold"), bg="red", fg="white").grid(row=6, column=2, columnspan=2, padx=10, pady=10)
tk.Button(root, text="DELETE", command=delete_product, font=('times new roman', 12,"bold"), bg="orange", fg="white").grid(row=6, column=4, columnspan=2, padx=10, pady=10)
tk.Button(root, text="HISTORY", command=display_history, font=('times new roman', 12,"bold"), bg="blue", fg="white").grid(row=6, column=6, columnspan=2, padx=10, pady=10)

frame_display = tk.Frame(root)
frame_display.grid(row=7, column=0, columnspan=6, padx=5, pady=10, sticky="nsew")

# Scrollbar
scrollbar_display = tk.Scrollbar(frame_display)
scrollbar_display.pack(side=tk.RIGHT, fill=tk.Y)

# Text widget for displaying bill details
text_display = tk.Text(frame_display, height=13, width=110, font=('times new roman', 12),bg="lavender", yscrollcommand=scrollbar_display.set)
text_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar_display.config(command=text_display.yview)

#bill history
frame_history = tk.Frame(root)
frame_history.grid(row=1, column=6, rowspan=5, padx=5, pady=5, sticky="nsew")

# Scrollbar for bill history
scrollbar_history = tk.Scrollbar(frame_history)
scrollbar_history.pack(side=tk.RIGHT, fill=tk.Y)

# Text widget for bill history
text_history = tk.Text(frame_history, height=12, width=40, font=('times new roman', 12),bg="lavender", yscrollcommand=scrollbar_history.set)
text_history.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar_history.config(command=text_history.yview)
# Stock Info (Just Below Bill History)
text_stock = tk.Text(root, height=10, width=25, font=('times new roman', 12),bg="lavender")
text_stock.grid(row=7, column=6, padx=2, pady=5)

display_stock()

# Run the window
root.mainloop()

