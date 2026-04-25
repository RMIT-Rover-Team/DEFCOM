from DEFCOM import ChannelTransactional
import time

if __name__ == "__main__":
    channel = ChannelTransactional.ClientChannel("test/basicTest.defcom")
    
    counter = 0
    while True:
        request = channel.getNewRequestObject()
        request.setInt("One", counter)
        request.setFloat("Two", counter/2)
        response = channel.request(request)
        print("Ret: " + response.getString("Three"))

        counter += 1

        time.sleep(0.1)

    