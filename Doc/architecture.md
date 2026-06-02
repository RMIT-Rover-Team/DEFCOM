# DEFCOM Architecture definition Version 1.0 (05/05/2026)
## Authors:
* Kaelan Grainger (MegaKG)

## Table of Contents:

- [DEFCOM Architecture definition Version 1.0 (05/05/2026)](#defcom-architecture-definition-version-10-05052026)
  - [Authors:](#authors)
  - [Table of Contents:](#table-of-contents)
  - [The DEFCOM File Format](#the-defcom-file-format)
    - [The FQDN](#the-fqdn)
    - [The Application Name](#the-application-name)
    - [Establishing a host](#establishing-a-host)
    - [Establishing a client](#establishing-a-client)
    - [Message Content](#message-content)
    - [Packet Format](#packet-format)
  - [Publisher \& Subscriber Channels](#publisher--subscriber-channels)
  - [Lossy Publisher \& Subscriber Channels](#lossy-publisher--subscriber-channels)
  - [Transactional Channels](#transactional-channels)


## The DEFCOM File Format
DEFCOM files provide the fundamental basis for all communication between DEFCOM nodes.

At the core of the DEFCOM file format is the service "Name".
This name must be unique within the entire network, referring to combination of the application's name and Fully Qualified Domain Name (FQDN). 

An example of a service name is `TestSimpleService@localhost`.
This can be decoded as follows:
* `TestSimpleService` is the application name
* `localhost` is the FQDN

### The FQDN
DEFCOM relies entirely on maintaining a valid DNS or /etc/hosts file for resolving the FQDN to an IP address within the network. In the case of a field deployment without DNS, it is vitally important that every node in the network has the full definition of all hostnames listed in the hosts file as follows:

/etc/hosts:
```
127.0.0.1 localhost
192.168.40.1 SomeNode1
192.168.40.2 SomeNode2
```

It is also valid in a DEFCOM file to just directly reference the IP address of the node such as: `TestSimpleService@192.168.40.1`

### The Application Name
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

### Establishing a host

When a host side (such as *MulticastPublisher* or *ServerChannel*) is created, the system will attempt to bind to both the TCP address defined by the Application Name, and a Unix socket located at `/tmp/<Name>`.

A seperate thread will be spawned to accept connection for each of the socket types. 

![Host Decoding](https://github.com/RMIT-Rover-Team/rmit-lib-DEFCOM/blob/main/Doc/assets/ServerSpawn.png)

### Establishing a client

When a client side (such as *MulticastSubscriber* or *ClientChannel*) is created, the system will first check the `/tmp/` directory for a socket with the name defined by the Application Name. If it does not exist, the system will attempt to connect to the TCP address and treat the connection as a remote target.

![Client Decoding](https://github.com/RMIT-Rover-Team/rmit-lib-DEFCOM/blob/main/Doc/assets/ClientSpawn.png)

### Message Content

There are two message formats that need to be defined in the DEFCOM file.
These are: `RequestFormat` and `ResponseFormat`

These formats have an identical structure, defining the datatypes present in a message for a given service.

The supported datatypes are:
* `int`
* `char`
* `string`
* `bytes`
* `float`
* `long`

Only Single Dimensional Arrays are supported, which can be defined as:
* `int[30]`

Higher dimensional arrays can utilise this transmission format by collapsing the array into a single dimension array. For example, a 3D array of 10x10x10 can be defined as:
* `int[1000]`
  
This can be indexed as:
* ```value = array[z * 10 + (y * 10 + x)]```


Strings are a special case of char array, in which a supplied length is **required** to determine the fixed maximum length of the string.
A string definition is as follows:
* `string[10]` - A string of maximum length 10
* `string[20]` - A string of maximum length 20



If the process is a publisher, only the `RequestFormat` is used, however, an empty stub must exist for the `ResponseFormat`. 

### Packet Format

Packets are assembled directly as specified in the DEFCOM `RequestFormat` and `ResponseFormat` sections in the order given in the file. 

If the file contains the following:

```
RequestFormat {
    VA: float[2]
    VB: char
}

```

Then the packet shall be of the format:
```
|------|-----------------|-----------------|
| Off- | Byte n          | Byte n+1        |
| set  | 0 1 2 3 4 5 6 7 | 0 1 2 3 4 5 6 7 |
|------|-----------------|-----------------|
| 0x00 | VA Float[0]     | VA Float[0]     |
| 0x02 | VA Float[0]     | VA Float[0]     |
| 0x04 | VA Float[1]     | VA Float[1]     |
| 0x06 | VA Float[1]     | VA Float[1]     |
| 0x08 | VB char         |                 |
|------|-----------------|-----------------|

Length = 9 bytes
```

The total packet size is the sum of all variables present in the format specification, and remains constant for every transmission.

## Publisher & Subscriber Channels

A Publisher Subscriber pair is a unidirectional connection that allows data frames to be broadcast from one node to any other nodes listening on the same network.

![Publisher](https://github.com/RMIT-Rover-Team/rmit-lib-DEFCOM/blob/main/Doc/assets/Publisher.png)

In this configuration, the publisher process will occasionally broadcast a message within its main loop. This operation is non-blocking as messages are sent asynchronously:

```
FOREVER LOOP:
    # Do Something............
    publish(message) # Does not block the process
```

Subscribers operate with a blocking receiver loop, waiting for a message before proceeding with code:

```
FOREVER LOOP:
    message = receive() # Stops the process until a message is received
    # Do Something............
```

## Lossy Publisher & Subscriber Channels

Operate identically to the Publisher & Subscriber channels, but allow packets to be dropped when late.
This is designed to ensure that only the most recent information is received by the endpoint.

This uses UDP as a transport layer, limiting packets to max 1000 bytes in size. A sequence number is inserted into each packet, and the receiver will only receive the latest packet, ignoring any older packets.

Sequence numbers are inserted in the format of Unsigned Long Long (8 bytes) as follows:

```
|------|-----------------|-----------------|
| Off- | Byte n          | Byte n+1        |
| set  | 0 1 2 3 4 5 6 7 | 0 1 2 3 4 5 6 7 |
|------|-----------------|-----------------|
| 0x00 | Sequence Number | Sequence Number |
| 0x02 | Sequence Number | Sequence Number |
| 0x04 | Sequence Number | Sequence Number |
| 0x06 | Sequence Number | Sequence Number |
| 0x08 | Message         | Message         |
...
|------|-----------------|-----------------|

Length = lengthg(Message) + 8 bytes
```
## Transactional Channels

Transactional connections behave as a traditional network server. A message 'request' is send by the client to the server, and the server will respond with a different 'response' message in a synchronous manner.

![Server](https://github.com/RMIT-Rover-Team/rmit-lib-DEFCOM/blob/main/Doc/assets/Server.png)


A client may initiate a request at any time during operation. As requests are synchronous, this will block the process until a response is received.
```
FUNCTION MAIN:
    ...
    resultMessage = request(requestMessage) # Send Request and Get Result
    ...
```

To handle requests as they arrive, thge server process relies on a function hook `handlerHook` to be defined by the user. This function will be called upon reception of a request and must construct a response message, returning control to the server calling process.

```
FUNCTION myHandler(requestMessage, responseMessage)
    # Do something with the response based by the request

FUNCTION MAIN:
    # Make a server 
    myServer ← newServer(DEFCOM, myHandler)
    myServer.run()

```

