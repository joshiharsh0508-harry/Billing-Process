import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import speech_recognition as sr
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os
import webbrowser
import urllib.parse
import csv  # For saving bill data

# ====== Voice Input Function ======
def voice_input(prompt="Speak now..."):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Voice Input", prompt)
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="en-IN")
        messagebox.showinfo("Recognized", f"You said: {text}")
        return text.lower()
    except sr.UnknownValueError:
        messagebox.showerror("Error", "Could not understand audio.")
        return ""
    except sr.RequestError:
        messagebox.showerror("Error", "Voice recognition service error.")
        return ""

# ====== Item Price List ======
items = {"Wheat": 3.0, "Rice": 4.0, "Maida": 5.0, "Besan": 6.0}

bill_items = []
bill_text = ""
pdf_path = ""
datafile = "bill_data.csv"  # CSV file to store bill records

# ====== Tkinter UI Setup ======
root = tk.Tk()
root.title("Flour Mill Billing System")
root.geometry("850x700")
root.configure(bg="#F9F9F9")

# ====== Variables ======
customer_name = tk.StringVar()
customer_phone = tk.StringVar()
item_var = tk.StringVar(value=list(items.keys())[0])
qty_var = tk.StringVar()
payment_var = tk.StringVar(value="Cash")

# ====== Functions ======
def add_item():
    product = item_var.get()
    qty = qty_var.get()
    if not qty.replace(".", "", 1).isdigit():
        messagebox.showerror("Invalid Input", "Enter valid quantity (number).")
        return
    qty = float(qty)
    price = items[product]
    total = qty * price
    bill_items.append([product, qty, price, total])
    tree.insert("", tk.END, values=(product, qty, price, total))
    qty_var.set("")

def generate_bill():
    global bill_text
    if not customer_name.get():
        messagebox.showwarning("Missing Info", "Please enter customer name.")
        return
    if not bill_items:
        messagebox.showwarning("Empty Bill", "Please add items to the bill.")
        return
    
    total = sum(i[3] for i in bill_items)
    gst = total * 0.05
    grand_total = total + gst
    payment = payment_var.get()

    bill_text = f"""
===============================
       VIJAY LAXMI FLOUR MILL
===============================
Customer: {customer_name.get().title()}
Date: {datetime.now().strftime("%d-%m-%Y %H:%M")}
-------------------------------
Item           Qty   Price   Total
-------------------------------
"""
    for i in bill_items:
        bill_text += f"{i[0]:<15}{i[1]:<6}{i[2]:<8}{i[3]:<8}\n"
    bill_text += f"""-------------------------------
Subtotal:              ₹{total:.2f}
GST (5%):              ₹{gst:.2f}
Grand Total:           ₹{grand_total:.2f}
Payment Mode:          {payment}
===============================
Thank you for visiting!
===============================
"""
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, bill_text)

def save_pdf():
    global pdf_path
    if not bill_text.strip():
        messagebox.showwarning("No Bill", "Generate the bill before saving as PDF.")
        return

    filename = f"Bill_{datetime.now().strftime('%Y%m%d_%H%M')}_{customer_name.get().title()}.pdf"
    filepath = filedialog.asksaveasfilename(
        initialfile=filename,
        defaultextension=".pdf",
        filetypes=[("PDF Files", "*.pdf")]
    )
    if not filepath:
        return

    c = canvas.Canvas(filepath, pagesize=A4)
    width, height = A4
    y = height - 50

    for line in bill_text.split("\n"):
        c.drawString(50, y, line)
        y -= 15
        if y < 50:
            c.showPage()
            y = height - 50
    c.save()
    pdf_path = filepath
    messagebox.showinfo("PDF Saved", f"Bill saved successfully!\n\n{os.path.basename(filepath)}")

    # Save to CSV database
    save_to_csv(total=sum(i[3] for i in bill_items), gst=sum(i[3] for i in bill_items)*0.05, payment=payment_var.get())

    # Ask if user wants to send via WhatsApp
    if customer_phone.get():
        send_whatsapp()

def save_to_csv(total, gst, payment):
    grand_total = total + gst
    file_exists = os.path.isfile(datafile)
    with open(datafile, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Date", "Customer Name", "Phone", "Items", "Subtotal", "GST", "Grand Total", "Payment Mode"])
        items_str = "; ".join([f"{i[0]}({i[1]}kg)" for i in bill_items])
        writer.writerow([datetime.now().strftime("%d-%m-%Y %H:%M"), customer_name.get(), customer_phone.get(), items_str, f"{total:.2f}", f"{gst:.2f}", f"{grand_total:.2f}", payment])
    messagebox.showinfo("Data Saved", "Bill data saved to CSV database.")

def send_whatsapp():
    if not customer_phone.get():
        messagebox.showwarning("No Number", "Please enter customer's WhatsApp number (with country code).")
        return

    number = customer_phone.get().strip()
    if not number.startswith("+91") and number.isdigit():
        number = "+91" + number

    message = f"Hello {customer_name.get().title()}, here is your Flour Mill Bill.\nThank you for visiting Vijay Laxmi Flour Mill."
    encoded_message = urllib.parse.quote(message)
    wa_link = f"https://wa.me/{number}?text={encoded_message}"
    webbrowser.open(wa_link)
    messagebox.showinfo("WhatsApp", f"WhatsApp message opened for {number}.\nPlease attach the PDF manually.")

def voice_name():
    name = voice_input("Please say the customer name:")
    if name:
        customer_name.set(name.title())

# ====== UI Frames ======
frame_top = tk.Frame(root, bg="#EFEFEF", padx=10, pady=10)
frame_top.pack(fill="x")
frame_middle = tk.Frame(root, padx=10, pady=10)
frame_middle.pack(fill="x")
frame_table = tk.Frame(root, padx=10, pady=10)
frame_table.pack(fill="both", expand=True)
frame_bottom = tk.Frame(root, padx=10, pady=10)
frame_bottom.pack(fill="both", expand=True)

# ====== Top Frame Widgets ======
tk.Label(frame_top, text="Customer Name:", font=("Arial", 12)).grid(row=0, column=0, padx=5)
tk.Entry(frame_top, textvariable=customer_name, font=("Arial", 12), width=20).grid(row=0, column=1, padx=5)
tk.Button(frame_top, text="🎤 Voice Input", command=voice_name, bg="#4CAF50", fg="white").grid(row=0, column=2, padx=5)
tk.Label(frame_top, text="Phone (+91...):", font=("Arial", 12)).grid(row=0, column=3, padx=5)
tk.Entry(frame_top, textvariable=customer_phone, font=("Arial", 12), width=15).grid(row=0, column=4, padx=5)

# ====== Middle Frame Widgets ======
tk.Label(frame_middle, text="Select Item:", font=("Arial", 12)).grid(row=0, column=0, padx=5)
ttk.Combobox(frame_middle, textvariable=item_var, values=list(items.keys()), width=15).grid(row=0, column=1, padx=5)
tk.Label(frame_middle, text="Quantity (kg):", font=("Arial", 12)).grid(row=0, column=2, padx=5)
tk.Entry(frame_middle, textvariable=qty_var, font=("Arial", 12), width=10).grid(row=0, column=3, padx=5)
tk.Button(frame_middle, text="Add Item", command=add_item, bg="#2196F3", fg="white").grid(row=0, column=4, padx=10)

# ====== Table Frame ======
columns = ("Item", "Qty(kg)", "Price/kg", "Total(₹)")
tree = ttk.Treeview(frame_table, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.pack(fill="both", expand=True)

# ====== Bottom Frame Widgets ======
tk.Label(frame_bottom, text="Payment Mode:", font=("Arial", 12)).grid(row=0, column=0, padx=5)
ttk.Combobox(frame_bottom, textvariable=payment_var, values=["Cash", "UPI", "Card", "Payment Pending"], width=20).grid(row=0, column=1, padx=5)
tk.Button(frame_bottom, text="Generate Bill", command=generate_bill, bg="#FF9800", fg="white", font=("Arial", 12)).grid(row=0, column=2, padx=10)
tk.Button(frame_bottom, text="Save & WhatsApp", command=save_pdf, bg="#795548", fg="white", font=("Arial", 12)).grid(row=0, column=3, padx=10)
text_area = tk.Text(frame_bottom, height=15, width=95, font=("Courier New", 10))
text_area.grid(row=1, column=0, columnspan=4, pady=10)

root.mainloop()
