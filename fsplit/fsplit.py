import os
import argparse

def split_file(file_path, output_dir, chunk_size):
    file_name = os.path.basename(file_path)
    file_dir = os.path.dirname(file_path)
    
    with open(file_path, "rb") as file:
        index = 1
        while True:
            data = file.read(chunk_size)
            if not data:
                break
            
            new_file_name = f"{file_name}_{index}"
            new_file_path = os.path.join(output_dir, new_file_name)
            
            with open(new_file_path, "wb") as new_file:
                new_file.write(data)
            del data
            
            index += 1

# Boyut birimini dönüştüren fonksiyon
def convert_size_to_bytes(size, unit):
    units = {
        'byte':1,
        'kb': 1024,
        'mb': 1024 * 1024,
        'gb': 1024 * 1024 * 1024
    }
    return size * units[unit]

if __name__ == "__main__":
    # Komut satırı argümanlarını tanımla
    parser = argparse.ArgumentParser(description='Large file splitter')
    parser.add_argument('-file','-f', dest='file_path', type=str, help='Path of the file to split')
    parser.add_argument('-output','-o',dest="output_dir", type=str, help='Path of the output directory')
    parser.add_argument('-size', type=int, help='Chunk size')
    parser.add_argument('-unit', type=str, choices=['kb', 'mb', 'gb','byte'], help='Size unit (kb, mb, or gb)')

    # Argümanları ayrıştır
    args = parser.parse_args()

    # Chunk boyutunu hesapla
    chunk_size = convert_size_to_bytes(args.size, args.unit)

    # Split işlemini başlat
    split_file(args.file_path, args.output_dir, chunk_size)
    
#usage fsplit -file myfile -output myfolder -size 500 -unit mb
