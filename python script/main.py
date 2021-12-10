# This code is tilting at specific points with a tilting function
# here we are tilting in between points

import cv2
import serial
# import time
import numpy as np

cap = cv2.VideoCapture(1)

# selecting the object we want to track
success, image = cap.read()
tracker = cv2.TrackerCSRT_create()
# cv2.legacy.TrackerMOSSE_create
# bbox = cv2.selectROI("Tracking", image, False)
# bbox = [229, 403, 30, 30]
# tracker.init(image, bbox)

# serial communication
arduino = serial.Serial(port='COM15', baudrate=115200, timeout=.1)


def drawBox(img, bbox):
    # bbox has four values (x,y, width, height)
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x, y), ((x+w), (y+h)), (255, 0, 255), 3, 1)
    cv2.putText(img, "Track", (75, 75), cv2.FONT_ITALIC, 0.7, (0, 255, 0), 2)
    print(x, " ", y)


def coordinates(x, y, vr, hr):
    t = y - vr
    d = y + vr
    l = x - hr
    r = x + hr
    return [t, d, l, r]


def write_read(x):
    print(x)
    arduino.write(bytes(x, 'utf-8'))
    # time.sleep(0.05)


# midpoint of bbox
def boxmid(bbox):
    return (int(bbox[0] + bbox[2] / 2), int(bbox[1] + bbox[3] / 2))


# function for the bot to go a little forward
def forward(bot):
    # main loop
    string = str(bot)
    while True:
        success, image = cap.read()
        success_tracker, bbox = tracker.update(image)
        box = boxmid(bbox)
        print(box, end=" ")

        if box[1] > 345:
            string = string + "U1"
            write_read(string)
        else:
            break
        string = str(bot)

        if success:
            drawBox(image, bbox)
        # write_read("1L0000")
        cv2.imshow("doing", image)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break


# function for the bot to go int the vertical axis
def inch_vs(t, d, l, r, bot):
    # main loop
    string = str(bot)
    while True:
        success, image = cap.read()
        success_tracker, bbox = tracker.update(image)
        box = boxmid(bbox)
        print(box, end=" ")

        if success:
            drawBox(image, bbox)

        if box[0] > r:
            string = string + "L1"
            write_read(string)
        elif box[0] < l:
            string = string + "R1"
            write_read(string)
        string = str(bot)

        if box[1] > d:
            string = string + "U2"
            write_read(string)
        elif box[1] < t:
            string = string + "D2"
            write_read(string)
        else:
            # time.sleep(0.1)
            string = string + "DO"
            for x in range(0, 100):
                write_read(string)
            break
        string = str(bot)
        string = string + "U0"
        write_read(string)
        string = str(bot)
        # write_read("1L0000")
        cv2.imshow("doing", image)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break


# function for the bot to go in the horizontal axis
def inch_hs(t, d, l, r, bot):
    string = str(bot)
    while True:
        success, image = cap.read()
        success_tracker, bbox = tracker.update(image)
        box = boxmid(bbox)
        print(box, end=" ")

        if success:
            drawBox(image, bbox)

        if box[1] >= d:
            string = string + "U1"
            write_read(string)
        elif box[1] <= t:
            string = string + "D1"
            write_read(string)
        string = str(bot)

        if box[0] <= l:
            string = string + "R2"
            write_read(string)
        elif box[0] >= r:
            string = string + "L2"
            write_read(string)
        else:
            string = string + "D2"
            for x in range(0, 100):
                write_read(string)
            break
        string = str(bot)
        string = string + "U0"
        write_read(string)
        string = str(bot)
        # write_read("1L0000")
        cv2.imshow("doing", image)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break


# adjusting
def inch_adj(t, d, l, r, bot):
    # main loop
    string = str(bot)
    while True:
        success, image = cap.read()
        success_tracker, bbox = tracker.update(image)
        box = boxmid(bbox)
        print(box, end=" ")

        if success:
            drawBox(image, bbox)

        if box[0] > r:
            string = string + "L3"
            write_read(string)
        elif box[0] < l:
            string = string + "R3"
            write_read(string)
        elif box[1] > d:
            string = string + "U3"
            write_read(string)
        elif box[1] < t:
            string = string + "D3"
            write_read(string)
        else:
            string = string + "U0"
            for i in range(0, 100):
                write_read(string)
            break
        string = str(bot)
        # write_read("1L0000")
        cv2.imshow("doing", image)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break


def tilting(bot):
    while True:
        timer = cv2.getTickCount()
        success, img = cap.read()

        # to resize the video
        # resize = cv2.resize(img, (640, 480))

        success, bbox = tracker.update(img)

        box = boxmid(bbox)

        if success:
            drawBox(image, bbox)

        string = str(bot)
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mask = np.zeros(grey.shape[:2], dtype="uint8")
        cv2.circle(mask, box, 8, 255, -1)
        masked = cv2.bitwise_and(grey, grey, mask=mask)
        edges = cv2.Canny(masked, 100, 200)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 10, minLineLength=1, maxLineGap=5)

        try:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                angle = (y1 - y2) / (x2 - x1)
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                break
            if angle > 0.15:
                string = string + "CW"
            elif angle < -0.15:
                string = string + "AW"
            else:
                string = string + "O0"
                for i in range(0, 1000):
                    write_read(string)
                break

        except:
            string = string + "N0"

        write_read(string)
        string = str(bot)

        '''
        if success:
            drawBox(img, bbox)
        else:
            cv2.putText(img, "Lost", (75, 75), cv2.FONT_ITALIC, 0.7, (0, 0, 255), 2)
        '''
        # to get frames per second
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        # cv2.putText(img, str(int(fps)), (75, 50), cv2.FONT_ITALIC, 0.7, (0, 0, 255), 2)

        keyCode = cv2.waitKey(1)
        cv2.imshow("doing", img)

        if cv2.waitKey(1) & 0xff == ord('q'):
            break


# FOR THE FIRST BOT
forward(1)
bot = 1

# going up mid
t, d, l, r = coordinates(229, 403, 10, 10)
inch_vs(t, d, l, r, bot)
print("went up")
tilting(1)

# going up final
t, d, l, r = coordinates(276, 169, 10, 10)
inch_vs(t, d, l, r, bot)
print("went up")
tilting(1)

# going left
t, d, l, r = coordinates(180, 146, 10, 10)
inch_hs(t, d, l, r, bot)
print("went left")
tilting(1)
# going left
t, d, l, r = coordinates(48, 147, 10, 10)
inch_hs(t, d, l, r, bot)
print("went left")
tilting(1)

# adjusting while throwing
t, d, l, r = coordinates(25, 159, 5, 5)
inch_adj(t, d, l, r, bot)
print("adjusted")
tilting(1)

# throwing
for i in range(0, 1000):
    write_read("1T0")
# tracker.init(image, bbox)
print("thrown")

# going left
t, d, l, r = coordinates(48, 147, 10, 10)
inch_hs(t, d, l, r, bot)
print("went left")
tilting(1)
# going left
t, d, l, r = coordinates(180, 146, 10, 10)
inch_hs(t, d, l, r, bot)
print("went left")
tilting(1)

# going down mid
t, d, l, r = coordinates(229, 403, 10, 10)
inch_vs(t, d, l, r, bot)
print("went up")
tilting(1)
# going down final
t, d, l, r = coordinates(269, 371, 10, 10)
inch_vs(t, d, l, r, bot)
print("went up")
tilting(1)

# adjust in the end
t, d, l, r = coordinates(243, 422, 5, 5)
inch_adj(t, d, l, r, bot)
print("adjusted")


# FOR THE SECOND BOT
bbox = [265, 400, 40, 40]
tracker.init(image, bbox)
bot = 2
forward(bot)
print("went forward")
tilting(2)

# going up
# t, d, l, r = coordinates(278, 294, 10, 10)
# inch_vs(t, d, l, r, bot)
# print("went up")
# tilting(2)
# going up
t, d, l, r = coordinates(284, 160, 10, 10)
inch_vs(t, d, l, r, bot)
print("went up")
tilting(2)

# going left
t, d, l, r = coordinates(168, 160, 10, 10)
inch_hs(t, d, l, r, bot)
print("went left")
tilting(2)
# going left
t, d, l, r = coordinates(82, 160, 10, 10)
inch_hs(t, d, l, r, bot)
print("went left")
tilting(2)

# adjusting while throwing
t, d, l, r = coordinates(50, 157, 5, 5)
print("adjusted")
tilting(2)

# throwing
for i in range(0, 1000):
    write_read("2T0")
# tracker.init(image, bbox)
print("thrown")

# going up (back to midpoint)
# going left
t, d, l, r = coordinates(168, 160, 10, 10)
inch_hs(t, d, l, r, bot)
print("went left")
tilting(2)
# going left
t, d, l, r = coordinates(284, 160, 10, 10)
inch_hs(t, d, l, r, bot)
print("went left")
tilting(2)

# going right (back to pos)
t, d, l, r = coordinates(275, 378, 10, 10)
inch_vs(t, d, l, r, bot)
print("went down")
tilting(2)

# adjust in the end
t, d, l, r = coordinates(291, 436, 5, 5)
inch_adj(t, d, l, r, bot)
print("adjusted")


# FOR THE THIRD BOT
bbox = [309, 412, 30, 30]
tracker.init(image, bbox)
bot = 3
forward(bot)

# going up 1
t, d, l, r = coordinates(349, 315, 10, 10)
inch_vs(t, d, l, r, bot)
print("went up")

tilting(3)

# going up 1
t, d, l, r = coordinates(353, 165, 10, 10)
inch_vs(t, d, l, r, bot)
print("went up")

tilting(3)

# going right 2
t, d, l, r = coordinates(471, 160, 10, 10)
inch_hs(t, d, l, r, bot)
print("went right")

tilting(3)

# going right 2
t, d, l, r = coordinates(564, 160, 10, 10)
inch_hs(t, d, l, r, bot)
print("went right")

tilting(3)

# adjusting while throwing
t, d, l, r = coordinates(590, 155, 5, 5)
inch_adj(t, d, l, r, bot)
print("adjusted")

tilting(3)

# throwing
for i in range(0, 2000):
    write_read("3T0")
# tracker.init(image, bbox)
print("thrown")

# going left 1
t, d, l, r = coordinates(470, 160, 10, 10)
inch_vs(t, d, l, r, bot)
print("went up")

tilting(3)

# going left 2 (back to midpoint)
t, d, l, r = coordinates(353, 165, 10, 10)
inch_hs(t, d, l, r, bot)
print("went left")

tilting(3)

# going down 1
t, d, l, r = coordinates(349, 287, 10, 10)
inch_vs(t, d, l, r, bot)
print("went down")

tilting(3)

# going down (back to pos)
t, d, l, r = coordinates(349, 372, 10, 10)
inch_vs(t, d, l, r, bot)
print("went down")

tilting(3)

# adjust in the end
t, d, l, r = coordinates(328, 433, 5, 5)
inch_adj(t, d, l, r, bot)
print("adjusted")


# FOR THE FORTH BOT
bbox = [350, 372, 30, 30]
tracker.init(image, bbox)
bot = 4
forward(4)

# going up
t = 132
d = 145
l = 338
r = 355
inch_vs(t, d, l, r, bot)
print("went up")

# going left
t = 132
d = 145
l = 557
r = 574
inch_hs(t, d, l, r, bot)
print("went left")

# adjusting while throwing
t = 150
d = 161
l = 571
r = 583
inch_adj(t, d, l, r, bot)
print("adjusted")

# throwing
for i in range(0, 1000):
    write_read("4T0")
# tracker.init(image, bbox)
print("thrown")

# going up (back to midpoint)
t = 132
d = 145
l = 338
r = 355
inch_hs(t, d, l, r, bot)
print("right")

# going right (back to pos)
t = 341
d = 356
l = 339
r = 356
inch_vs(t, d, l, r, bot)
print("went down")

# adjust in the end
t = 377
d = 389
l = 360
r = 373
inch_adj(t, d, l, r, bot)
print("adjusted")
