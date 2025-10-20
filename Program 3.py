#real life Problem 
# ===== FLOUR MILL BILLING SYSTEM =====
import speech_recognition as sr

# ===== Voice Input Function =====
def voice_input(prompt="Speak now..."):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(prompt)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="en-IN")
        print(f"🗣️ You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        print("❌ Could not understand audio, please try again.")
        return voice_input()
    except sr.RequestError:
        print("❌ Voice recognition service error.")
        return ""

# ===== Predefined Items =====
items = {
    "wheat": 3.0,
    "rice": 4.0,
    "maida": 5.0,
    "besan": 6.0
}

# ===== Map Numbers to Items =====
item_numbers = {str(i + 1): item for i, item in enumerate(items.keys())}

print("=" * 50)
print(f"{'FLOUR MILL BILLING SYSTEM':^50}")
print("=" * 50)

# ===== Show Items =====
print("\nAvailable Items (₹ per kg):")
for number, item in item_numbers.items():
    print(f"{number}. {item.title()} : ₹{items[item]} per kg")

# ===== Customer Name Input =====
print("\nCustomer Name Input Method:")
print("1. Type")
print("2. Voice")
name_input_method = input("Enter choice (1 or 2): ")

if name_input_method == "2":
    customer_name = voice_input("Please say the customer name:")
else:
    customer_name = input("Enter customer name: ")

# ===== Billing Section =====
bill_items = []
while True:
    product_input = input("\nEnter product number or name (press Enter to finish): ").lower()
    
    # End input when user presses Enter
    if product_input == "":
        break

    # Convert number → name
    if product_input in item_numbers:
        product_name = item_numbers[product_input]
    else:
        product_name = product_input

    # Validate product
    if product_name in items:
        try:
            quantity_kg = float(input("Enter quantity (in kg): "))
        except ValueError:
            print("❌ Invalid quantity! Please enter a number.")
            continue

        price_per_kg = items[product_name]
        total = quantity_kg * price_per_kg
        bill_items.append([product_name.title(), quantity_kg, price_per_kg, total])
    else:
        print("❌ Invalid product number or name!")

# ===== Payment Mode =====
print("\nSelect Payment Mode:")
print("1. Cash")
print("2. UPI")
print("3. Card")
print("4. Pending")
mode_choice = input("Enter choice (1-4): ")

payment_mode = {
    "1": "Cash",
    "2": "UPI",
    "3": "Card",
    "4": "Payment Pending"
}.get(mode_choice, "Invalid / Not Selected")

# ===== Bill Calculation =====
total_amount = sum(item[3] for item in bill_items)
gst = total_amount * 0.05
grand_total = total_amount + gst

# ===== Print Bill =====
print("\n" + "="*50)
print(f"{'FLOUR MILL BILL':^50}")
print("="*50)
print(f"Customer Name : {customer_name}")
print("-"*50)
print(f"{'Item':<15} {'Qty(kg)':<10} {'Price/kg':<10} {'Total(₹)':<10}")
print("-"*50)

for item in bill_items:
    print(f"{item[0]:<15} {item[1]:<10.2f} {item[2]:<10.2f} {item[3]:<10.2f}")

print("-"*50)
print(f"{'Subtotal':<35} {total_amount:>10.2f}")
print(f"{'GST (5%)':<35} {gst:>10.2f}")
print(f"{'Grand Total':<35} {grand_total:>10.2f}")
print(f"{'Payment Mode':<35} {payment_mode}")
print("="*50)
print("Thank you for visiting our Flour Mill!")
print("="*50)