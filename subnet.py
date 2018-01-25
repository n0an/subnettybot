#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

import sys


def check_ip_address(ip_address):
    #Checking octets

    a = ip_address.split('.')

    if (len(a) == 4) and (1 <= int(a[0]) <= 223) and (int(a[0]) != 127) and (int(a[0]) != 169 or int(a[1]) != 254) and (0 <= int(a[1]) <= 255 and 0 <= int(a[2]) <= 255 and 0 <= int(a[3]) <= 255):
        return True
    else:
        return False

def check_subnet_mask(subnet_mask):
    masks = [255, 254, 252, 248, 240, 224, 192, 128, 0]
    b = subnet_mask.split('.')

    if (len(b) == 4) and (int(b[0]) == 255) and (int(b[1]) in masks) and (int(b[2]) in masks) and (int(b[3]) in masks) and (int(b[0]) >= int(b[1]) >= int(b[2]) >= int(b[3])):
        return True
    else:
        return False

def check_subnet_prefix(prefix):
    if prefix[0] != '/':
        return False

    numericPrefix = int(prefix[1:])
    if 8 <= numericPrefix and numericPrefix <= 32:
        return True
    else:
        return False



def convert_subnet_prefix_to_binarystring(prefix):

    str = ''

    for index in range(0, 32):
        if index < prefix:
            str += '1'
        else:
            str += '0'

    print('str = ', str)

    mask_octets_decimal = ['{}'.format(int(str[:8], 2)),
                           '{}'.format(int(str[8:16], 2)),
                           '{}'.format(int(str[16:24], 2)),
                           '{}'.format(int(str[24:32], 2))]


    print('mask_octets_decimal =', mask_octets_decimal)
    return (str, mask_octets_decimal)




 #Convert mask to binary string
def convert_mask_to_binary_string(subnet_mask):

    mask_octets_padded = []

    mask_octets_decimal = subnet_mask.split(".")


    for octet_index in range(0, len(mask_octets_decimal)):

        binary_octet = bin(int(mask_octets_decimal[octet_index])).split("b")[1]

        if len(binary_octet) == 8:

            mask_octets_padded.append(binary_octet)

        elif len(binary_octet) < 8:

            binary_octet_padded = binary_octet.zfill(8)

            mask_octets_padded.append(binary_octet_padded)

    decimal_mask = "".join(mask_octets_padded)
    return (decimal_mask, mask_octets_decimal)


def calculate_wildcard_mask(decimal_mask, mask_octets_decimal):
    no_of_zeros = decimal_mask.count("0")

    no_of_ones = 32 - no_of_zeros

    no_of_hosts = abs(2 ** no_of_zeros - 2) #return positive value for mask /32

    #Obtaining wildcard mask

    wildcard_octets = []

    for w_octet in mask_octets_decimal:

        wild_octet = 255 - int(w_octet)

        wildcard_octets.append(str(wild_octet))

    wildcard_mask = ".".join(wildcard_octets)

    return (wildcard_mask, no_of_ones, no_of_zeros, no_of_hosts)


def convert_ip_to_binary_string(ip_address, no_of_ones, no_of_zeros, no_of_hosts, wildcard_mask):
    ip_octets_padded = []

    ip_octets_decimal = ip_address.split(".")

    for octet_index in range(0, len(ip_octets_decimal)):

        binary_octet = bin(int(ip_octets_decimal[octet_index])).split("b")[1]

        if len(binary_octet) < 8:

            binary_octet_padded = binary_octet.zfill(8)

            ip_octets_padded.append(binary_octet_padded)

        else:

            ip_octets_padded.append(binary_octet)


    binary_ip = "".join(ip_octets_padded)

    network_address_binary = binary_ip[:(no_of_ones)] + "0" * no_of_zeros

    broadcast_address_binary = binary_ip[:(no_of_ones)] + "1" * no_of_zeros

    net_ip_octets = []

    for octet in range(0, len(network_address_binary), 8):

        net_ip_octet = network_address_binary[octet:octet+8]

        net_ip_octets.append(net_ip_octet)


    net_ip_address = []

    for each_octet in net_ip_octets:

        net_ip_address.append(str(int(each_octet, 2)))



    network_address = ".".join(net_ip_address)

    bst_ip_octets = []

    for octet in range(0, len(broadcast_address_binary), 8):

        bst_ip_octet = broadcast_address_binary[octet:octet+8]

        bst_ip_octets.append(bst_ip_octet)

    bst_ip_address = []

    for each_octet in bst_ip_octets:

        bst_ip_address.append(str(int(each_octet, 2)))


    broadcast_address = ".".join(bst_ip_address)

    #Results for selected IP/mask

    result = """
Network address is: {}
Broadcast address is: {}
Number of valid hosts per subnet: {}
Wildcard mask: {}
Mask bits: {}
    """.format(network_address,
               broadcast_address,
               no_of_hosts,
               wildcard_mask,
               no_of_ones)

    return result

    # print("\n")
    #
    # print("Network address is: %s" % network_address)
    #
    # print("Broadcast address is: %s" % broadcast_address)
    #
    # print("Number of valid hosts per subnet: %s" % no_of_hosts)
    #
    # print("Wildcard mask: %s" % wildcard_mask)
    #
    # print("Mask bits: %s" % no_of_ones)
    #
    # print("\n")


ipaddress = '10.1.1.12'
subnetmask = '255.255.255.248'

print(check_ip_address(ip_address=ipaddress))
print(check_subnet_mask(subnet_mask=subnetmask))

print(convert_mask_to_binary_string(subnetmask))

(decimal_mask, mask_octets_decimal) = convert_mask_to_binary_string(subnetmask)

(wildcard_mask, no_of_ones, no_of_zeros, no_of_hosts) = calculate_wildcard_mask(decimal_mask, mask_octets_decimal)

print(calculate_wildcard_mask(decimal_mask, mask_octets_decimal))

print(convert_ip_to_binary_string(ipaddress, no_of_ones, no_of_zeros, no_of_hosts, wildcard_mask))