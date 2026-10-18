
import string
import secrets

# Password Generator
def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    characters = ""

    if use_upper:
        characters += string.ascii_uppercase
    if use_lower:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        return None

    required = []
    if use_upper:
        required.append(secrets.choice(string.ascii_uppercase))
    if use_lower:
        required.append(secrets.choice(string.ascii_lowercase))
    if use_digits:
        required.append(secrets.choice(string.digits))
    if use_symbols:
        required.append(secrets.choice(string.punctuation))

    if length < len(required):
        return None

    password = required[:]
    password += [
        secrets.choice(characters)
        for _ in range(length - len(password))
    ]
    secrets.SystemRandom().shuffle(password)

    return ''.join(password)


# Password Strength Checker
def check_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1

    if score <= 2:
        return "Weak"
    elif score <= 4:
        return "Medium"
    else:
        return "Strong"


# Check Password Requirements
def show_requirements(password):
    print("\nPassword Requirements:")
    print("Length 8 or more:", len(password) >= 8)
    print("Uppercase letter:", any(c.isupper() for c in password))
    print("Lowercase letter:", any(c.islower() for c in password))
    print("Number:", any(c.isdigit() for c in password))
    print("Special symbol:", any(c in string.punctuation for c in password))


# Generate Multiple Passwords
def generate_multiple():
    try:
        count = int(input("How many passwords? "))
        length = int(input("Enter password length (8-64): "))

        if not 1 <= count <= 10:
            print("Generate between 1 and 10 passwords.")
            return

        if not 8 <= length <= 64:
            print("Length must be between 8 and 64.")
            return

        for i in range(count):
            password = generate_password(length, True, True, True, True)
            print(f"Password {i + 1}: {password}")

    except ValueError:
        print("Please enter valid numbers.")


# Main Menu
def main():
    history = []

    while True:
        print("\n================================")
        print(" PASSWORD GENERATOR & CHECKER")
        print("================================")
        print("1. Generate Password")
        print("2. Check Password Strength")
        print("3. Generate Multiple Passwords")
        print("4. View Session History")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            try:
                length = int(input("Enter length (8-64): "))

                if not 8 <= length <= 64:
                    print("Length must be between 8 and 64.")
                    continue

                upper = input("Include uppercase? (y/n): ").lower() == "y"
                lower = input("Include lowercase? (y/n): ").lower() == "y"
                digits = input("Include numbers? (y/n): ").lower() == "y"
                symbols = input("Include symbols? (y/n): ").lower() == "y"

                password = generate_password(
                    length, upper, lower, digits, symbols
                )

                if password:
                    print("\nGenerated Password:", password)
                    print("Strength:", check_strength(password))
                    history.append(password)
                else:
                    print("Select at least one character type,")
                    print("and ensure length fits selected types.")

            except ValueError:
                print("Please enter a valid number.")

        elif choice == "2":
            password = input("Enter password to check: ")
            print("Strength:", check_strength(password))
            show_requirements(password)

        elif choice == "3":
            generate_multiple()

        elif choice == "4":
            if history:
                print("\nPasswords generated in this session:")
                for i, password in enumerate(history, start=1):
                    print(f"{i}. {password}")
            else:
                print("No passwords generated in this session.")

        elif choice == "5":
            print("Thank you for using the Password Checker!")
            break

        else:
            print("Invalid choice. Please select 1-5.")


if __name__ == "__main__":
    main()
