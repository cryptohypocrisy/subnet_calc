# calculate subnet information based on IP and mask


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
        mask = input("\nEnter subnet mask in dotted decimal notation: ")
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


def calculate_subnet_info(ip, mask):
    net_address_list = []
    broad_address_list = []
    wildcard_list = []

    for n in mask:
        x = 255 - int(n)
        wildcard_list.append(x)

    for i in range(4):
        net_address = int(ip[i]) & int(mask[i])
        net_address_list.append(str(net_address))
        broad_address = int(ip[i]) | int(wildcard_list[i])
        broad_address_list.append(str(broad_address))

    print("{:20} {:10}".format("Network Address:", ".".join(net_address_list)))
    print("{:20} {:10}".format("Broadcast Address:", ".".join(broad_address_list)))


def main():
    display_title()

    while True:
        ip_list = get_ip()
        mask_list = get_mask()
        calculate_subnet_info(ip_list, mask_list)


if __name__ == "__main__":
    main()