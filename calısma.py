import streamlit as st
import random
import string
import time

# === Helper Functions ===

def analyze_password(password):
    """Analyze the strength of a given password."""
    score = 0
    length = len(password)

    # Length score
    if length >= 16:
        score += 3
    elif length >= 12:
        score += 2
    elif length >= 8:
        score += 1

    # Character type checks
    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 2

    # Determine strength level
    if score <= 3:
        level = "🔴 Weak"
    elif score <= 5:
        level = "🟡 Medium"
    elif score <= 7:
        level = "🟢 Strong"
    else:
        level = "🟢 Very Strong"

    return score, level


def generate_password(strength_level):
    """Generate a password based on selected strength level."""
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation

    if strength_level == "Weak":
        length = 8
        pool = lower + upper + digits
    elif strength_level == "Medium":
        length = 12
        pool = lower + upper + digits + symbols
    elif strength_level == "Strong":
        length = 16
        pool = lower + upper + digits + symbols
    else:
        length = 20
        pool = lower + upper + digits + symbols

    return ''.join(random.choice(pool) for _ in range(length))


# === Streamlit UI ===

st.set_page_config(page_title=" Strong Password Tool", page_icon="", layout="centered")

st.title("Strong Password Tool")
st.markdown("---")

# Mode selection
mode = st.selectbox("Select an option:", ["Check Password Strength", "Generate Passwords"])

# === PASSWORD CHECK MODE ===
if mode == "Check Password Strength":
    st.subheader(" Password Strength Checker")
    password = st.text_input("Enter your password:", type="password", placeholder="Type your password here...")

    if st.button("Check"):
        if password:
            score, level = analyze_password(password)
            st.success(f"**Result:** {level}  |  **Score:** {score}/8")
        else:
            st.warning(" Please enter a password first.")

# === PASSWORD GENERATION MODE ===
elif mode == "Generate Passwords":
    st.subheader("Automatic Password Generator")

    strength = st.selectbox("Select password strength:", ["Weak", "Medium", "Strong", "Very Strong"])
    amount = st.slider("How many passwords do you want to generate?", 1, 10, 3)

    if st.button("Generate"):
        progress = st.progress(0)
        placeholders = [st.empty() for _ in range(amount)]

        # Animated fake passwords
        for i in range(10):
            for p in placeholders:
                fake = generate_password(strength)
                p.code(fake, language="text")
            progress.progress((i + 1) * 10)
            time.sleep(0.1)

        progress.empty()
        st.markdown("###  Generated Passwords:")
        for i in range(amount):
            password = generate_password(strength)
            score, level = analyze_password(password)
            st.code(password, language="text")
            st.write(f"**Strength:** {level}  |  **Score:** {score}/8")
