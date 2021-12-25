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
    return tokens[0].number
    # _, literal = tokens[0]
    # return literal[0].number


def prettify(tokens):
    s = ''
    for token in tokens:
        if isinstance(token, list):
            s += '[{}]'.format(prettify(token))
        elif isinstance(token, Literal):
            s += 'literal value: {}, '.format(token.number)
        elif isinstance(token, SubPacket):
            s += 'subpacket type: {}, content: '.format(token.type_id)
    return s


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

    def apply_op(self, packets):
        print('op: {}, packets: {}'.format(self.type_id, prettify(packets)))
        if self.type_id == 0:
            # sum
            res = 0
            for packet in packets:
                if isinstance(packet, list):
                    res += packet[0].number
                else:
                    res += packet.number

        elif self.type_id == 1:
            # product
            res = 1
            for packet in packets:
                res *= packet.number

        elif self.type_id == 2:
            # min
            res = min(packets, key=lambda packet: packet.number)

        elif self.type_id == 3:
            # max
            res = max(packets, key=lambda packet: packet.number)

        elif self.type_id == 4:
            print("ACHTUNG!")

        elif self.type_id == 5:
            # greater than
            res = 1 if packets[0].number > packets[1].number else 0

        elif self.type_id == 6:
            # less than
            res = 1 if packets[0].number < packets[1].number else 0

        elif self.type_id == 7:
            # equal
            res = packets[0].number == packets[1].number

        tmp = Literal(0)
        tmp.number = res

        return [tmp]

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
                    # print('-', cur_idx, num_of_bits)
                    parsed, delta = parse_bits(
                        bits[SubPacket.BITS_LEN+cur_idx: SubPacket.BITS_LEN+num_of_bits])
                    # sub_packets.extend(parsed)
                    if isinstance(parsed, Literal):
                        sub_packets.extend(parsed)
                    else:
                        print('wrong case 1')
                        sub_packets.extend(parsed)

                    cur_idx += delta

                #sub_packets = self.apply_op(sub_packets)

                return sub_packets, cur_idx + SubPacket.BITS_LEN

            elif length_type_id == NUMBER_OF_SUBPACKETS_ID:

                num_of_packets = bits[1: SubPacket.BITS_PACKETS]
                num_of_packets = int(''.join(num_of_packets), 2)

                for _ in range(num_of_packets):
                   # print('+')
                    parsed, delta = parse_bits(
                        bits[SubPacket.BITS_PACKETS+cur_idx:])
                    # sub_packets.extend(parsed)
                    if isinstance(parsed, Literal):
                        sub_packets.extend(self.apply_op(parsed))
                    else:
                        print('wrong case 2')
                        sub_packets.extend(parsed)

                    cur_idx += delta

                #print('sub b4: {}'.format(sub_packets))
                #sub_packets = self.apply_op(sub_packets)

                return sub_packets, cur_idx + SubPacket.BITS_PACKETS

        except Exception as e:
            print(e, prettify(sub_packets))
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
            print('lit')
            literal = Literal(version)
            cur_idx += literal.parse(bits[cur_idx:])

            # print('lit:', literal)
            # all_tokens.append(literal)
            parsed.append(literal)

        else:
            print('sub')
            sub_packet = SubPacket(version, type_id)
            sub_parsed, delta = sub_packet.parse(bits[cur_idx:])
            cur_idx += delta

            # print('sub:', sub_parsed)

            #parsed.append([sub_packet, [*sub_parsed]])
            # parsed.extend(sub_parsed)
            parsed.append(sub_parsed)
            #print('parsed {}'.format(parsed))

    # print('parsed: {}'.format(parsed))

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

    # print(tokens)

    # return "DAY16", silver(tokens), gold(tokens)
    return "DAY16", None, gold(tokens)
