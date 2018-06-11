# module that gets IP address in dotted decimal and subnet mask
# in DD or CIDR and returns each as a list of four quartets


def get_ip():
    """CHECKS FOR VALID IP (DOTTED DECIMAL
     NOTATION) AND RETURNS AS A LIST"""
    while True:
        ip = input("\nEnter IP in dotted decimal notation: ")
        ip = ip.strip()
        ip_list = ip.split(".")  # split into quartet list at the dots

        if len(ip_list) == 4 and check_ip(ip_list):  # input validation
            return ip_list  # return the list of quartets
        else:
            print("Invalid IP address, try again.")


def get_mask():
    """CHECKS FOR VALID NETMASK (CIDR OR
    DOTTED DECIMAL) AND RETURNS AS LIST"""
    dec_mask_list = []

    while True:
        netmask = input("Enter netmask in dotted decimal or CIDR notation: ")
        netmask = netmask.strip()
        netmask = netmask.replace("/", "")  # user can input slash for CIDR

        # if input is DD, run these statements
        if "." in netmask:
            dec_mask = netmask.strip()
            dec_mask_list = dec_mask.split(".")

            # input validation
            if len(dec_mask_list) == 4 and check_mask(dec_mask_list):
                cidr = 0  # hold the count of 1's in binary mask
                # go through each quartet, convert decimal to binary and
                # sum the number of 1's in each quartet to get cidr number
                for quartet in dec_mask_list:
                    cidr += bin(int(quartet)).count("1")
            else:
                print("Invalid netmask, try again. ")
                continue

            return dec_mask_list, cidr  # return mask in DD and CIDR

        # if mask input is CIDR, run these statements
        elif netmask.isdecimal() and (0 <= int(netmask) <= 32):
            cidr = int(netmask)
            bin_mask = "1" * cidr  # create string representing mask in binary
            if len(bin_mask) < 32:
                # fill in the zeros to make it 32 bits
                bin_mask += "0" * (32 - len(bin_mask))

            # split up binary string into octet list
            bin_mask_list = [bin_mask[0:8]] + [bin_mask[8:16]] + [bin_mask[16:24]] + \
                            [bin_mask[24:32]]

            for quartet in bin_mask_list:
                # convert binary mask to decimal
                dec_mask = 256 - (2 ** (8 - quartet.count("1")))
                # append resulting decimal number to mask list
                dec_mask_list.append(str(dec_mask))

            return dec_mask_list, cidr  # return mask in DD and CIDR
        else:
            print("Invalid netmask, try again.")


def check_ip(ip_list):
    try:
        for n in ip_list:
            n = int(n)  # must be an integer
    except ValueError:
        return False

    if n < 0 or n > 255:  # must be in range 0 - 255
        return False

    return True


def check_mask(mask_list):
    valid_masks = (0, 128, 192, 224, 240, 248, 252, 254, 255)  # valid masks
    # 'a' holds the value of the previous quartet processed in
    # the for loop so it can be compared to the subsequent octet
    a = 255

    for n in mask_list:
        try:
            n = int(n)  # must be a number
        except ValueError:
            return False

        # each successive quartet musn't be greater than the
        # one preceding it.  each quartet must be a valid exponent
        # of 2.  all quartets after the one with the significant
        # bit must be equal to 0
        if n > a or n not in valid_masks or (a < 255 and n != 0):
            return False
        a = n  # set 'a' to value of current octet for next iteration checks

    return True
