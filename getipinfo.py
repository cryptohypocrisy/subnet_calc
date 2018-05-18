# module that gets IP address in dotted decimal and subnet mask
# in DD or CIDR


def get_ip():
    while True:
        ip = input("\nEnter IP in dotted decimal notation: ")
        ip = ip.strip()
        ip_list = ip.split(".")

        if len(ip_list) == 4 and check_ip(ip_list):  # input validation
            return ip_list
        else:
            print("Invalid IP address, try again.")


def get_mask():
    dec_mask_list = []

    while True:
        netmask = input("Enter netmask in dotted decimal or CIDR notation: ")
        netmask = netmask.strip()
        netmask = netmask.replace("/", "")

        if "." in netmask:
            dec_mask = netmask.strip()
            dec_mask_list = dec_mask.split(".")
            if len(dec_mask_list) == 4 and check_mask(dec_mask_list):
                cidr = 0
                for quartet in dec_mask_list:
                    cidr += bin(int(quartet)).count("1")
            else:
                print("Invalid netmask, try again. ")
                continue

            return dec_mask_list, cidr

        elif netmask.isdecimal() and (0 <= int(netmask) <= 32):
            cidr = int(netmask)
            bin_mask = "1" * cidr  # create string to
            if len(bin_mask) < 32:  # represent mask in
                bin_mask += "0" * (32 - len(bin_mask))  # binary

            bin_mask_list = [bin_mask[0:8]] + [bin_mask[8:16]] + [bin_mask[16:24]] + \
                            [bin_mask[24:32]]  # split up "binary" string into
            # quartets

            for quartet in bin_mask_list:
                dec_mask = 256 - (2 ** (8 - quartet.count("1")))  # convert binary
                dec_mask_list.append(str(dec_mask))  # quartet to decimal
                # and append to list
            return dec_mask_list, cidr
        else:
            print("Invalid netmask, try again.")


def check_ip(ip_list):
    try:
        for n in ip_list:
            n = int(n)
            if n < 0 or n > 255:
                return False
    except ValueError:
        return False

    return True


def check_mask(mask_list):
    valid_masks = (0, 128, 192, 224, 240, 248, 252, 254, 255)
    a = 255

    try:
        for n in mask_list:
            n = int(n)
            if n > a or n not in valid_masks or a < 255 and n != 0:
                return False
            a = n
    except ValueError:
        return False

    return True