import heapq
import os
import xml.etree.ElementTree as ET
import configparser
from src.Node import *



def txt_writer(soubor,path):
    """
    :param config: the config of the test
    :param path: the path of the txt file
    :return: None
    """
    with open(path, 'w') as f:
        f.write(soubor)


def xml_writer(ifSuccess, path):
    """
    :param ifSuccess: if the test is successful
    :param path: the path of the xml file
    :return: None
    """
    root = ET.Element("log")
    succesElement = ET.SubElement(root,"success")
    succesElement.text = str(ifSuccess)
    tree = ET.ElementTree(root)
    tree.write(path)

def xml_reader(path):
    """
    :param path: the path of the xml file
    :return: None
    """

    tree = ET.parse(path)
    root = tree.getroot()
    print(root.tag)
    for child in root:
        print(child.tag, child.text)


class HuffmanCoding:
    def __init__(self, path):
        """
        :param path: the path of the file to be compressed or decompressed
        """
        self.path = path
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

    # functions for compression:

    def make_frequency_dict(self, text):
        """
        :param text: the text to be compressed or decompressed
        :return: the frequency of each character in the text
        """
        frequency = {}
        for character in text:
            if not character in frequency:
                frequency[character] = 0
            frequency[character] += 1
        return frequency

    def make_heap(self, frequency):
        """
        :param frequency: the frequency of each character in the text
        :return: None
        """
        for key in frequency:
            node = Node(key, frequency[key])
            heapq.heappush(self.heap, node)

    def merge_nodes(self):
        """
        :param: the heap of the nodes
        :return:
        """
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = Node(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)

    def make_codes_helper(self, root, current_code):
        """
        :param root: the root of the tree
        :param current_code: the current code
        :return: None
        """
        if root == None:
            return

        if root.char != None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self):
        """
        :param: the heap of the nodes
        :return: None
        """
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code)

    def get_encoded_text(self, text):
        """
        :param text: the text to be compressed or decompressed
        :return: the encoded text
        """
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text

    def pad_encoded_text(self, encoded_text):
        """
        :param encoded_text: the encoded text
        :return: the padded encoded text
        """
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def get_byte_array(self, padded_encoded_text):
        """
        :param padded_encoded_text: the padded encoded text
        :return: the byte array
        """
        if len(padded_encoded_text) % 8 != 0:
            print("Encoded text not padded properly")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            b.append(int(byte, 2))
        return b

    def compress(self):
        """
        :param: the path of the file to be compressed
        :return: None
        """
        config = configparser.ConfigParser()
        config.read('../config/config.ini')
        directory_compress = config['soubor']['adresar']
        file = config['soubor']['nazev']
        filename, file_extension = os.path.splitext(self.path)
        output_path = directory_compress + file + ".bin"

        with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
            text = file.read()
            text = text.rstrip()

            frequency = self.make_frequency_dict(text)
            self.make_heap(frequency)
            self.merge_nodes()
            self.make_codes()

            encoded_text = self.get_encoded_text(text)
            padded_encoded_text = self.pad_encoded_text(encoded_text)

            b = self.get_byte_array(padded_encoded_text)
            output.write(bytes(b))

        print("Compressed")
        return output_path

    # functions for decompression:

    def remove_padding(self, padded_encoded_text):
        """
        :param padded_encoded_text: the padded encoded text
        :return: the encoded text
        """
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:]
        encoded_text = padded_encoded_text[:-1*extra_padding]

        return encoded_text

    def decode_text(self, encoded_text):
        """
        :param encoded_text: the encoded text
        :return: the decoded text
        """
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                character = self.reverse_mapping[current_code]
                decoded_text += character
                current_code = ""

        return decoded_text

    def decompress(self, input_path):
        """
        :param input_path: the path of the file to be decompressed
        :return: None
        """
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + "_decompressed.txt"

        with open(input_path, 'rb') as file, open(output_path, 'w') as output:
            bit_string = ""

            byte = file.read(1)
            while len(byte) > 0:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)

            encoded_text = self.remove_padding(bit_string)

            decompressed_text = self.decode_text(encoded_text)

            output.write(decompressed_text)

        print("Decompressed")
        return output_path
