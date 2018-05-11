# calculate subnet information based on IP and mask


def display_title():
    print("\nSubnet Calculator")


def get_ip():
    while True:
        ip = input("\nEnter IP in dotted decimal notation: ")
        ip = ip.strip()
        ip_list = []

        if len(ip.split(".")) != 4:
            print("Invalid IP address, try again.")
            continue

        for n in ip.split("."):
            if n.isdigit() and int(n) <= 255 and int(n) >= 0:
                ip_list.append(n)

        if len(ip_list) != 4:
            print("Invalid IP address, try again.")
            continue
        else:
            return ip_list


def check_ip():
    pass


def get_mask():
    while True:
        mask = input("\nEnter subnet mask in dotted decimal notation: ")
        mask = mask.strip()
        mask_list = mask.split(".")

        if check_mask(mask_list) and len(mask_list) == 4:
            return mask_list
        else:
            print("Invalid subnet mask, try again. ")


def check_mask(mask_list):
    valid_masks = (0, 128, 192, 224, 240, 248, 252, 254, 255)
    a = 255

    try:
        for n in mask_list:
            n = int(n)
            if n > a or n not in valid_masks or a < 255 and n != 0:
                print("1")
                return False
            a = n
    except ValueError:
        print('4')
        return False

    return True


def main():
    display_title()

    while True:
        ip_list = get_ip()
        mask_list = get_mask()
        print(ip_list, mask_list, sep="\n")


if __name__ == "__main__":
    main()