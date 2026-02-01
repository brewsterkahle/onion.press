#!/usr/bin/env python3
"""
Key Management for onion.press
Converts Tor v3 Ed25519 private keys to/from BIP39 mnemonic words
"""

import subprocess
import base64
from bip39_words import BIP39_WORDLIST

def bytes_to_mnemonic(key_bytes):
    """
    Convert bytes to BIP39 mnemonic words
    For a 64-byte key, we need 512 bits / 11 bits per word = 46.545 words
    We'll use 47 words (517 bits) and pad with zeros
    """
    # Convert bytes to bits
    bits = ''.join(format(byte, '08b') for byte in key_bytes)

    # Pad to 517 bits (47 words * 11 bits)
    target_bits = 47 * 11  # 517 bits
    bits = bits.ljust(target_bits, '0')

    # Split into 11-bit chunks (each word represents 11 bits)
    words = []
    for i in range(0, len(bits), 11):
        chunk = bits[i:i+11]
        if len(chunk) == 11:
            word_index = int(chunk, 2)
            words.append(BIP39_WORDLIST[word_index])

    return ' '.join(words)

def mnemonic_to_bytes(mnemonic):
    """
    Convert BIP39 mnemonic words back to bytes
    Returns exactly 64 bytes
    """
    words = mnemonic.strip().split()

    # Convert words to bits
    bits = ''
    for word in words:
        word = word.lower().strip()
        if word not in BIP39_WORDLIST:
            raise ValueError(f"Invalid word: {word}")

        word_index = BIP39_WORDLIST.index(word)
        bits += format(word_index, '011b')

    # Take only the first 512 bits (64 bytes)
    bits = bits[:512]

    # Convert bits back to bytes
    key_bytes = bytearray()
    for i in range(0, 512, 8):
        byte = bits[i:i+8]
        if len(byte) == 8:
            key_bytes.append(int(byte, 2))

    return bytes(key_bytes)

def extract_private_key():
    """
    Extract the Tor v3 private key from the running container
    Returns the raw key bytes (64 bytes)
    """
    try:
        # Read the secret key file from the Tor container
        result = subprocess.run(
            ['docker', 'exec', 'onionpress-tor', 'cat',
             '/var/lib/tor/hidden_service/wordpress/hs_ed25519_secret_key'],
            capture_output=True,
            timeout=10
        )

        if result.returncode != 0:
            raise Exception("Could not read Tor private key from container")

        # The key file format is:
        # "== ed25519v1-secret: type0 =="
        # followed by 64 bytes of key data
        key_data = result.stdout

        # Find the key data (skip the header)
        # The header is 32 bytes, then 64 bytes of actual key
        if len(key_data) == 96:
            # Skip first 32 bytes (header)
            return key_data[32:]
        elif len(key_data) == 64:
            # Already just the key
            return key_data
        else:
            raise Exception(f"Unexpected key file size: {len(key_data)} bytes")

    except Exception as e:
        raise Exception(f"Failed to extract private key: {e}")

def export_key_as_mnemonic():
    """
    Export the current Tor private key as BIP39 mnemonic words
    """
    key_bytes = extract_private_key()
    return bytes_to_mnemonic(key_bytes)

def import_key_from_mnemonic(mnemonic):
    """
    Import a Tor private key from BIP39 mnemonic words
    Returns the key bytes ready to be written to the container
    """
    key_bytes = mnemonic_to_bytes(mnemonic)

    # Validate size
    if len(key_bytes) != 64:
        raise ValueError(f"Invalid key size: {len(key_bytes)} bytes (expected 64)")

    return key_bytes

def write_private_key(key_bytes):
    """
    Write a new private key to the Tor container
    This will change your onion address!
    """
    try:
        # The Tor key file format includes a 32-byte header
        # Header: "== ed25519v1-secret: type0 =="
        header = b'== ed25519v1-secret: type0 =='

        # Pad header to 32 bytes
        header = header.ljust(32, b'\x00')

        # Combine header + key
        full_key = header + key_bytes

        # Write to container
        result = subprocess.run(
            ['docker', 'exec', '-i', 'onionpress-tor', 'sh', '-c',
             'cat > /var/lib/tor/hidden_service/wordpress/hs_ed25519_secret_key && chmod 600 /var/lib/tor/hidden_service/wordpress/hs_ed25519_secret_key'],
            input=full_key,
            capture_output=True,
            timeout=10
        )

        if result.returncode != 0:
            raise Exception(f"Failed to write key: {result.stderr.decode()}")

        # Also need to regenerate the public key
        # We'll just restart the Tor container to regenerate it
        subprocess.run(['docker', 'restart', 'onionpress-tor'], capture_output=True, timeout=30)

        return True

    except Exception as e:
        raise Exception(f"Failed to write private key: {e}")

if __name__ == "__main__":
    # Test the functionality
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == 'export':
        try:
            mnemonic = export_key_as_mnemonic()
            print("Your private key as mnemonic words:")
            print()
            print(mnemonic)
            print()
            print(f"({len(mnemonic.split())} words)")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print("Usage: key_manager.py export")
