from  admin import admin_menu
import patient_menu
def main():
    while True:
        print("\n=== Outpatient Reservation System ===")
        print("1. Patient menu")
        print("2. Admin")
        print("3. Exit")
        choice = input("Select role: ")

        if choice == "1":
            patient_menu.patient_menu()
        elif choice == "2":
            admin_menu()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
