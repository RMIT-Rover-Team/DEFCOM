### DEFCOM Architecture definition Version 1.0 (05/05/2026)
## Authors:
* Kaelan Grainger (MegaKG)

## The DEFCOM File Format
DEFCOM files provide the fundamental basis for all communication between DEFCOM nodes.

At the core of the DEFCOM file format is the service "Name".
This name must be unique within the entire network, referring to combination of the application's name and Fully Qualified Domain Name (FQDN). 

An example of a service name is `TestSimpleService@localhost`.
This can be decoded as follows:
* `TestSimpleService` is the application name
* `localhost` is the FQDN

# The FQDN
DEFCOM relies entirely on maintaining a valid DNS or /etc/hosts file for resolving the FQDN to an IP address within the network. In the case of a field deployment without DNS, it is vitally important that every node in the network has the full definition of all hostnames listed in the hosts file as follows:

/etc/hosts:
```
127.0.0.1 localhost
192.168.40.1 SomeNode1
192.168.40.2 SomeNode2
```

It is also valid in a DEFCOM file to just directly reference the IP address of the node such as: `TestSimpleService@192.168.40.1`

# The Application Name
Similarly, the application name is also resolved into a unique TCP port via hashing. 

This is implemented using the following algorithm:
```
FUNCTION nameToPort(name):
    count ← 0

    FOR each character c IN name:
        count ← count * 31 + ASCII_VALUE(c)

    RETURN 2000 + (count MOD 60000)

```

As with the FQDN, the application name can also be substituted with a numeric port number if required. The Name would be defined as: `2000@localhost`, or combined with IP as well: `2000@192.168.40.1`.

# Establishing a host

When a host side (such as *MulticastPublisher* or *ServerChannel*) is created, the system will attempt to bind to both the TCP address defined by the Application Name, and a Unix socket located at `/tmp/<Name>`.

A seperate thread will be spawned to accept connection for each of the socket types. 

![Host Decoding](https://github.com/RMIT-Rover-Team/rmit-lib-DEFCOM/Doc/assets/ServerSpawn.png)

# Establishing a client

When a client side (such as *MulticastSubscriber* or *ClientChannel*) is created, the system will first check the `/tmp/` directory for a socket with the name defined by the Application Name. If it does not exist, the system will attempt to connect to the TCP address and treat the connection as a remote target.

## Publisher & Subscriber


## Transactional

