#Publish code
from DEFCOM import ChannelLossyCast
import time

if __name__ == "__main__":
    publisher = ChannelLossyCast.LossyCastPublisher("test/basicTest.defcom")

    count = 0
    while True:
        message = publisher.getNewMessageObject()
        message.setInt("One", count)
        message.setFloat("Two",count**0.5)

        print("Sending message count={}".format(count))
        publisher.publish(message)
        count += 1
        time.sleep(0.3)