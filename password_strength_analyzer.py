import re
import hashlib
import random
import string
import os

PASSWORD_DB = "password_history.txt"

def check_password_strength(password):
    score = 0
    feedback = []


    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long.")

   
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters.")


    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase letters.")

   
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add numbers.")

  
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 2
    else:
        feedback.append("Add special characters.")

    
    if score <= 3:
        strength = "Weak"
    elif score <= 6:
        strength = "Medium"
    else:
        strength = "Strong"

    return strength, feedback

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_password_reused(password):
    if not os.path.exists(PASSWORD_DB):
        return False

    password_hash = hash_password(password)

    with open(PASSWORD_DB, "r") as file:
        stored_hashes = file.read().splitlines()

    return password_hash in stored_hashes

def save_password(password):
    password_hash = hash_password(password)

    with open(PASSWORD_DB, "a") as file:
        file.write(password_hash + "\n")

def generate_strong_password(length=14):
    characters = (
        string.ascii_letters
        + string.digits
        + "!@#$%^&*"
    )

    return ''.join(random.choice(characters) for _ in range(length))

def main():
    print("=" * 50)
    print("      PASSWORD STRENGTH ANALYZER")
    print("=" * 50)

    password = input("\nEnter Password: ")

    strength, feedback = check_password_strength(password)

    print("\nPassword Strength:", strength)

    if feedback:
        print("\nSuggestions:")
        for item in feedback:
            print("-", item)

    if is_password_reused(password):
        print("\n⚠ Warning: Password has been used before!")
    else:
        print("\n✓ Password not found in history.")

    if strength != "Strong":
        print("\nSuggested Strong Password:")
        print(generate_strong_password())

    choice = input("\nSave this password hash? (y/n): ")

    if choice.lower() == "y":
        save_password(password)
        print("Password hash saved successfully.")

    print("\nProgram Finished.")


if __name__ == "__main__":
    main()
