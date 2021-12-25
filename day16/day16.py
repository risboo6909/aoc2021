import os
from functools import reduce


def silver(tokens):
    net = 0
    for token in tokens:
        if isinstance(token, list):
            net += silver(token)
        else:
            net += token.version
        
    return net


def gold(tokens):
    
    pass


class Literal(object):

    PACKET_ID = 4
    GROUP_SIZE = 5

    def __init__(self, version):
        self.version = version

    def parse(self, bits):
        try:
            number_bits = []
            for i in range(0, len(bits), Literal.GROUP_SIZE):
                number_bits.append(bits[i+1: i+Literal.GROUP_SIZE])
                if int(bits[i]) == 0:
                    break

            self.number = int(''.join(number_bits), 2)
            return i+Literal.GROUP_SIZE
        except:
            return 0

    def __str__(self):
        return str(self.number)


class SubPacket(object):

    PACKET_ID = 6

    BITS_LEN = 16
    BITS_PACKETS = 12

    def __init__(self, version, type_id):
        self.version = version
        self.type_id = type_id

    def apply_op(self):
        pass

    def parse(self, bits):

        ABSOLUTE_LEN_ID = 0
        NUMBER_OF_SUBPACKETS_ID = 1

        length_type_id = int(bits[0], 2)

        try:

            cur_idx = 0
            sub_packets = []

            if length_type_id == ABSOLUTE_LEN_ID:

                num_of_bits = bits[1: SubPacket.BITS_LEN]
                num_of_bits = int(''.join(num_of_bits), 2)

                while cur_idx < num_of_bits:
                    parsed, delta = parse_bits(bits[SubPacket.BITS_LEN+cur_idx: SubPacket.BITS_LEN+num_of_bits])
                    sub_packets.extend(parsed)
                    cur_idx += delta

                return sub_packets, cur_idx + SubPacket.BITS_LEN

            elif length_type_id == NUMBER_OF_SUBPACKETS_ID:

                num_of_packets = bits[1: SubPacket.BITS_PACKETS]
                num_of_packets = int(''.join(num_of_packets), 2)

                for _ in range(num_of_packets):
                    parsed, delta = parse_bits(bits[SubPacket.BITS_PACKETS+cur_idx:])
                    sub_packets.extend(parsed)
                    cur_idx += delta

                return sub_packets, cur_idx + SubPacket.BITS_PACKETS

        except:
            return [], 0


def parse_bits(bits):
    cur_idx = 0

    parsed = []

    while cur_idx < len(bits)-6:
        version, type_id = bits[cur_idx: cur_idx +
                                3], bits[cur_idx+3: cur_idx+6]

        # skip first 6 bits of version and type_id
        cur_idx += 6

        version = int(version, 2)
        type_id = int(type_id, 2)

        if type_id == Literal.PACKET_ID:
            literal = Literal(version)
            cur_idx += literal.parse(bits[cur_idx:])

            parsed.append(literal)

        else:
            sub_packet = SubPacket(version, type_id)
            sub_parsed, delta = sub_packet.parse(bits[cur_idx:])
            cur_idx += delta

            parsed.append([sub_packet, [*sub_parsed]])
            #parsed.extend(sub_parsed)

    return parsed, cur_idx


def parse(lines):
    hex_str = lines[0]
    bits = bin(int('1'+hex_str, 16))[3:]
    tokens, _ = parse_bits(bits)

    return tokens


def solve():
    lines = open(os.path.join(os.path.dirname(
        __file__), "input"), "rt").readlines()
    tokens = parse(lines)

    #print(tokens)

    return "DAY16", silver(tokens), gold(tokens)
