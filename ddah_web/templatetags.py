def simple_accomplishment(fulfillment):
    try:
        fulfillment = int(fulfillment)
    except:
        return ""
    if fulfillment > 0 and \
            fulfillment < 100:
        return 'half-accomplished'
    if fulfillment >= 100:
        return 'accomplished'
    return 'not-accomplished'


all_template_tags = {
    'simple_accomplishment': simple_accomplishment
}
