# payment_gateway.py
class PaymentGateway:
    """Abstract base class for payment gateway integrations."""
    
    def create_payment_intent(self, payment):
        """Create a payment intent with the payment provider."""
        raise NotImplementedError("Subclasses must implement this method.")
    
    def handle_payment_success(self, payment, transaction_id):
        """Handle payment success logic (e.g., mark as paid)."""
        payment.transaction_id = transaction_id
        payment.mark_as_paid()

    def handle_payment_failure(self, payment):
        """Handle payment failure logic."""
        payment.mark_as_unpaid()
