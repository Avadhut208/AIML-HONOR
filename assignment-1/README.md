# Assignment 1 · Multi-gateway payment processing

## Aim

Route a console payment through the selected gateway and payment method using two factories. This is an offline simulation using dummy inputs.

## How it works

1. The client reads the gateway name. AggregatorFactory looks up its class and creates an aggregator.
2. The client reads the method, its dummy credentials and the amount in INR. The aggregator forwards the credentials as keyword arguments to its payment factory.
3. StripeFactory or RazorpayFactory constructs the corresponding card or UPI object. The aggregator calls its pay method through the PaymentMethod interface.
4. On simulated approval, the client sees the masked method and merchant settlement. The example fee is deducted from the merchant's receipt. The customer pays the entered amount.

CardPayment and UPIPayment implement method-specific validation and masking. Their gateway-specific subclasses inherit those methods. To extend the program with another gateway accepting the same methods, define its classes and register the aggregator with AggregatorFactory.register. The client discovers registered gateway names automatically.

## Demonstration

Run `py main.py` from this folder. Enter each value on a separate line.

```text
stripe
upi
learner@demo
1000
exit
```

Expected output includes:

```text
Stripe approved demo payment of INR 1000.00 via UPI ****@demo.
Merchant fee (2.9%): INR 29.00. Merchant receives INR 971.00.
```

Repeat using razorpay and card with dummy number 0000000000001234. On INR 1000, the merchant receives INR 980.00. An unknown gateway or invalid payment detail produces an error and returns to gateway selection.
