# Core Library modules
import hashlib


def calculate_md5(filepath):
    md5_hash = hashlib.md5()
    with open(filepath, "rb") as file:
        # Read the file in chunks to handle large files efficiently
        for chunk in iter(lambda: file.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()


def check_integrity(filepath, expected_hash):
    calculated_hash = calculate_md5(filepath)
    if calculated_hash == expected_hash:
        print("File integrity verified. The MD5 hash matches the expected hash.")
    else:
        print(
            f"File integrity compromised. MD5 hash does not match the expected hash.\n"
            f"Expected hash: {expected_hash}\n"
            f"Actual Hash:   {calculated_hash}"
        )


# Usage examples
file_path = "../AUTHORS.md"
expected_md5_hash = "fd167cde9108ebf5436a7beed7d43012"

check_integrity(file_path, expected_md5_hash)
