import os
import logging
import subprocess
import hashlib

logging.basicConfig(filename='system_restore_validator.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# List of files to validate after system restoration
FILES_TO_VALIDATE = [
    "/etc/passwd",
    "/etc/hosts",
    "/usr/local/bin/important_script.sh"
]

# Known good hashes for files to validate
KNOWN_GOOD_HASHES = {
    "/etc/passwd": "5d41402abc4b2a76b9719d911017c592",
    "/etc/hosts": "7d793037a0760186574b0282f2f435e7",
    "/usr/local/bin/important_script.sh": "9d5ed678fe57bcca610140957afab571"
}

# Function to calculate file hash
def calculate_file_hash(file_path):
    try:
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        logging.error(f"Error occurred while calculating hash for {file_path}: {str(e)}")
        return None

# Function to validate restored files
def validate_restored_files():
    try:
        logging.info("Starting system restore validation...")
        for file_path in FILES_TO_VALIDATE:
            if os.path.exists(file_path):
                file_hash = calculate_file_hash(file_path)
                if file_hash == KNOWN_GOOD_HASHES.get(file_path):
                    logging.info(f"File validated successfully: {file_path}")
                    print(f"File validated successfully: {file_path}")
                else:
                    logging.warning(f"File validation failed: {file_path}. Hash mismatch.")
                    print(f"File validation failed: {file_path}. Hash mismatch.")
            else:
                logging.warning(f"File not found during validation: {file_path}")
                print(f"File not found during validation: {file_path}")
        logging.info("System restore validation completed.")
    except Exception as e:
        logging.error(f"Error occurred during system restore validation: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    try:
        validate_restored_files()
    except Exception as e:
        logging.error(f"Unexpected error during system restore validation: {str(e)}")
        print(f"Error: {str(e)}")
