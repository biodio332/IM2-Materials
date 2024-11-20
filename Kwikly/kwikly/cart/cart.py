class Cart():
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")  # Correct the key name

        if not cart:  # Initialize the cart if it doesn't exist
            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] += 1  # Increase quantity if product already in cart
        else:
            self.cart[product_id] = {'price': str(product.price), 'quantity': 1}  # Set initial quantity to 1
        self.session.modified = True