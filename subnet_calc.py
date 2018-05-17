# calculate subnet information based on IP and mask


import math as m
import locale as lc

locale = lc.setlocale(lc.LC_ALL, '')  # set locale for formatting
if locale == "C":
    lc.setlocale(lc.LC_ALL, 'en_us')  # if Mac OS, set it 'en_us'


def display_title():
    print("\nSubnet Calculator")


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
        """
        mask = input("Enter subnet mask in dotted decimal notation: ")
        mask = mask.strip()
        mask_list = mask.split(".")

        if len(mask_list) == 4 and check_mask(mask_list):
            return mask_list
        else:
            print("Invalid subnet mask, try again. ")
        """    
        try:
            cidr = int(input("Enter mask in CIDR notation: "))
            if 0 <= cidr <= 32:
                bin_mask = "1" * cidr                   # create string to
                if len(bin_mask) < 32:                  # represent mask in
                    bin_mask += "0" * (32 - len(bin_mask))  # binary
            else:
                print("Invalid mask, must be from 0 to 32")
                continue
        except ValueError:
            print("Invalid mask, try again.")
            continue
            
        bin_mask_list = [bin_mask[0:8]]+[bin_mask[8:16]]+[bin_mask[16:24]] + \
                        [bin_mask[24:32]]  # split up "binary" string into
                                           # quartets

        for quartet in bin_mask_list:
            dec_mask = 256 - (2 ** (8 - quartet.count("1")))  # convert binary
            dec_mask_list.append(str(dec_mask))            # quartet to decimal
                                                           # and append to list
        return dec_mask_list, cidr


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


def calculate_network_address(ip, mask):
    net_address_list = []

    for i in range(4):
        net_address = int(ip[i]) & int(mask[i])
        net_address_list.append(str(net_address))

    return net_address_list


def calculate_broadcast_address(ip, mask):
    broadcast_address_list = []
    wildcard_list = []

    for n in mask:
        x = 255 - int(n)
        wildcard_list.append(x)

    for i in range(4):
        broad_address = int(ip[i]) | int(wildcard_list[i])
        broadcast_address_list.append(str(broad_address))

    return broadcast_address_list


def calculate_networks_hosts(mask):
    for i in mask:
        i = int(i)
        if 0 <= i < 255:
            significant_index = mask.index(str(i))
            break
        else:
            significant_index = 3

    if significant_index == 0:
        nh_binary = bin(int(mask[0])).count("1")
        number_of_hosts = int(m.pow(2, (32 - nh_binary)) - 2)
    elif significant_index == 1:
        nh_binary = bin(int(mask[1])).count("1")
        number_of_hosts = int(m.pow(2, (24 - nh_binary)) - 2)
    elif significant_index == 2:
        nh_binary = bin(int(mask[2])).count("1")
        number_of_hosts = int(m.pow(2, (16 - nh_binary)) - 2)
    elif significant_index == 3:
        nh_binary = bin(int(mask[3])).count("1")
        number_of_hosts = int(m.pow(2, (8 - nh_binary)) - 2)

    number_of_networks = int(m.pow(2, nh_binary))

    if int(mask[3]) == 255:
        number_of_networks = 1
        number_of_hosts = 1

    return number_of_networks, number_of_hosts


def get_net_class(ip):
    if '0' <= ip[0] <= '126':
        return "A"
    elif ip[0] == '127':
        return "A (loopback)"
    elif '128' <= ip[0] <='191':
        return "B"
    elif '192'<= ip[0] <= '223':
        return "C"
    elif '224' <= ip[0] <= '239':
        return "D"
    else:
        return "E"


def get_wildcard(mask):
    wildcard_list = []

    for quartet in mask:
        wildcard = int(quartet) ^ 255
        wildcard_list.append(str(wildcard))

    return wildcard_list


def display_subnet_info(ip, mask, cidr):
    network = calculate_network_address(ip, mask)
    broadcast = calculate_broadcast_address(ip, mask)
    networks, hosts = calculate_networks_hosts(mask)
    net_class = get_net_class(ip)
    wildcard = get_wildcard(mask)

    fmt = "{:<25} {:>25}"

    print()
    print(fmt.format("IP:", ".".join(ip)))
    print("{:<20} {:>25} = {:>}".format("Netmask:", ".".join(mask), cidr))
    print(fmt.format("Wildcard:", ".".join(wildcard)))
    print("{:<25} {:>22}/{:>}".format("Network:", ".".join(network), cidr))
    print(fmt.format("Broadcast:", ".".join(broadcast)))
    print(fmt.format("Class:", net_class))
    print(fmt.format("Number of Networks:", networks))
    print("{:<25} {:>25,}".format("Number of Usable Hosts:", hosts))


def main():
    display_title()

    while True:
        ip_list = get_ip()
        mask_list, cidr = get_mask()
        display_subnet_info(ip_list, mask_list, cidr)
        choice = input("\nAnother? [y/n] ")
        if choice.lower() != "y" or choice.lower() != "yes":
            break

    print("Terminating program...")


if __name__ == "__main__":
    main()