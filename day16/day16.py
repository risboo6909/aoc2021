import os


def silver(parsed):
    pass


def gold(parsed):
    pass


class Literal(object):

    PACKET_ID = 4
    GROUP_SIZE = 5

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
    HEADER_SIZE = 16

    def parse(self, bits):

        ABSOLUTE_LEN_ID = 0
        NUMBER_OF_SUBPACKETS_ID = 1

        length_type_id = int(bits[0])

        try:

            num = bits[1: SubPacket.HEADER_SIZE]
            num = int(''.join(num), 2)

            cur_idx = 0
            sub_packets = []

            if length_type_id == ABSOLUTE_LEN_ID:
                num_of_bits = num

                while cur_idx < num_of_bits:
                    parsed, delta = parse_bits(bits[16+cur_idx:16+num_of_bits])
                    sub_packets.extend(parsed)
                    cur_idx += delta

                return sub_packets, cur_idx + SubPacket.HEADER_SIZE
            else:
                num_of_packets = num

        except:
            return [], 0
        else:
            return sub_packets, cur_idx + SubPacket.HEADER_SIZE


def parse_bits(bits):
    cur_idx = 0

    parsed = []

    while cur_idx < len(bits)-6:
        version, type_id = bits[cur_idx: cur_idx +
                                3], bits[cur_idx+3: cur_idx+6]

        # skip first 6 bits of version and type_id
        cur_idx += 6

        if int(type_id, 2) == Literal.PACKET_ID:
            literal = Literal()
            cur_idx += literal.parse(bits[cur_idx:])
            parsed.append(literal)
        else:
            sub_packet = SubPacket()
            sub_parsed, delta = sub_packet.parse(bits[cur_idx:])
            cur_idx += delta
            parsed.extend(sub_parsed)

    return parsed, cur_idx


def parse(lines):
    hex_str = lines[0]
    bits = bin(int('1'+hex_str, 16))[3:]
    parsed, _ = parse_bits(bits)

    for token in parsed:
        print(token)


def solve():
    lines = open(os.path.join(os.path.dirname(
        __file__), "input"), "rt").readlines()
    parsed = parse(lines)

    return "DAY16", silver(parsed), gold(parsed)
