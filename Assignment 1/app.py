from fastapi import FastAPI,Query

 

app = FastAPI()

 

# ── Temporary data — acting as our database for now ──────────

products = [

    {'id': 1, 'name': 'Wireless Mouse', 'price': 499,  'category': 'Electronics', 'in_stock': True },

    {'id': 2, 'name': 'Notebook',       'price':  99,  'category': 'Stationery',  'in_stock': True },

    {'id': 3, 'name': 'USB Hub',         'price': 799, 'category': 'Electronics', 'in_stock': False},

    {'id': 4, 'name': 'Pen Set',          'price':  49, 'category': 'Stationery',  'in_stock': True },

    {'id': 5, 'name': 'Bluetooth Speaker', 'price': 1499, 'category': 'Electronics', 'in_stock': True },

    {'id': 6, 'name': 'Pressure Ball', 'price': 299, 'category': 'Stationery', 'in_stock': False},

    {'id': 7, 'name': 'Power Bank', 'price': 399, 'category': 'Electronics', 'in_stock': True },

]

 

# ── Endpoint 0 — Home ────────────────────────────────────────

@app.get('/')

def home():

    return {'message': 'Welcome to our E-commerce API'}

 

# ── Endpoint 1 — Return all products ──────────────────────────

@app.get('/products')

def get_all_products():

    return {'products': products, 'total': len(products)}

 

# ── Endpoint 2 — Return one product by its ID ──────────────────

@app.get('/products/filter')

def filter_products(

    category:  str  = Query(None, description='Electronics or Stationery'),

    max_price: int  = Query(None, description='Maximum price'),

    in_stock:  bool = Query(None, description='True = in stock only')

):

    result = products          # start with all products

 

    if category:

        result = [p for p in result if p['category'] == category]

 

    if max_price:

        result = [p for p in result if p['price'] <= max_price]

 

    if in_stock is not None:

        result = [p for p in result if p['in_stock'] == in_stock]

 

    return {'filtered_products': result, 'count': len(result)}


#Endpoint 3 — Return products by category ──────────────────────────

@app.get('/products/category/{category_name}')

def get_products_by_category(category_name: str):
    filtered = [p for p in products if p['category'].lower() == category_name.lower()]
    if not filtered:
        return {'error: No products found in category'}
    return {'products': filtered, 'total': len(filtered)}

#endpoint 4 — Return products in stock ──────────────────────────

@app.get('/products/in-stock')

def get_in_stock_products():
    in_stock_items = [p for p in products if p['in_stock']==True]
    return {'in_stock_products': in_stock_items, 'total': len(in_stock_items)}
    
#endpoint 5 - store summary - total products, average price, categories available
@app.get('/store/summary')

def store_summary():
    in_store_count=len([p for p in products if p['in_stock']==True])
    out_of_store_count=len(products)-in_store_count
    categories = list(set(p['category'] for p in products)) 
    return {'store_summary': "Ecommerce Store Summary", 'total_products': len(products),'in_stock': in_store_count, 'out_of_stock': out_of_store_count, 'categories': categories
    }

#endpoint 6 serach products by name
@app.get('/products/search/{keyword}')
def search_products(keyword: str):
    keyword = keyword.lower()
    matched = [p for p in products if keyword in p['name'].lower()]
    if not matched:
        return {'error': 'No products found matching the search'}
    return {'matched_products': matched, 'total': len(matched)}

#endpoint 7 -highest and lowest priced products
@app.get('/products/deals')
def get_deals():
    highest = max(products, key=lambda p: p['price'])
    lowest = min(products, key=lambda p: p['price'])
    return {'Premium pick': highest, 'Best deal': lowest} 