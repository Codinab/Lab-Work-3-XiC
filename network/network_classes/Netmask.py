class Netmask:
    def __init__(self, mask):
        self.netmask = self.cidr_to_int(mask)
        self.wildcard = self.cidr_to_int(self.int_to_cidr(~self.netmask))

    @staticmethod
    def cidr_to_int(mask):
        """Converts a dotted decimal format IP to integer."""
        octets = map(int, mask.split('.'))
        return sum(octet << (24 - i * 8) for i, octet in enumerate(octets))

    @staticmethod
    def int_to_cidr(mask):
        """Converts an integer IP to dotted decimal format."""
        return '.'.join(str(mask >> (24 - i * 8) & 0xFF) for i in range(4))

    def netmask_to_decimal(self):
        """Converts a netmask to dotted decimal format."""
        return self.int_to_cidr(self.netmask)

    def wildcard_to_decimal(self):
        """Converts a wildcard to dotted decimal format."""
        return self.int_to_cidr(self.wildcard)

    def netmask_to_cidr(self):
        """Converts a netmask to CIDR notation."""
        return sum(bin(int(x)).count('1') for x in self.int_to_cidr(self.netmask).split('.'))

    def wildcard_to_cidr(self):
        """Converts a wildcard to CIDR notation."""
        return sum(bin(int(x)).count('1') for x in self.int_to_cidr(self.wildcard).split('.'))

    def is_host_mask(self):
        """Checks if the netmask is a host mask."""
        return self.netmask == 0xFFFFFFFF

    def is_default_mask(self):
        """Checks if the netmask is a default mask."""
        return self.netmask == 0x00000000

    def __eq__(self, other):
        return self.netmask == other.netmask and self.wildcard == other.wildcard

    def __hash__(self):
        return hash((self.netmask, self.wildcard))

