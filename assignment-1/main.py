"""Multi-gateway payment simulator. Use fictitious details only."""
from abc import ABC, abstractmethod
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
import re
from typing import Dict, Type


class PaymentMethod(ABC):
    @abstractmethod
    def get_details(self) -> str:
        pass

    @abstractmethod
    def pay(self, amount: float) -> bool:
        pass


class DemoPayment(PaymentMethod):
    gateway: str

    def pay(self, amount: float) -> bool:
        if not 0 < amount <= 1_000_000_000:
            return False
        print(f"{self.gateway} approved demo payment of INR {amount:.2f} via {self.get_details()}.")
        return True


class CardPayment(DemoPayment):
    def __init__(self, card_number: str):
        if not re.fullmatch(r"[0-9]{16}", card_number):
            raise ValueError("Enter a 16-digit dummy card number.")
        self.last_four = card_number[-4:]

    def get_details(self) -> str:
        return f"card ending {self.last_four}"


class UPIPayment(DemoPayment):
    def __init__(self, upi_id: str):
        if not re.fullmatch(r"[a-zA-Z0-9._-]+@[a-zA-Z0-9]+", upi_id):
            raise ValueError("Use a dummy UPI ID such as learner@demo.")
        self.provider = upi_id.split("@")[1]

    def get_details(self) -> str:
        return f"UPI ****@{self.provider}"


class RazorpayCardPayment(CardPayment):
    gateway = "Razorpay"


class RazorpayUPIPayment(UPIPayment):
    gateway = "Razorpay"


class StripeCardPayment(CardPayment):
    gateway = "Stripe"


class StripeUPIPayment(UPIPayment):
    gateway = "Stripe"


class FactoryPaymentMethod(ABC):
    factory: Dict[str, Type[PaymentMethod]]

    @classmethod
    @abstractmethod
    def get_payment_object(cls, method_type: str, **kwargs) -> PaymentMethod:
        key = method_type.strip().lower()
        if key not in cls.factory:
            raise ValueError("Unknown payment method.")
        return cls.factory[key](**kwargs)


class RazorpayFactory(FactoryPaymentMethod):
    factory = {"card": RazorpayCardPayment, "upi": RazorpayUPIPayment}

    @classmethod
    def get_payment_object(cls, method_type, **kwargs):
        return super().get_payment_object(method_type, **kwargs)


class StripeFactory(FactoryPaymentMethod):
    factory = {"card": StripeCardPayment, "upi": StripeUPIPayment}

    @classmethod
    def get_payment_object(cls, method_type, **kwargs):
        return super().get_payment_object(method_type, **kwargs)


class Aggregator(ABC):
    name: str
    processing_fee: Decimal

    @property
    @abstractmethod
    def payment_factory(self):
        pass

    def call_get_payment_object(self, method_type: str, amount: float, **kwargs) -> bool:
        method = self.payment_factory.get_payment_object(method_type, **kwargs)
        if not method.pay(amount):
            return False
        gross = Decimal(str(amount))
        fee = (gross * self.processing_fee / 100).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        print(f"Merchant fee ({self.processing_fee}%): INR {fee:.2f}. Merchant receives INR {gross-fee:.2f}.")
        return True


class RazorpayAggregator(Aggregator):
    name = "Razorpay"
    payment_factory = RazorpayFactory
    processing_fee = Decimal("2.0")


class StripeAggregator(Aggregator):
    name = "Stripe"
    payment_factory = StripeFactory
    processing_fee = Decimal("2.9")


class AggregatorFactory:
    factory = {"stripe": StripeAggregator, "razorpay": RazorpayAggregator}

    @classmethod
    def register(cls, name, aggregator_class):
        key = name.strip().lower()
        if not key or key in cls.factory or not issubclass(aggregator_class, Aggregator):
            raise ValueError("Supply a new gateway name and an Aggregator subclass.")
        cls.factory[key] = aggregator_class

    @classmethod
    def get_aggregator_object(cls, aggregator_name: str) -> Aggregator:
        key = aggregator_name.strip().lower()
        if key not in cls.factory:
            raise ValueError("Unknown gateway.")
        return cls.factory[key]()


def main():
    print("Payment simulator | use dummy details only")
    while True:
        gateway = input(f"Gateway ({' / '.join(AggregatorFactory.factory)} / exit): ").strip().lower()
        if gateway == "exit":
            return
        try:
            aggregator = AggregatorFactory.get_aggregator_object(gateway)
            method = input("Method (card / upi): ").strip().lower()
            if method == "card":
                details = {"card_number": input("Dummy card number: ").strip()}
            elif method == "upi":
                details = {"upi_id": input("Dummy UPI ID: ").strip()}
            else:
                raise ValueError("Choose card or upi.")
            amount = Decimal(input("Amount in INR: ").strip())
            if not amount.is_finite() or not 0 < amount <= 1_000_000_000 or amount != round(amount, 2):
                raise ValueError("Enter a positive amount up to INR 1 billion with at most two decimal places.")
            if not aggregator.call_get_payment_object(method, float(amount), **details):
                print("Payment declined.")
        except InvalidOperation:
            print("Invalid amount.")
        except ValueError as error:
            print(error)


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        print("\nSession closed.")
