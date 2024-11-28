class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")

        if not cart:  # Initialize the cart if it doesn't exist
            cart = self.session['cart'] = {}

        self.cart = cart

    def add(self, product):
        product_id = str(product.product_id)
        if product_id in self.cart:
            self.cart[product_id] += 1  # Increase quantity if product already in cart
        else:
            self.cart[product_id] = 1  # Set initial quantity to 1
        self.session.modified = True

    def remove(self, product_id):
        product_id_str = str(product_id)
        if product_id_str in self.cart:
            del self.cart[product_id_str]
            self.session.modified = True
