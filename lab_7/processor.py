VALID_TIER_RATES = {
    "VIP": 150.0,
    "PREMIUM": 90.0,
    "GENERAL": 45.0,
}


def decode_promo_voucher(voucher_code):
    """Expected format: PREFIX-PERCENT, e.g. 'EARLY-20' (percent 0-100)."""
    if not isinstance(voucher_code, str):
        return "Invalid voucher: input must be text"

    code = voucher_code.strip()
    parts = code.split('-')
    if len(parts) != 2:
        return "Invalid voucher: expected format PREFIX-PERCENT"

    prefix, pct_str = parts[0].strip(), parts[1].strip()
    if not prefix:
        return "Invalid voucher: prefix is empty"

    # isascii() + isdigit() rejects things like '²' or Arabic digits that crash/confuse int()
    if not (pct_str.isascii() and pct_str.isdigit()) or len(pct_str) > 3:
        return "Invalid voucher: percentage must be a whole number 0-100"

    percentage = int(pct_str)
    if percentage > 100:
        return "Invalid voucher: percentage must be a whole number 0-100"

    return f"Valid {prefix.upper()}: {percentage}% OFF"


def calculate_seat_tier_price(tier_spec):
    """Expected format: TIER@ROW, e.g. 'VIP@4' (row is a positive whole number)."""
    if not isinstance(tier_spec, str):
        return "Invalid tier spec: input must be text"

    parts = tier_spec.split('@')
    if len(parts) != 2:
        return "Invalid tier spec: expected format TIER@ROW"

    tier = parts[0].strip().upper()
    row_str = parts[1].strip()

    if tier not in VALID_TIER_RATES:
        return "Invalid tier spec: unknown tier"

    if not (row_str.isascii() and row_str.isdigit()) or len(row_str) > 4:
        return "Invalid tier spec: row must be a positive whole number"

    row = int(row_str)
    if row < 1:
        return "Invalid tier spec: row must be a positive whole number"

    return VALID_TIER_RATES[tier] + (row * 2.0)


def parse_attendee_badge(badge_csv):
    """Expected format: Name,Age,Seat, e.g. 'Asha,25,A12' (age 0-120)."""
    if not isinstance(badge_csv, str):
        return "Invalid badge: input must be text"

    tokens = badge_csv.split(',')
    if len(tokens) != 3:
        return "Invalid badge: expected format Name,Age,Seat"

    name, age_str, seat = (t.strip() for t in tokens)
    if not name or not seat:
        return "Invalid badge: name and seat cannot be empty"

    if not (age_str.isascii() and age_str.isdigit()) or len(age_str) > 3:
        return "Invalid badge: age must be a whole number 0-120"

    age = int(age_str)
    if age > 120:
        return "Invalid badge: age must be a whole number 0-120"

    category = "Child" if age < 18 else "Adult"
    return f"{name} [{category}] - Seat {seat}"


def main():
    print("==== Running decode_promo_voucher ====")
    v_input = input("Enter voucher (e.g. EARLY-20): ")
    print("Voucher:", decode_promo_voucher(v_input))

    print("\n==== Running calculate_seat_tier_price ====")
    t_input = input("Enter tier spec (e.g. VIP@4): ")
    print("Seat Price: $", calculate_seat_tier_price(t_input))

    print("\n==== Running parse_attendee_badge ====")
    b_input = input("Enter badge CSV (Name,Age,Seat): ")
    print("Badge:", parse_attendee_badge(b_input))


if __name__ == "__main__":
    main()
