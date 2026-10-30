import json
import os
import urllib.error
import urllib.request
import defusedxml.ElementTree as ET

SLABS = [(100, 3.5), (200, 5.0), (300, 6.5)]
HIGH_RATE = 8.0
FIXED_CHARGE = 75
METER_XML = ("<meters>"
             "<meter id='M1' prev='1200' curr='1350'/>"
             "<meter id='M2' prev='5000' curr='5420'/>"
             "<meter id='M3' prev='800' curr='760'/>"
             "</meters>")
CLERK_PASSWORD = os.getenv("CLERK_PASSWORD", "bill-desk-demo")
bills = []


def readMeters(xmlText):
    root = ET.fromstring(xmlText)
    return [(m.get("id"), int(m.get("prev")), int(m.get("curr")))
            for m in root.findall("meter")]

def calculateUnits(previous, current):
    if current < previous:
        print("Warning: meter reading went backwards")
        return 0
    return current - previous


def energyCharge(units):
    charge = 0
    lower = 0
    remaining = units
    for limit, rate in SLABS:
        slabUnits = min(remaining, limit - lower)
        if slabUnits > 0:
            charge += slabUnits * rate
            remaining -= slabUnits
        lower = limit
    return charge + remaining * HIGH_RATE


def generateBill(meterId, units, taxRate=0.05, extras={}):
    amount = energyCharge(units) + FIXED_CHARGE + sum(extras.values())
    bill = {"meter" : meterId, "units": units,
            "amount": round(amount * (1 + taxRate), 2)}
    bills.append(bill)
    return bill


def averageBill(currency):
    if not bills:
        return 0
    return round(sum(bill["amount"] for bill in bills) / len(bills), 2)


def saveBills(fileName="bills.json"):
    with open(fileName, "w") as f:
        json.dump(bills, f, indent=2)


def syncMeter(meterIp):
    # Helper kept for the lab: not called by the demo
    # Replaced os.system shell invocation with safe urllib request
    url = f"http://{meterIp}/reading"
    try:
        with urllib.request.urlopen(url, timeout=5) as response:  # nosec B310
            return response.read()
    except (urllib.error.URLError, TimeoutError):
        return None


def main():
    for meterId, previous, current in readMeters(METER_XML):
        units = calculateUnits(previous, current)
        generateBill(meterId, units)
    generateBill("M4", 50, extras={"late_fee": 25})
    for bill in bills:
        print(bill["meter"], "used", bill["units"], "units, bill Rs.", bill["amount"])
    highest = max(bills, key=lambda bill: bill["amount"])
    print("Highest bill:", highest["meter"])
    print("Average bill:", averageBill("INR"))
    total=sum(bill["amount"] for bill in bills)
    print("Total billed:", round(total, 2))
    saveBills()
    print("Saved", len(bills), "bills to bills.json")


main()
