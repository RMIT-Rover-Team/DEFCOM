# DEFCOM Python API definition Version 1.0 (05/05/2026)
## Authors:
* Kaelan Grainger (MegaKG)

## Table of Contents:
- [DEFCOM Python API definition Version 1.0 (05/05/2026)](#defcom-python-api-definition-version-10-05052026)
  - [Authors:](#authors)
  - [Table of Contents:](#table-of-contents)
  - [Message Objects](#message-objects)
    - [MessageStructure](#messagestructure)
      - [Methods:](#methods)
        - [Function: `setDouble(key: str, value: float, index: int)` returns `None`](#function-setdoublekey-str-value-float-index-int-returns-none)
        - [Function: `setFloat(key: str, value: float, index: int)` returns `None`](#function-setfloatkey-str-value-float-index-int-returns-none)
        - [Function: `setInt(key: str, value: int, index: int)` returns `None`](#function-setintkey-str-value-int-index-int-returns-none)
        - [Function: `setLong(key: str, value: int, index: int)` returns `None`](#function-setlongkey-str-value-int-index-int-returns-none)
        - [Function: `setChar(key: str, value: bytes, index: int)` returns `None`](#function-setcharkey-str-value-bytes-index-int-returns-none)
        - [Function: `setBytes(key: str, value: bytes)` returns `None`](#function-setbyteskey-str-value-bytes-returns-none)
        - [Function: `setString(key: str, value: str)` returns `None`](#function-setstringkey-str-value-str-returns-none)
      - [Function: `getDouble(key: str, index: int)` returns `float`](#function-getdoublekey-str-index-int-returns-float)
        - [Function: `getFloat(key: str, index: int)` returns `float`](#function-getfloatkey-str-index-int-returns-float)
        - [Function: `getInt(key: str, index: int)` returns `int`](#function-getintkey-str-index-int-returns-int)
        - [Function: `getLong(key: str, index: int)` returns `int`](#function-getlongkey-str-index-int-returns-int)
        - [Function: `getChar(key: str, index: int)` returns `bytes`](#function-getcharkey-str-index-int-returns-bytes)
        - [Function: `getBytes(key: str)` returns `bytes`](#function-getbyteskey-str-returns-bytes)
        - [Function: `getString(key: str)` returns `str`](#function-getstringkey-str-returns-str)
  - [Publisher / Subscriber Channel](#publisher--subscriber-channel)
    - [Publisher](#publisher)
      - [Dependencies:](#dependencies)
      - [Constructor:](#constructor)
      - [Methods:](#methods-1)
        - [Function: `getNewMessageObject(None)` returns `MessageStructure`](#function-getnewmessageobjectnone-returns-messagestructure)
        - [Function: `publish(MessageStructure message)` returns `None`](#function-publishmessagestructure-message-returns-none)
    - [Subscriber](#subscriber)
      - [Dependencies:](#dependencies-1)
      - [Constructor:](#constructor-1)
      - [Methods:](#methods-2)
        - [Function: `subscribe(None)` returns `MessageStructure`](#function-subscribenone-returns-messagestructure)
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
        - [Function: `start(None)` returns `None`](#function-startnone-returns-none)
    - [Client Channel](#client-channel)
      - [Dependencies:](#dependencies-5)
      - [Constructor:](#constructor-5)
      - [Methods:](#methods-6)
        - [Function: `getNewRequestObject(None)` returns `MessageStructure`](#function-getnewrequestobjectnone-returns-messagestructure)
        - [Function: `request(MessageStructure request)` returns `MessageStructure`](#function-requestmessagestructure-request-returns-messagestructure)


## Message Objects

### MessageStructure

This object is not designed to be instantiated directly, instead relying on the DEFCOM file loader or Channel to create an object as required. It is included in all Channel library files.

#### Methods:

##### Function: `setDouble(key: str, value: float, index: int)` returns `None`
Sets a double value in the message for a given key. The index is optional and defaults to 0.
```python
myMessage.setDouble('VA', 1.0, 0)
```

##### Function: `setFloat(key: str, value: float, index: int)` returns `None`
Sets a float value in the message for a given key. The index is optional and defaults to 0.
```python
myMessage.setFloat('VA', 1.0, 0)
```

##### Function: `setInt(key: str, value: int, index: int)` returns `None`
Sets an int value in the message for a given key. The index is optional and defaults to 0.
```python
myMessage.setInt('VA', 1, 0)
```

##### Function: `setLong(key: str, value: int, index: int)` returns `None`
Sets a long value in the message for a given key. The index is optional and defaults to 0.
```python
myMessage.setLong('VA', 1, 0)
```

##### Function: `setChar(key: str, value: bytes, index: int)` returns `None`
Sets a char value in the message for a given key. The index is optional and defaults to 0.
```python
myMessage.setChar('VA', b'A', 0)
```

##### Function: `setBytes(key: str, value: bytes)` returns `None`
Copies a buffer into the message for given key. 
```python
myMessage.setBytes('VA', b'Hello World')
```

##### Function: `setString(key: str, value: str)` returns `None`
Sets a string value in the message for a given key.
```python
myMessage.setString('VA', 'Hello World')
```

#### Function: `getDouble(key: str, index: int)` returns `float`
Gets a double value in the message for a given key. The index is optional and defaults to 0.
```python
localVar = myMessage.getDouble('VA', 0)
```

##### Function: `getFloat(key: str, index: int)` returns `float`
Gets a float value in the message for a given key. The index is optional and defaults to 0.
```python
localVar = myMessage.getFloat('VA', 0)
```

##### Function: `getInt(key: str, index: int)` returns `int`
Gets an int value in the message for a given key. The index is optional and defaults to 0.
```python
localVar = myMessage.getInt('VA', 0)
```

##### Function: `getLong(key: str, index: int)` returns `int`
Gets a long value in the message for a given key. The index is optional and defaults to 0.
```python
localVar = myMessage.getLong('VA', 0)
```

##### Function: `getChar(key: str, index: int)` returns `bytes`
Gets a char value in the message for a given key. The index is optional and defaults to 0.
```python
localVar = myMessage.getChar('VA', 0)
```

##### Function: `getBytes(key: str)` returns `bytes`
Gets a bytes value in the message for a given key. The index is optional and defaults to 0.
```python
localVar = myMessage.getBytes('VA', 0)
```

##### Function: `getString(key: str)` returns `str`
Gets a string value in the message for a given key. The index is optional and defaults to 0.
```python
localVar = myMessage.getString('VA', 0)
```


## Publisher / Subscriber Channel

### Publisher

Used to broadcast a message to all subscribers.
Class: `MulticastPublisher` in library `ChannelMulticast`

#### Dependencies:
Must import the following:
```python
from DEFCOM.ChannelMulticast import MulticastPublisher
```

#### Constructor:

To create a publisher server, the object must be initialised with the path to the DEFCOM file:
```python
publisherObject = MulticastPublisher('path/to/defcom/file')
```

#### Methods:

##### Function: `getNewMessageObject(None)` returns `MessageStructure`

To create an outgoing message, a new message object must be created:
```python
requestObject = publisherObject.getNewMessageObject()
```

This can then be populated with the data to be sent as specified in Message Objects reference:
```python
requestObject.setFloat('VA',1.0,0)
requestObject.setChar('VB','a')
```

##### Function: `publish(MessageStructure message)` returns `None`
To send the message, the publisher must be called with the message object:
```python
publisherObject.publish(requestObject)
```



### Subscriber

Used to subscribe to publisher messages.
Class: `MulticastSubscriber` in library `ChannelMulticast`

#### Dependencies:
Must import the following:
```python
from DEFCOM.ChannelMulticast import MulticastSubscriber
```

#### Constructor:

A Subscriber object must be created with the path to the DEFCOM file:
```python
subscriberObject = MulticastSubscriber('path/to/defcom/file')
```

#### Methods:

##### Function: `subscribe(None)` returns `MessageStructure`

The client can await a message to be received from the server by calling the subscribe method:
```python
myMessage = subscriberObject.subscribe()
```

This will return a message object that can be extracted by the client process as specified in Message Objects reference:
```python
localVariable = myMessage.getChar('VA',1)
```

## Lossy Publisher / Subscriber Channel

### Publisher

Used to broadcast a message to all lossy subscribers.
These messages are not guaranteed to arrive, however, only the latest will be received.
Class: `MulticastPublisher` in library `ChannelMulticast`

#### Dependencies:
Must import the following:
```python
from DEFCOM.ChannelLossyCast import LossyCastPublisher
```

#### Constructor:

To create a publisher server, the object must be initialised with the path to the DEFCOM file:
```python
publisherObject = LossyCastPublisher('path/to/defcom/file')
```

#### Methods:
See the Publisher / Subscriber Channel section for more information.


### Subscriber
Used to subscribe to lossy publisher messages.
Class: `MulticastSubscriber` in library `ChannelMulticast`

#### Dependencies:
Must import the following:
```python
from DEFCOM.ChannelLossyCast import LossyCastSubscriber
```

#### Constructor:

A Subscriber object must be created with the path to the DEFCOM file:
```python
subscriberObject = LossyCastSubscriber('path/to/defcom/file')
```

#### Methods:
Refer to the Publisher / Subscriber Channel section for more information.


## Transactional Channel

### Server Channel

Used to service transactional requests from clients.
Class: `ServerChannel` in library `ChannelTransactional`

#### Dependencies:
Must import the following:
```python
from DEFCOM.ChannelTransactional import ServerChannel
```

#### Constructor:

To create a server channel, the object must be initialised with the path to the DEFCOM file and a hook to a message handler function:
```python

def myMessageHandler(request, response):
    ...

serverObject = ServerChannel('path/to/defcom/file', myMessageHandler)
```
The message handler function must have the following signature, and will be called on reception of a message:
```python
def myMessageHandler(request: MessageStructure, response: MessageStructure)
```


#### Methods:

##### Function: `start(None)` returns `None`

To start the server serving clients:
```python
serverObject.start()
```

### Client Channel

Used for clients to request and receive information from the server via initiating a transaction.
Class: `ClientChannel` in library `ChannelTransactional`

#### Dependencies:
Must import the following:
```python
from DEFCOM.ChannelTransactional import ClientChannel
```

#### Constructor:

To create a client channel, the object must be initialised with the path to the DEFCOM file:
```python
clientObject = ClientChannel('path/to/defcom/file')
```

#### Methods:

##### Function: `getNewRequestObject(None)` returns `MessageStructure`

To initiate an outgoing request, a new request object must be created:
```python
requestObject = clientObject.getNewRequestObject()
```

This can then be populated with the data to be sent as specified in Message Objects reference:
```python
requestObject.setFloat('VA',1.0,0)
requestObject.setChar('VB',b'a')
```

##### Function: `request(MessageStructure request)` returns `MessageStructure`

Sends the contents of request message to the server and synchronously returns the response message object.
```python
responseObject = clientObject.request(requestObject)
```

This can be extracted by the client process as specified in Message Objects reference:
```python
localVariable = responseObject.getChar('VA',1)
```