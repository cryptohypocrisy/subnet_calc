# calculate subnet information based on IP and mask


import math as m
import locale as lc

locale = lc.setlocale(lc.LC_ALL, '')
if locale == "C":
    lc.setlocale(lc.LC_ALL, 'en_us')


def display_title():
    print("\nSubnet Calculator")


def get_ip():
    while True:
        ip = input("\nEnter IP in dotted decimal notation: ")
        ip = ip.strip()
        ip_list = ip.split(".")

        if len(ip_list) == 4 and check_ip(ip_list):
            return ip_list
        else:
            print("Invalid IP address, try again.")


def get_mask():
    while True:
        mask = input("Enter subnet mask in dotted decimal notation: ")
        mask = mask.strip()
        mask_list = mask.split(".")

        if len(mask_list) == 4 and check_mask(mask_list):
            return mask_list
        else:
            print("Invalid subnet mask, try again. ")


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

    return number_of_networks, number_of_hosts


def get_net_class(ip):
    return ip


def display_subnet_info(ip, mask):
    network = calculate_network_address(ip, mask)
    broadcast = calculate_broadcast_address(ip, mask)
    networks, hosts = calculate_networks_hosts(mask)
    # net_class = get_net_class(ip)

    fmt = "{:<25} {:>25}"

    print()
    print(fmt.format("Network Address:", ".".join(network)))
    print(fmt.format("Broadcast Address:", ".".join(broadcast)))
    # print(fmt.format("Network Class:", ".".join(net_class)))
    print(fmt.format("Number of Networks:", networks))
    print("{:<25} {:>25,}".format("Number of Usable Hosts:", hosts))


def main():
    display_title()

    while True:
        ip_list = get_ip()
        mask_list = get_mask()
        display_subnet_info(ip_list, mask_list)


if __name__ == "__main__":
    main()