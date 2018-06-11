# calculate subnet information based on IP and mask


import getipinfo as gii
from network import Network


def display_title():
    print("\nSubnet Calculator")


# gets and displays all the subnet info by using properties
# and methods from the Network class on the 'subnet' object
def display_subnet_info(subnet):
    net_address = subnet.get_network_address()
    broadcast = subnet.get_broadcast_address()
    networks, hosts = subnet.get_num_networks_hosts()
    net_class = subnet.get_net_class()
    wildcard = subnet.get_wildcard()

    fmt = "{:<25} {:>25}"

    # many of the variables like net_address and wildcard are returned
    # as lists; we use the join method to display the value properly
    print()
    print(fmt.format("IP:", ".".join(subnet.ip)))
    print(fmt.format("Netmask:", ".".join(subnet.mask)))
    print(fmt.format("Wildcard:", ".".join(wildcard)))
    print(fmt.format("Network:", ".".join(net_address) +
                     "/%i" % subnet.cidr))
    print(fmt.format("Broadcast:", ".".join(broadcast)))
    print(fmt.format("Class:", net_class))
    print(fmt.format("Number of Networks:", networks))
    print("{:<25} {:>25,}".format("Hosts Per Network:", hosts))


def main():
    display_title()

    while True:
        # use the 'getipinfo' module to get ip address, mask, and
        # cidr from user and validate their input
        ip_list = gii.get_ip()
        mask_list, cidr = gii.get_mask()

        # instantiate our subnet object from the Network class
        # using the values we got from the user
        subnet = Network(ip_list, mask_list, cidr)
        # pass our subnet object to display_subnet_info function
        # which will get and properly format all subnet info
        display_subnet_info(subnet)

        choice = input("\nAnother? [y/n] ")
        if choice.strip().lower() != "y":
            break

    print("Terminating program...")


if __name__ == "__main__":
    main()
