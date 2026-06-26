# DEFCOM C++ API definition Version 1.0 (26/06/2026)
## Authors:
* Kaelan Grainger (MegaKG)

## Table of Contents:
- [DEFCOM C++ API definition Version 1.0 (26/06/2026)](#defcom-c-api-definition-version-10-26062026)
  - [Authors:](#authors)
  - [Table of Contents:](#table-of-contents)
  - [Message Objects](#message-objects)
    - [MessageStructure](#messagestructure)
      - [Methods:](#methods)
        - [Function: `void setDouble(std::string key, double value, size_t index)`](#function-void-setdoublestdstring-key-double-value-size_t-index)
        - [Function: `void setFloat(std::string key, float value, index: int)`](#function-void-setfloatstdstring-key-float-value-index-int)
        - [Function: `void setInt(std::string key, int value, size_t index)`](#function-void-setintstdstring-key-int-value-size_t-index)
        - [Function: `void setLong(std::string key, long long value, size_t index)`](#function-void-setlongstdstring-key-long-long-value-size_t-index)
        - [Function: `void setChar(std::string key, char value, size_t index)`](#function-void-setcharstdstring-key-char-value-size_t-index)
        - [Function: `void setBytes(std::string key, uint8_t* data)`](#function-void-setbytesstdstring-key-uint8_t-data)
        - [Function: `void setString(std::string key, std::string value)`](#function-void-setstringstdstring-key-stdstring-value)
      - [Function: `double getDouble(std::string key, size_t index)`](#function-double-getdoublestdstring-key-size_t-index)
        - [Function: `float getFloat(std::string key, size_t index)`](#function-float-getfloatstdstring-key-size_t-index)
        - [Function: `int getInt(std::string key, size_t index)`](#function-int-getintstdstring-key-size_t-index)
        - [Function: `long long getLong(std::string key, size_t index)`](#function-long-long-getlongstdstring-key-size_t-index)
        - [Function: `getChar(std::string key, size_t index)`](#function-getcharstdstring-key-size_t-index)
        - [Function: `void getBytes(std::string key, uint8_t* dataBuffer)`](#function-void-getbytesstdstring-key-uint8_t-databuffer)
        - [Function: `std::string getString(std::string key)`](#function-stdstring-getstringstdstring-key)
  - [Publisher / Subscriber Channel](#publisher--subscriber-channel)
    - [Publisher](#publisher)
      - [Dependencies:](#dependencies)
      - [Constructor:](#constructor)
      - [Methods:](#methods-1)
        - [Function: `MessageStructure getNewMessageObject()`](#function-messagestructure-getnewmessageobject)
        - [Function: `void publish(MessageStructure message)`](#function-void-publishmessagestructure-message)
    - [Subscriber](#subscriber)
      - [Dependencies:](#dependencies-1)
      - [Constructor:](#constructor-1)
      - [Methods:](#methods-2)
        - [Function: `MessageStructure subscribe()`](#function-messagestructure-subscribe)
  - [Lossy Publisher / Subscriber Channel](#lossy-publisher--subscriber-channel)
    - [Publisher](#publisher-1)
      - [Dependencies:](#dependencies-2)
      - [Constructor:](#constructor-2)
      - [Methods:](#methods-3)
    - [Subscriber](#subscriber-1)
      - [Dependencies:](#dependencies-3)
      - [Constructor:](#constructor-3)
      - [Methods:](#methods-4)
  - [Transactional Channel](#transactional-channel)
    - [Server Channel](#server-channel)
      - [Dependencies:](#dependencies-4)
      - [Constructor:](#constructor-4)
      - [Methods:](#methods-5)
        - [Function: `void start()`](#function-void-start)
    - [Client Channel](#client-channel)
      - [Dependencies:](#dependencies-5)
      - [Constructor:](#constructor-5)
      - [Methods:](#methods-6)
        - [Function: `MessageStructure getNewRequestObject()`](#function-messagestructure-getnewrequestobject)
        - [Function: `MessageStructure request(MessageStructure request)`](#function-messagestructure-requestmessagestructure-request)


## Message Objects

### MessageStructure

This object is not designed to be instantiated directly, instead relying on the DEFCOM file loader or Channel to create an object as required. It is included in all Channel library files.

#### Methods:

##### Function: `void setDouble(std::string key, double value, size_t index)`
Sets a double value in the message for a given key. The index is optional and defaults to 0.
```c++
myMessage.setDouble("VA", 1.0, 0)
```

##### Function: `void setFloat(std::string key, float value, index: int)`
Sets a float value in the message for a given key. The index is optional and defaults to 0.
```c++
myMessage.setFloat("VA", 1.0, 0)
```

##### Function: `void setInt(std::string key, int value, size_t index)`
Sets an int value in the message for a given key. The index is optional and defaults to 0.
```c++
myMessage.setInt("VA", 1, 0)
```

##### Function: `void setLong(std::string key, long long value, size_t index)`
Sets a long value in the message for a given key. The index is optional and defaults to 0.
```c++
myMessage.setLong("VA", 1, 0)
```

##### Function: `void setChar(std::string key, char value, size_t index)`
Sets a char value in the message for a given key. The index is optional and defaults to 0.
```c++
myMessage.setChar("VA", 'A', 0)
```

##### Function: `void setBytes(std::string key, uint8_t* data)`
Copies a buffer into the message for given key. 
```c++
uint8_t myData[] = {0x01, 0x02, 0x03};
myMessage.setBytes("VA", myData)
```

##### Function: `void setString(std::string key, std::string value)`
Sets a string value in the message for a given key.
```c++
myMessage.setString("VA", "Hello World")
```

#### Function: `double getDouble(std::string key, size_t index)`
Gets a double value in the message for a given key. The index is optional and defaults to 0.
```c++
double localVar = myMessage.getDouble("VA", 0)
```

##### Function: `float getFloat(std::string key, size_t index)`
Gets a float value in the message for a given key. The index is optional and defaults to 0.
```c++
float localVar = myMessage.getFloat("VA", 0)
```

##### Function: `int getInt(std::string key, size_t index)`
Gets an int value in the message for a given key. The index is optional and defaults to 0.
```c++
int localVar = myMessage.getInt("VA", 0)
```

##### Function: `long long getLong(std::string key, size_t index)`
Gets a long value in the message for a given key. The index is optional and defaults to 0.
```c++
long long localVar = myMessage.getLong("VA", 0)
```

##### Function: `getChar(std::string key, size_t index)`
Gets a char value in the message for a given key. The index is optional and defaults to 0.
```c++
char localVar = myMessage.getChar("VA", 0)
```

##### Function: `void getBytes(std::string key, uint8_t* dataBuffer)`
Gets a bytes value in the message for a given key.
```c++
uint8_t myBuffer[10];
myMessage.getBytes("VA", myBuffer)
```

##### Function: `std::string getString(std::string key)`
Gets a string value in the message for a given key. The index is optional and defaults to 0.
```c++
std::string localVar = myMessage.getString("VA", 0)
```


## Publisher / Subscriber Channel

### Publisher

Used to broadcast a message to all subscribers.
Class: `MulticastPublisher` in library `ChannelMulticast`

#### Dependencies:
Must import the following:
```c++
#include <ChannelMulticast.hpp>
#include <FlexibleMessageStructure.hpp>
```

#### Constructor:

To create a publisher server, the object must be initialised with the path to the DEFCOM file:
```c++
MulticastPublisher publisherObject("path/to/defcom/file");
```

#### Methods:

##### Function: `MessageStructure getNewMessageObject()`

To create an outgoing message, a new message object must be created:
```c++
MessageStructure requestObject = publisherObject.getNewMessageObject()
```

This can then be populated with the data to be sent as specified in Message Objects reference:
```c++
requestObject.setFloat("VA",1.0,0)
requestObject.setChar("VB",'a')
```

##### Function: `void publish(MessageStructure message)`
To send the message, the publisher must be called with the message object:
```c++
publisherObject.publish(requestObject)
```



### Subscriber

Used to subscribe to publisher messages.
Class: `MulticastSubscriber` in library `ChannelMulticast`

#### Dependencies:
Must import the following:
```c++
#include <ChannelMulticast.hpp>
#include <FlexibleMessageStructure.hpp>
```

#### Constructor:

A Subscriber object must be created with the path to the DEFCOM file:
```c++
MulticastSubscriber subscriberObject("path/to/defcom/file");
```

#### Methods:

##### Function: `MessageStructure subscribe()`

The client can await a message to be received from the server by calling the subscribe method:
```c++
myMessage = subscriberObject.subscribe()
```

This will return a message object that can be extracted by the client process as specified in Message Objects reference:
```c++
localVariable = myMessage.getChar("VA",1)
```

## Lossy Publisher / Subscriber Channel

### Publisher

Used to broadcast a message to all lossy subscribers.
These messages are not guaranteed to arrive, however, only the latest will be received.
Class: `MulticastPublisher` in library `ChannelMulticast`

#### Dependencies:
Must import the following:
```c++
#include <ChannelLossycast.hpp>
#include <FlexibleMessageStructure.hpp>
```

#### Constructor:

To create a publisher server, the object must be initialised with the path to the DEFCOM file:
```c++
LossyCastPublisher publisherObject("path/to/defcom/file");
```

#### Methods:
See the Publisher / Subscriber Channel section for more information.


### Subscriber
Used to subscribe to lossy publisher messages.
Class: `MulticastSubscriber` in library `ChannelMulticast`

#### Dependencies:
Must import the following:
```c++
#include <ChannelLossycast.hpp>
#include <FlexibleMessageStructure.hpp>
```

#### Constructor:

A Subscriber object must be created with the path to the DEFCOM file:
```c++
LossyCastSubscriber subscriberObject("path/to/defcom/file");
```

#### Methods:
Refer to the Publisher / Subscriber Channel section for more information.


## Transactional Channel

### Server Channel

Used to service transactional requests from clients.
Class: `TXServerChannel` in library `ChannelTransactional`

#### Dependencies:
Must import the following:
```c++
#include <ChannelTransactional.hpp>
#include <FlexibleMessageStructure.hpp>
```

#### Constructor:

To create a server channel, the object must be initialised with the path to the DEFCOM file and a hook to a message handler function:
```c++

void myMessageHandler(MessageStructure* request, MessageStructure* response){
  ...
}

ServerChannel serverObject("path/to/defcom/file", &myMessageHandler);
```
The message handler function must have the following signature, and will be called on reception of a message:
```c++
void myMessageHandler(MessageStructure* request, MessageStructure* response)
```


#### Methods:

##### Function: `void start()`

To start the server serving clients:
```c++
serverObject.start()
```

### Client Channel

Used for clients to request and receive information from the server via initiating a transaction.
Class: `TXClientChannel` in library `ChannelTransactional`

#### Dependencies:
Must import the following:
```c++
#include <ChannelTransactional.hpp>
#include <FlexibleMessageStructure.hpp>
```

#### Constructor:

To create a client channel, the object must be initialised with the path to the DEFCOM file:
```c++
ClientChannel clientObject("path/to/defcom/file")
```

#### Methods:

##### Function: `MessageStructure getNewRequestObject()`

To initiate an outgoing request, a new request object must be created:
```c++
MessageStructure requestObject = clientObject.getNewRequestObject()
```

This can then be populated with the data to be sent as specified in Message Objects reference:
```c++
requestObject.setFloat("VA",1.0,0)
requestObject.setChar("VB",b"a")
```

##### Function: `MessageStructure request(MessageStructure request)`

Sends the contents of request message to the server and synchronously returns the response message object.
```c++
MessageStructure responseObject = clientObject.request(requestObject)
```

This can be extracted by the client process as specified in Message Objects reference:
```c++
localVariable = responseObject.getChar("VA",1)
```