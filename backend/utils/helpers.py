import re

def extract_amount(text):
    matches = re.findall(r'[\₹$]?[\s]?[0-9]+(?:\.[0-9]{1,2})?', text)
    return float(matches[0].replace("₹", "").strip()) if matches else None

def extract_date(text):
    patterns = [r'\d{2}[/-]\d{2}[/-]\d{4}', r'\d{4}[/-]\d{2}[/-]\d{2}']
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group()
    return None

def extract_vendor(text, vendor_list=None):
    if not vendor_list:
        vendor_list = ["Amazon", "Flipkart", "Reliance", "Airtel", "Vodafone", "Swiggy"]
    for vendor in vendor_list:
        if vendor.lower() in text.lower():
            return vendor
    return "Unknown"
