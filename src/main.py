from HuffmanCoding import *


if __name__ == "__main__":
    path = "../data/test.txt"
    h = HuffmanCoding(path)
    output_path = h.compress()
    print("Compressed file path: " + output_path)
    decompressed_path = h.decompress(output_path)
    print("Decompressed file path: " + decompressed_path)

    if open(path, 'r').read() == open(decompressed_path, 'r').read():
        xml_writer(True, "../log/test.xml")
    else:
        xml_writer(False, "../log/test.xml")

    xml_reader("../log/test.xml")








