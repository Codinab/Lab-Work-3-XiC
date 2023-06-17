class Ip:
    def __init__(self, ip):
        self.value = self.octets_to_int(ip)

    @staticmethod
    def octets_to_int(ip):
        """Converts a dotted decimal format IP to integer."""
        octets = map(int, ip.split('.'))
        return sum(octet << (24 - i * 8) for i, octet in enumerate(octets))

    @staticmethod
    def int_to_octets(ip_value):
        """Converts an integer IP to dotted decimal format."""
        return '.'.join(str(ip_value >> (24 - i * 8) & 0xFF) for i in range(4))

    def __str__(self):
        return self.int_to_octets(self.value)

    def __eq__(self, other):
        return self.value == other.value

    def __lt__(self, other):
        return self.value < other.value

    def __hash__(self):
        return hash(self.value)
