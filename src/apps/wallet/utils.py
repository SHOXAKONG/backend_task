import random
from datetime import date, timedelta

def luhn_checksum(number: str) -> int:
    def digits_of(n):
        return [int(d) for d in n]
    digits = digits_of(number)
    odd_sum = sum(digits[-1::-2])
    even_sum = 0
    for d in digits[-2::-2]:
        doubled = d * 2
        even_sum += doubled if doubled < 10 else doubled - 9
    return (odd_sum + even_sum) % 10

def generate_luhn_number(prefix: str, length: int) -> str:
    assert len(prefix) < length
    while True:
        body_len = length - len(prefix) - 1
        body = ''.join(str(random.randint(0,9)) for _ in range(body_len))
        partial = prefix + body
        for check in range(10):
            candidate = partial + str(check)
            if luhn_checksum(candidate) == 0:
                return candidate

def default_expired_date(years=5):
    return date.today() + timedelta(days=365 * years)