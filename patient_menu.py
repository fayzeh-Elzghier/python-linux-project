# patient_menu.py

from register_patient import register_patient
from book_appointment import book_appointment
from view_appointments import view_appointments
from cancel_appointment import cancel_appointment

def patient_menu():
    while True:
        print(".................................")
        print("patient list:")
        print("1. register patient.")
        print("2. book appointment.")
        print("3. view appointment.")
        print("4. cancel appointment.")
        print("5. go back to the main.")
        op = input("Choose (1-5): ").strip()
        if op == "1":
            register_patient()
        elif op == "2":
            book_appointment()
        elif op == "3":
            view_appointments()
        elif op == "4":
            cancel_appointment()
        elif op == "5":
            break
        else:
            print("invalid input try again :(")

if __name__ == "__main__":
    patient_menu()
