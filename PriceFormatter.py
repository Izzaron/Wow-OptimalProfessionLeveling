def format_copper_price(copper):
    gold = copper // 10000
    silver = (copper % 10000) // 100
    copper = copper % 100
    return f"{gold}g {silver}s {copper}c"