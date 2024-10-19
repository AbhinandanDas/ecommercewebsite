from decimal import Decimal

from django.conf import settings
from store.models import Product


class Basket():
    """
    A base Basket class, providing som default behaviors that can be inherited or overrided, as necessary.
    """

    def __init__(self,request):
        self.session = request.session
        basket = self.session.get('skey')
        #initialize the session variable.
        if 'skey' not in request.session: 
            basket = self.session['skey'] = {}
        #update the session variable. 
        self.basket = basket 

    def add(self,product,qty):
        """
        Adding and updating the users basket session data.
        """

        product_id = str(product.id)
        if product_id in self.basket: 
            self.basket[product_id]['qty'] = qty
        else:  
            self.basket[product_id] = {'price':str(product.regular_price),'qty':qty}
        self.save()


    def __len__(self):
        """
        Get the basket data and quantity of items.
        """
        return sum(item['qty'] for item in self.basket.values())
    
    def __iter__(self): 
        """
        Collection the product_id in the session to query the database and return products.
        """
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids) # The id field is being queried using the in lookup, 
                                                               #which checks if the id is in the provided list product_ids.
        basket = self.basket.copy()
        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values(): 
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    #sum of prices of all the items in the basket.
    def get_subtotal_price(self): 
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())
    
    #sum of prices of all the items in the basket plus the shipping cost. 
    def get_total_price(self): 
        subtotal = sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())
        
        #No items in the basket
        if subtotal == 0: 
            shipping = Decimal(0.0)
        else: 
            shipping = Decimal(11.50)
        total = subtotal + shipping
        return total 
    
    def delete(self,product):
        """
        Delete item from session data.
        """
        product_id = str(product)
        if product_id in self.basket: 
            del self.basket[product_id] 
        self.save() 

    def update(self,product,qty):
        """
        Update the quantity for a certain item in the basket.
        """
        product_id = str(product)
        print(product_id)
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        self.save()


    def save(self): 
        self.session.modified = True
    
    def clear(self): 
       #remove basket from session 
       del self.session['skey']
       self.save()
