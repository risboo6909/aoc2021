import os
from functools import reduce


def silver(tokens):
    return reduce(lambda acc, token: token.version + acc, tokens, 0)


def gold(tokens):
    return tokens[0].number


class Literal(object):

    PACKET_ID = 4
    GROUP_SIZE = 5

    def __init__(self, version):
        self.version = version

    def parse(self, bits):
        number_bits = []
        for i in range(0, len(bits), Literal.GROUP_SIZE):
            number_bits.append(bits[i + 1 : i + Literal.GROUP_SIZE])
            if int(bits[i]) == 0:
                break

        self.number = int("".join(number_bits), 2)
        return i + Literal.GROUP_SIZE


class SubPacket(object):

    PACKET_ID = 6

    BITS_LEN = 16
    BITS_PACKETS = 12

    def __init__(self, version, type_id):
        self.version = version
        self.type_id = type_id

    def apply_op(self, packets):

        if self.type_id == 0:
            # sum
            res = 0
            for packet in packets:
                res += packet.number

        elif self.type_id == 1:
            # product
            res = 1
            for packet in packets:
                res *= packet.number

        elif self.type_id == 2:
            # min
            res = min(packets, key=lambda packet: packet.number).number

        elif self.type_id == 3:
            # max
            res = max(packets, key=lambda packet: packet.number).number

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

    def parse(self, bits, apply_ops):

        ABSOLUTE_LEN_ID = 0
        NUMBER_OF_SUBPACKETS_ID = 1

        length_type_id = int(bits[0], 2)

        cur_idx = 0
        sub_packets = []

        if length_type_id == ABSOLUTE_LEN_ID:

            num_of_bits = bits[1 : SubPacket.BITS_LEN]
            if num_of_bits == "":
                return [], 0

            num_of_bits = int(num_of_bits, 2)

            while cur_idx < num_of_bits:
                parsed, delta = parse_bits(
                    bits[
                        SubPacket.BITS_LEN + cur_idx : SubPacket.BITS_LEN + num_of_bits
                    ],
                    apply_ops,
                )
                sub_packets.extend(parsed)
                cur_idx += delta

            if apply_ops:
                sub_packets = self.apply_op(sub_packets)

            return sub_packets, cur_idx + SubPacket.BITS_LEN

        elif length_type_id == NUMBER_OF_SUBPACKETS_ID:

            num_of_packets = bits[1 : SubPacket.BITS_PACKETS]
            if num_of_packets == "":
                return [], 0

            for _ in range(int(num_of_packets, 2)):
                parsed, delta = parse_bits(
                    bits[SubPacket.BITS_PACKETS + cur_idx :], apply_ops, one_packet=True
                )
                sub_packets.extend(parsed)
                cur_idx += delta

            if apply_ops:
                sub_packets = self.apply_op(sub_packets)

            return sub_packets, cur_idx + SubPacket.BITS_PACKETS


def parse_bits(bits, apply_ops, one_packet=False):

    cur_idx = 0
    parsed = []

    while cur_idx < len(bits) - 6:
        version, type_id = bits[cur_idx : cur_idx + 3], bits[cur_idx + 3 : cur_idx + 6]

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
            sub_expr, delta = sub_packet.parse(bits[cur_idx:], apply_ops)
            cur_idx += delta

            if not apply_ops:
                parsed.append(sub_packet)

            parsed.extend(sub_expr)

        if one_packet:
            # only one iteration if one_packet is True
            break

    return parsed, cur_idx


def parse(lines, apply_ops):
    hex_str = lines[0]
    bits = bin(int("1" + hex_str, 16))[3:]
    tokens, _ = parse_bits(bits, apply_ops)

    return tokens


def solve():
    lines = open(os.path.join(os.path.dirname(__file__), "input"), "rt").readlines()

    return "DAY16", silver(parse(lines, False)), gold(parse(lines, True))
