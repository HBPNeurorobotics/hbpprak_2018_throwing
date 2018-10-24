# Imported Python Transfer Function
import numpy as np
import sensor_msgs.msg
from cv_bridge import CvBridge
import cv2
@nrp.MapRobotSubscriber("camera", Topic("/camera/image_raw", sensor_msgs.msg.Image))
@nrp.MapRobotPublisher('visualizer', Topic('/visualizer', sensor_msgs.msg.Image))
@nrp.Robot2Neuron()
def grab_image(t, camera, visualizer):
    # Take the image from the robot's left eye
    image_msg = camera.value
    if image_msg is not None:
        # Read the image into an array, mean over 3 colors, resize it for the network and flatten the result
        img = CvBridge().imgmsg_to_cv2(image_msg, "rgb8")

        # detect the blue cylinder
        kernel = np.ones((8,8),np.uint8)
        blue_channel = np.array(img[:,:,2])
        ret, mask = cv2.threshold(blue_channel, 90, 255, cv2.THRESH_BINARY)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        blue_channel = cv2.bitwise_and(blue_channel, blue_channel, mask=mask)
        ret, mask = cv2.threshold(blue_channel, 108, 255, cv2.THRESH_BINARY_INV)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        blue_channel = cv2.bitwise_and(blue_channel, blue_channel, mask=mask)
        mm = cv2.moments(blue_channel)
        # calculate x,y coordinate of center
        cX = int(mm["m10"] / mm["m00"])
        cY = int(mm["m01"] / mm["m00"])

        # display the centroid
        vis_img = np.array(blue_channel)
        cv2.circle(vis_img, (cX, cY), 5, 255, -1)
        msg_frame = CvBridge().cv2_to_imgmsg(vis_img, 'mono8')
        visualizer.send_message(msg_frame)
