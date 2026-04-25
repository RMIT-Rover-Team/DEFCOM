from DEFCOM import ChannelTransactional

def handler(request: ChannelTransactional.MessageStructure, response: ChannelTransactional.MessageStructure):
    print("Received Request")
    print("One is: {} Two is: {}".format(request.getInt("One"), request.getFloat("Two")))
    
    print("Sending Response")
    response.setString("Three", "Hello!")

if __name__ == "__main__":
    channel = ChannelTransactional.ServerChannel("test/basicTest.defcom", handler)
    channel.start()
