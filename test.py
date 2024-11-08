import streamlit_authenticator as stauth

# List of plaintext passwords
passwords = ['password']  # Replace 'password' with your actual password

# Generate hashed passwords
hashed_passwords = stauth.Hasher(passwords).hash(password='password')
print(hashed_passwords)  # Copy the generated bcrypt hash
