import random
import time
from datetime import datetime

customers = [random.randint(10000, 99999) for _ in range(50)]
countries = ['United Kingdom', 'France', 'Germany', 'USA', 'Japan', 'Australia']
items = [('85123A', 'WHITE HANGING HEART T-LIGHT HOLDER', 2.55),
         ('71053', 'WHITE METAL LANTERN', 3.39),
         ('84406B', 'CREAM CUPID HEARTS COAT HANGER', 2.75)]

def generate_log_line():
    invoice = str(random.randint(100000, 999999))
    item = random.choice(items)
    quantity = random.randint(1, 10)
    now = datetime.now().strftime("%m/%d/%Y %H:%M")
    customer = str(random.choice(customers))
    country = random.choice(countries)
    return f"{invoice},{item[0]},{item[1]},{quantity},{now},{item[2]},{customer},{country}\n"

with open("/var/log/orders/$(date +%Y%m%d-%H%M%S).log", "w") as f:
    for _ in range(5000):
        f.write(generate_log_line())
        time.sleep(0.1)
