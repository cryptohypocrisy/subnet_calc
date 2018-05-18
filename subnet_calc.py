# calculate subnet information based on IP and mask


import math as m
import locale as lc
import getipinfo as gii

locale = lc.setlocale(lc.LC_ALL, '')  # set locale for formatting
if locale == "C":
    lc.setlocale(lc.LC_ALL, 'en_us')  # if Mac OS, set it 'en_us'


def display_title():
    print("\nSubnet Calculator")


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
    print(fmt.format("IP:", ".".join(ip) + "/%s" % cidr,))
    print(fmt.format("Netmask:", ".".join(mask)))
    print(fmt.format("Wildcard:", ".".join(wildcard)))
    print(fmt.format("Network:", ".".join(network)))
    print(fmt.format("Broadcast:", ".".join(broadcast)))
    print(fmt.format("Class:", net_class))
    print(fmt.format("Number of Networks:", networks))
    print("{:<25} {:>25,}".format("Hosts Per Network:", hosts))


def main():
    display_title()

    while True:
        ip_list = gii.get_ip()
        mask_list, cidr = gii.get_mask()
        display_subnet_info(ip_list, mask_list, cidr)
        choice = input("\nAnother? [y/n] ")
        if choice.strip().lower() != "y":
            break

    print("Terminating program...")


if __name__ == "__main__":
    main()