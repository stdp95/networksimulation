# -*- coding: utf-8 -*-
"""
Created on Sat May  6 18:44:50 2017

@author: Satya
"""
import random as r
import math
no_itr = 10
requests = []
networks = []
blocks = []
start_ip = [192,0,0,0]
# ip address space "192.0.0.0/8"
#to change tuple into dotted decimal ip
def dotted(l):
    return str(l[0])+"."+str(l[1])+"."+str(l[2])+"."+str(l[3])
#to find no. of address
def no_addr(s,e):
    n = (e[0]-s[0])*pow(256,3) + (e[1]-s[1])*pow(256,2) + (e[2]-s[2])*pow(256,1) + (e[3]-s[3])*pow(256,0)
    return n
#to allocate ip
def allocate(req,req_no):
    global start_ip
    print ("\n\n-----------------\n\n")
    a_n = 0
    b_s_ip = 0
    #to find an unallocated block
    for block in sorted(blocks,key = lambda tup:tup[2]):
        if block[3] == -1 and req[0] < block[2]:
            b_s_ip = list(block[0])
            break
    #if there is an unallocated block
    if not b_s_ip == 0:
        for i,block in enumerate(blocks):
            if b_s_ip == block[0]:
                a_n = i
                break
        n = int(math.log(req[0],2))
        n_temp = n    
        div = [0]*4
        l_count = 0
        while True:
            if(n_temp/8 > 0):
                div[3-l_count] = 8
                l_count += 1
                n_temp -= 8
            elif n_temp>0:
                div[3-l_count] = n_temp
                break
            else:
                break
        for j in range(3,0,-1):
            if not div[j] == 0:
                if not b_s_ip[j]%pow(2,div[j]) == 0:
                    b_s_ip[j] += pow(2,div[j]) - b_s_ip[j]%pow(2,div[j])
                    if b_s_ip[j]%256 == 0:
                        b_s_ip[j] = 0
                        b_s_ip[j-1] += 1
        ip_s = list(b_s_ip)
        ip_e = list(b_s_ip)
        for j in range(3,0,-1):
            if not div[j] == 0:
                ip_e[j] += pow(2,div[j]) - 1
                if ((b_s_ip[j]) % 256 == 0):
                    b_s_ip[j] = 0
                    b_s_ip[j-1] += 1
       #update network and block list            
        networks.append([req,req_no,ip_s,ip_e,n])
        blocks[a_n][3] = req_no
        for b in blocks:
            print (b)
   #if there is no unallocated block    
    else:
        block_s = list(start_ip)
        n = int(math.log(req[0],2))
        n_temp = n    
        div = [0]*4
        l_count = 0
        while True:
            if(n_temp/8 > 0):
                div[3-l_count] = 8
                l_count += 1
                n_temp -= 8
            elif n_temp>0:
                div[3-l_count] = n_temp
                break
            else:
                break
        for j in range(3,0,-1):
            if not div[j] == 0:
                if not start_ip[j]%pow(2,div[j]) == 0:
                    start_ip[j] += pow(2,div[j]) - start_ip[j]%pow(2,div[j])
                    if start_ip[j]%256 == 0:
                        start_ip[j] = 0
                        start_ip[j-1] += 1
        ip_s = list(start_ip)
        ip_e = list(start_ip)
        for j in range(3,0,-1):
            if not div[j] == 0:
                ip_e[j] += pow(2,div[j]) - 1
                if ((start_ip[j]) % 256 == 0):
                    start_ip[j] = 0
                    start_ip[j-1] += 1
        start_ip = list(ip_e)
        start_ip[3] += 1
        for j in range(3,0,-1):
            if ((start_ip[j]) % 256 == 0 and start_ip[j] != 0):
                start_ip[j] = 0
                start_ip[j-1] += 1
        block_e = list(start_ip)
        #update network and block lsit
        blocks.append([block_s,block_e,no_addr(block_s,block_e),req_no])
        networks.append([req,req_no,ip_s,ip_e,n])
   #print request details
    print ("request id:",req_no)
    print ("demand : ",req[0],"2^",n)
    print ("release time:",req[1])
    print ("IP Start: ",dotted(ip_s))
    print ("IP End: ",dotted(ip_e))
    print ("Network: ",dotted(ip_s)+"/"+str(32-n))
    #print networks details
    print ("Allocated Networks:")
    for network in networks:
        print ("N("+str(network[1])+")","2^"+str(network[4]),dotted(network[2]),dotted(network[3]),dotted(network[2])+"/"+str(32-network[4]))
    print ("-----------------\n\n")
#to deallocate
def deallocate(req_no):
    d_block = []
    n = -1
    #to find block to deallocate
    for d_n,block in enumerate(blocks):
        if block[3] == req_no:
            d_block = block
            n = d_n
            break
  #if no block found, return
    if n == -1:
        return
    #mark block as unallocated
    blocks[n][3] = -1
    print ("releasing request id:",req_no)
    #merge unallocated blocks
    try:
        #check left && right
        if n > 0 and blocks[n-1][3] == -1 and blocks[n+1][3] == -1:
            blocks[n-1][1] = blocks[n+1][1]
            blocks[n-1][2] += blocks[n][2] + blocks[n+1][2]
            blocks.pop(n)
            blocks.pop(n)
        #check left
        elif n > 0 and blocks[n-1][3] == -1:
            blocks[n-1][1] = blocks[n][1]
            blocks[n-1][2] += blocks[n][2]
            blocks.pop(n)
         #check right
        elif blocks[n+1][3] == -1:
            blocks[n][1] = blocks[n+1][1]
            blocks[n][2] += blocks[n+1][2]
            blocks.pop(n+1)
    except Exception as e:
        #if list index goes out of boiund
        print (e)
    #remove deleted network
    for index,network in enumerate(networks):
        if network[1] == req_no:
            networks.pop(index)
            break
    for b in blocks:
        print (b)
    print ("Allocated Networks:")    
    for network in networks:
        print ("N("+str(network[1])+")","2^"+str(network[4]),dotted(network[2]),dotted(network[3]),dotted(network[2])+"/"+str(32-network[4]))
#prepare request list for simulation    
for i in range(no_itr):    
    no_of_addr = pow(2,r.randint(5,15))
    release_time = r.randint(1,5)
    requests.append((no_of_addr,release_time+i))
#list for simulation
for request in requests:
    print (request)
#simulation loop
for req_no,req in enumerate(requests):
    allocate(req,req_no)
    #to check if its time to deallocate a request
    for i in range(0,no_itr):
        if req_no == requests[i][1]:
            input()
            deallocate(i)
    input()
