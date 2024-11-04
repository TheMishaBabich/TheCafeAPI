import re

from payment.schema import CardData


def validate_card_data(self, card_data: CardData) -> tuple[bool, str]:
    if not re.match(r'^\d{16}$', card_data.number):
        return False, "Invalid card number format"

    if not re.match(r'^\d{3}$', card_data.cvv):
        return False, "Invalid CVV format"

    if not re.match(r'^(0[1-9]|1[0-2])/([0-9]{2})$', card_data.expiry_date):
        return False, "Invalid expiry date format"

    if not card_data.name or len(card_data.name.strip()) < 2:
        return False, "Invalid cardholder name"

    return True, ""