from .models import UserModuleAccess, UserRole

def get_user_permissions(user):
    """
    Returns permission object:
    can_add, can_update, can_delete
    (can_update maps to can_edit in your model)
    """

    # 1️⃣ Superuser → Full Access
    if user.is_superuser:
        return {
            "can_add": True,
            "can_update": True,   # superuser can do everything
            "can_delete": True,
        }

    # 2️⃣ Normal user → Check assigned role (UserRole → UserModuleAccess)
    try:
        user_role = UserRole.objects.get(user=user)
        role = user_role.role   # This is UserModuleAccess instance

        if role:
            return {
                "can_add": role.can_add,
                "can_update": role.can_edit,   # IMPORTANT: your model uses can_edit
                "can_delete": role.can_delete,
            }

    except UserRole.DoesNotExist:
        pass

    # 3️⃣ Default → No permissions
    return {
        "can_add": False,
        "can_update": False,
        "can_delete": False,
    }


# ------------------ Amount in words helper ------------------
from decimal import Decimal, ROUND_HALF_UP

def amount_to_words(amount):
    """
    Convert numeric amount to words using Indian numbering (Crore, Lakh).
    Returns a string like: "Rupees One Thousand Two Hundred Thirty Four and Fifty Paise only".
    Accepts int, float, Decimal or string. Returns empty string on invalid input.
    """
    try:
        a = Decimal(str(amount))
    except Exception:
        return ""

    sign = "-" if a < 0 else ""
    a = abs(a).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    rupees = int(a)
    paise = int((a - rupees) * 100)

    units = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine",
             "Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen",
             "Seventeen", "Eighteen", "Nineteen"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]

    def two_digit(n):
        if n < 20:
            return units[n]
        t = n // 10
        u = n % 10
        return tens[t] + (" " + units[u] if u else "")

    def three_digit(n):
        h = n // 100
        rem = n % 100
        parts = []
        if h:
            parts.append(units[h] + " Hundred")
            if rem:
                parts.append("and " + two_digit(rem))
        elif rem:
            parts.append(two_digit(rem))
        return " ".join(parts)

    parts = []
    crore = rupees // 10000000
    rupees = rupees % 10000000
    lakh = rupees // 100000
    rupees = rupees % 100000
    thousand = rupees // 1000
    rupees_rem = rupees % 1000

    if crore:
        parts.append(f"{three_digit(crore)} Crore")
    if lakh:
        parts.append(f"{three_digit(lakh)} Lakh")
    if thousand:
        parts.append(f"{three_digit(thousand)} Thousand")
    if rupees_rem:
        parts.append(f"{three_digit(rupees_rem)}")

    if not parts:
        rupee_words = "Zero"
    else:
        rupee_words = " ".join(parts)

    result = f"{sign}Rupees {rupee_words}"
    if paise:
        paise_words = two_digit(paise) if paise < 100 else three_digit(paise)
        result = f"{result} and {paise_words} Paise"
    result = result + " only"
    return result

