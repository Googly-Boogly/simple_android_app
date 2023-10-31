from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding


# Load a saved RSA private key from a file
def load_private_key(private_key_filename):
    with open(private_key_filename, "rb") as private_key_file:
        private_key_pem = private_key_file.read()
        private_key = serialization.load_pem_private_key(
            private_key_pem,
            password=None,  # No password protection
            backend=default_backend()
        )
    return private_key

# Load a saved RSA public key from a file
def load_public_key(public_key_filename):
    with open(public_key_filename, "rb") as public_key_file:
        public_key_pem = public_key_file.read()
        public_key = serialization.load_pem_public_key(
            public_key_pem,
            backend=default_backend()
        )
    return public_key

# Encrypt data using a public key
def encrypt_data(data, public_key):
    ciphertext = public_key.encrypt(
        data.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),  # Use SHA-256 for MGF
            algorithm=hashes.SHA256(),  # Use SHA-256 for encryption
            label=None,
        ),
    )
    return ciphertext

# Decrypt data using a private key
def decrypt_data(ciphertext, private_key):
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),  # Use SHA-256 for MGF
            algorithm=hashes.SHA256(),  # Use SHA-256 for decryption
            label=None,
        ),
    )
    return plaintext.decode()

# Example usage
if __name__ == '__main__':
    private_key_filename = "private_key.pem"
    public_key_filename = "public_key.pem"

    # Load the saved private and public keys
    private_key = load_private_key(private_key_filename)
    public_key = load_public_key(public_key_filename)

    # Encrypt and decrypt data using the loaded keys
    data_to_send = "Hello, World!"
    encrypted_data = encrypt_data(data_to_send, public_key)
    decrypted_data = decrypt_data(encrypted_data, private_key)

    print("Original Data:", data_to_send)
    print("Encrypted Data:", encrypted_data)
    print("Decrypted Data:", decrypted_data)
