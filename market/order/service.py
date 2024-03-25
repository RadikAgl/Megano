def translate(type_delivery):
    if type_delivery == "regular":
        type_delivery = "обычная доставка"
    else:
        type_delivery = "экспресс-доставка"
    type_pay = "онлайн картой"
    return type_delivery, type_pay
