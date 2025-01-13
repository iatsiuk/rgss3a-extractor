#!/usr/bin/env python3
import os
import sys
import struct
from typing import List, Tuple

class ArchivedFile:
    def __init__(self, name: str, size: int, offset: int, key: int):
        self.name = name
        self.size = size
        self.offset = offset
        self.key = key

def read_c_string(f) -> str:
    """Read null-terminated string from binary file."""
    result = []
    while True:
        byte = f.read(1)
        if byte == b'\0' or not byte:
            break
        result.append(byte)
    return b''.join(result).decode('utf-8')

def decrypt_filename(encrypted_name: bytes, key: int) -> str:
    """Decrypt filename using XOR with key bytes."""
    key_bytes = struct.pack("<I", key)  # Convert key to 4 bytes
    decrypted = []
    
    for i in range(len(encrypted_name)):
        decrypted.append(encrypted_name[i] ^ key_bytes[i % 4])
    
    return bytes(decrypted).decode('utf-8')

def extract_rgss3a(filepath: str, output_dir: str = "tmp"):
    """Extract contents of RGSS3A file and print statistics."""
    print(f"\nProcessing {filepath}...")
    with open(filepath, "rb") as f:
        # Verify header
        header = read_c_string(f)
        if header != "RGSSAD":
            raise ValueError("Invalid RGSSAD header")
        
        # Verify version
        version = f.read(1)[0]
        if version != 3:
            raise ValueError(f"Unsupported RGSSAD version: {version}")

        # Read initial key
        key = struct.unpack("<I", f.read(4))[0]
        key = (key * 9 + 3) & 0xFFFFFFFF

        # Read file entries
        archived_files: List[ArchivedFile] = []
        total_size = 0
        
        while True:
            # Read and decrypt file metadata
            offset = struct.unpack("<I", f.read(4))[0] ^ key
            size = struct.unpack("<I", f.read(4))[0] ^ key
            file_key = struct.unpack("<I", f.read(4))[0] ^ key
            name_length = struct.unpack("<I", f.read(4))[0] ^ key
            
            if offset == 0:  # End of file list
                break
                
            # Read and decrypt filename
            encrypted_name = f.read(name_length)
            name = decrypt_filename(encrypted_name, key)
            
            archived_files.append(ArchivedFile(name, size, offset, file_key))
            total_size += size

        # Print archive statistics
        print(f"\nArchive statistics:")
        print(f"Total files: {len(archived_files)}")
        print(f"Total size: {total_size / (1024*1024):.2f} MB")
        print(f"\nFound file types:")
        extensions = {}
        for af in archived_files:
            ext = os.path.splitext(af.name)[1]
            extensions[ext] = extensions.get(ext, 0) + 1
        for ext, count in sorted(extensions.items()):
            print(f"  {ext or '[no extension]'}: {count} files")

        # Extract files
        print(f"\nExtracting files to {output_dir}...")
        os.makedirs(output_dir, exist_ok=True)
        
        extracted_size = 0
        for i, archived_file in enumerate(archived_files, 1):
            # Create output directory structure
            output_path = os.path.join(output_dir, archived_file.name.replace('\\', os.sep))
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Read encrypted data
            f.seek(archived_file.offset)
            data = f.read(archived_file.size)
            
            # Decrypt data
            key = archived_file.key
            decrypted = []
            key_bytes = struct.pack("<I", key)
            
            for i in range(len(data)):
                if i > 0 and i % 4 == 0:
                    key = (key * 7 + 3) & 0xFFFFFFFF
                    key_bytes = struct.pack("<I", key)
                decrypted.append(data[i] ^ key_bytes[i % 4])
            
            # Write decrypted file
            with open(output_path, "wb") as out_f:
                out_f.write(bytes(decrypted))
            
            # Update progress
            extracted_size += archived_file.size
            progress = (extracted_size / total_size) * 100
            print(f"\rProgress: [{i}/{len(archived_files)}] {progress:.1f}% - {archived_file.name}", end="")

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 rgss3a_extractor.py <rgss3a_file>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} not found")
        sys.exit(1)
        
    try:
        extract_rgss3a(input_file)
        print(f"\n\nSuccessfully extracted {input_file} to ./tmp directory")
    except Exception as e:
        print(f"Error extracting file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
