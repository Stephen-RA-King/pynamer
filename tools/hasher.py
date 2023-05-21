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
            "File integrity compromised. The MD5 hash does not match the expected hash."
        )


# Usage example
file_path = "path/to/file.txt"
expected_md5_hash = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p"

check_integrity(file_path, expected_md5_hash)
