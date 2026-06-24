#Publish code
from DEFCOM import ChannelLossyCast
import time

if __name__ == "__main__":
    subscriber = ChannelLossyCast.LossyCastSubscriber("test/basicTest.defcom")

    while True:
        message = subscriber.subscribe()
        print("One is: {} Two is: {}".format(message.getInt("One"), message.getFloat("Two")))
