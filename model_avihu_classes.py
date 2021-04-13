import requests
import struct
import time
from socket import *
import threading
import logging
import os

f = open("config.txt", "r")
line_list = [line for line in f]
SERVER = str(line_list[31])
SERVER = SERVER.strip()

URL = str(line_list[33])
URL = URL.strip()

VIDEO_STREAMS_PATH = str(line_list[35])
VIDEO_STREAMS_PATH = VIDEO_STREAMS_PATH.strip()

VIDEO_STREAMS_SMOKE_PATH = str(line_list[37])
VIDEO_STREAMS_SMOKE_PATH = VIDEO_STREAMS_SMOKE_PATH.strip()

ERRORS = str(line_list[39])
ERRORS = ERRORS.strip()

WARNINGS = str(line_list[41])
WARNINGS = WARNINGS.strip()

INFO = str(line_list[43])
INFO = INFO.strip()

DEBUG = str(line_list[45])
DEBUG = DEBUG.strip()

MASSAGE_TIMEOUT = 0.07
SIZE_OF_MAX_LIST = 500
PERSONS = 1
NO_CROSS_ZONE = 2
PPE_HELMET = 3
WATCH_MAN_ALERT = 4
DEAD_MAN_ALERT = 5
SMOKE_AND_LEAKAGE = 6
LEAKAGE = 7
ANOMALY = 9
TRAINING = [10, 11, 12, 13, 14, 15]
AVG_FRAME_RATE = 25
list_of_words_mean_yes = ["Yes", "yes", "YES", "True", "true", "TRUE", "yap", "Yap", "YAP"]
HEADER = 64
PORT = 5055
# SERVER = gethostbyname(gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MASSAGE = "!DISSCONNECT"
f.close()


def read_camera_data_from_file(config_name):
    f = open(config_name, "r")
    line_list = [line for line in f]
    camera_list = []
    ACTIVE_CAMERAS = str(line_list[1])
    ACTIVE_CAMERAS_ID = ACTIVE_CAMERAS.split()
    ACTIVE_CAMERAS_ID = [int(num) for num in ACTIVE_CAMERAS_ID]

    EVENT = str(line_list[3])
    EVENT_TYPES = EVENT.split(",")
    EVENT_TYPES = [event.split() for event in EVENT_TYPES]
    EVENT_TYPES = [[convertEventIntToSTR(int(event)) for event in events] for events in EVENT_TYPES]

    SECONDS_TO_START = str(line_list[5])
    SECONDS_TO_START_EVENT = SECONDS_TO_START.split()
    SECONDS_TO_START_EVENT = [float(num) for num in SECONDS_TO_START_EVENT]

    NUMBER_OF_FRAMES = str(line_list[7])
    SIZE_OF_QUEUE = NUMBER_OF_FRAMES.split()
    SIZE_OF_QUEUE = [int(num) for num in SIZE_OF_QUEUE]

    TIME_AFTER_PUBLISH = str(line_list[9])
    TIMEOUT_AFTER_PUBLISH = TIME_AFTER_PUBLISH.split()
    TIMEOUT_AFTER_PUBLISH = [int(num) for num in TIMEOUT_AFTER_PUBLISH]

    TIME_CLOSE = str(line_list[11])
    TIME_TO_CLOSE = TIME_CLOSE.split()
    TIME_TO_CLOSE = [int(num) for num in TIME_TO_CLOSE]

    TIME_BETWEEN = str(line_list[13])
    TIME_BETWEEN_EVENTS = TIME_BETWEEN.split()
    TIME_BETWEEN_EVENTS = [int(num) for num in TIME_BETWEEN_EVENTS]

    WATCHMAN = str(line_list[15])
    WATCHMAN_TIME = WATCHMAN.split()
    WATCHMAN_TIME = [int(num) for num in WATCHMAN_TIME]

    MAX_SIZE = str(line_list[17])
    MAX_SIZE_OF_MAN = MAX_SIZE.split()
    MAX_SIZE_OF_MAN = [float(num) for num in MAX_SIZE_OF_MAN]

    MIN_SIZE = str(line_list[19])
    MIN_SIZE_OF_MAN = MIN_SIZE.split()
    MIN_SIZE_OF_MAN = [float(num) for num in MIN_SIZE_OF_MAN]

    S_INTREST_X = str(line_list[21])
    START_INTREST_AREA_X = S_INTREST_X.split()
    START_INTREST_AREA_X = [float(num) for num in START_INTREST_AREA_X]

    E_INTREST_X = str(line_list[23])
    END_INTREST_AREA_X = E_INTREST_X.split()
    END_INTREST_AREA_X = [float(num) for num in END_INTREST_AREA_X]

    S_INTREST_Y = str(line_list[25])
    START_INTREST_AREA_Y = S_INTREST_Y.split()
    START_INTREST_AREA_Y = [float(num) for num in START_INTREST_AREA_Y]

    E_INTREST_Y = str(line_list[27])
    END_INTREST_AREA_Y = E_INTREST_Y.split()
    END_INTREST_AREA_Y = [float(num) for num in END_INTREST_AREA_Y]

    D_RATIO = str(line_list[29])
    DETECTION_RATIO = D_RATIO.split()
    DETECTION_RATIO = [float(num) for num in DETECTION_RATIO]

    for i in range(len(ACTIVE_CAMERAS_ID)):
        camera_list.append(Camera(ACTIVE_CAMERAS_ID[i], EVENT_TYPES[i], SECONDS_TO_START_EVENT[i], SIZE_OF_QUEUE[i],
                                  TIMEOUT_AFTER_PUBLISH[i], TIME_TO_CLOSE[i], TIME_BETWEEN_EVENTS[i], WATCHMAN_TIME[i], MAX_SIZE_OF_MAN[i],
                                  MIN_SIZE_OF_MAN[i], START_INTREST_AREA_X[i], END_INTREST_AREA_X[i], START_INTREST_AREA_Y[i],
                                  END_INTREST_AREA_Y[i], DETECTION_RATIO[i]))

    f.close()
    return camera_list


# class Test:
#     def __init__(self):
#         self.end_of_video = 0
#         self.list_of_detections_times = list(list_of_detections_times)
#         self.true_counter = 0
#         self.false_counter = 0
#         self.finished = False
#         self.time_diffrences = list(time_diffrences)
#         self.lenght = 0
#         self.start_time_list = list(start_time_list)
#         self.end_time_list = list(end_time_list)
#         self.detections_time = tuple(start_time_list, end_time_list)
#
#     def __repr__(self):
#         return self
#
#     def updateTimeDiffrences(self, videos):
#         self.time_diffrences.append([self.detections_time[1][j] - self.detections_time[0][j] for j in range(videos)])
#
#     def updateLenght(self, obj):
#         self.lenght = obj
#
#     def addToStartList(self, obj):
#         self.start_time_list.append(obj)
#
#     def addToEndList(self, obj):
#         self.end_time_list.append(obj)
#
#     def addToTimeDiffrences(self, obj):
#         self.time_diffrences.append(obj)
#
#     def addToCounter(self, counter):
#         if counter:
#             self.true_counter += 1
#         else:
#             self.false_counter += 1


class Camera:
    def __init__(self, id, eventTypes, timeToPublish, queueSize, timeoutAfterPublish, timeToOpenAfterClose, timeBetweenEvents, timeForWatchman,
                 maxSize, minSize, x_start, x_end, y_start, y_end, detectionRatio):
        self.id = id
        self.eventTypes = eventTypes
        self.timeToPublish = timeToPublish
        self.queueSize = queueSize
        self.timeoutAfterPublish = timeoutAfterPublish
        self.timeToOpenAfterClose = timeToOpenAfterClose
        self.timeBetweenEvents = timeBetweenEvents
        self.timeForWatchman = timeForWatchman
        self.maxSize = maxSize
        self.minSize = minSize
        self.x_start = x_start
        self.x_end = x_end
        self.y_start = y_start
        self.y_end = y_end
        self.detectionRatio = detectionRatio
        self.timeOfLastClose = int
        self.typeOfLastClose = str
        self.timeoutCount = -1.0
        self.lastDetectionInCamera = time.time()
        self.WatchmanStarted = False

    def __repr__(self):
        return (f"camera {self.id} event_type are: {self.eventTypes}")


class Detection:
    def __init__(self, cameraId, objId, eventType, subClass, x, y):
        self.cameraId = cameraId
        self.objId = objId
        self.eventType = eventType
        self.subClass = subClass
        self.x = x
        self.y = y

    def __repr__(self):
        return (f"camera [{self.cameraId}] objId [{self.objId}] eventType [{self.eventType}] subClass [{self.subClass}] x {self.x} y {self.y}")


class Event:
    def __init__(self, cameraId, type, open = False):
        self.id = id
        self.originalCameraId = int
        self.type = type
        self.published = False
        self.lastUpdate = time.time()
        self.startTime = float
        self.subClassList = []
        self.realDetectionList = []
        self.cameraId = cameraId
        self.open = bool(open)
        self.publishedTime = float

    def __repr__(self):
        return (f"Event [{self.id}] type [{self.type}] camera [{self.cameraId}] open? [{self.open}]")

    def __eq__(self, other):
        return self.type == other.type and self.cameraId == other.cameraId


def is_print_on(print_level, list_of_yes):
    if print_level in list_of_yes:
        print_level = True
    else:
        print_level = False
    return print_level


ERRORS = is_print_on(ERRORS, list_of_words_mean_yes)
WARNINGS = is_print_on(WARNINGS, list_of_words_mean_yes)
INFO = is_print_on(INFO, list_of_words_mean_yes)
DEBUG = is_print_on(DEBUG, list_of_words_mean_yes)


class Finisihed_Error(Exception):
    pass


def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)


def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        try:
            sock.settimeout(MASSAGE_TIMEOUT)
        except IndexError:
            sock.settimeout(0.07)
        try:
            packet = sock.recv(n - len(data))
        except timeout:
            return None
        if not packet:
            return None
        data.extend(packet)
    return data


def handle_massage(client):
    # time.sleep(0.05)
    massage = recv_msg(client)
    # # logging.warning(f"massage read in {time.time()}")
    massage = str(massage)
    massage = massage.strip("bytearray(b'{" "}')")
    if DEBUG:
        logging.debug(massage)
    list_of_strings = massage.split("|")
    if DEBUG:
        logging.debug(list_of_strings)
    return list_of_strings


def convertIntrestArea(instrest_area):
    try:
        return float(instrest_area)
    except IndexError:
        return 0.0


def createEventInThread(event_type):
    threading.Thread(target=createEvent(event_type), args=()).start()


def createEvent(event_type):
    client = socket(AF_INET, SOCK_STREAM)
    client.connect(ADDR)
    camList = read_camera_data_from_file("config.txt")
    listOfDetections = []
    listOfTotalEvents = []
    listOfOpenEvents = []
    while True:
        list_of_strings = handle_massage(client)
        try:
            for string in list_of_strings:
                eventType = convertEventIntToSTR(event_type)
                detectionStatus = True
                anomalyTest = True
                str_list = string.split(" ")
                if DEBUG and str_list[0] != 'Non':
                    print(str_list)
                serialId = int(str_list[1])
                if int(str_list[2]) != 1:
                    eventType = int(str_list[2])
                objSubclass = int(str_list[3])
                objId = str_list[4]
                cameraId = int(str_list[0])
                if camList[cameraId].timeoutCount != -1:
                    if time.time() - float(camList[cameraId].timeoutCount) < camList[cameraId].timeToOpenAfterClose:
                        break
                eventTypes = camList[cameraId].eventTypes
                camId = camList[cameraId].id
                tempHistoryEventList = [event for event in listOfTotalEvents if event.cameraId == camId]
                for historyEvent in tempHistoryEventList:
                    if not historyEvent.open and time.time() - float(historyEvent.lastUpdate) < camList[cameraId].timeToOpenAfterClose:
                        break
                object_cluster_x = covertStrToFloatList(str_list[5])
                object_cluster_y = covertStrToFloatList(str_list[6])
                temp = checkBoundaries(camList[cameraId], object_cluster_x, object_cluster_y)
                camList[cameraId].lastDetectionInCamera = time.time()
                listOfTotalEvents = addObjectToList(listOfTotalEvents, Event(cameraId, eventType), 100)
                if not temp:
                    break
                else:
                    if temp == "Size_Issue":
                        if ("NO_CROSS_ZONE" in eventTypes or "PPE_HELMET" in eventTypes):
                            detectionStatus = False
                        else:
                            detectionStatus = True
                    else:
                        object_cluster_x, object_cluster_y = temp
                if eventType == "PERSONS":
                    if "NO_CROSS_ZONE" in eventTypes:
                        eventType = "NO_CROSS_ZONE"
                        tempDetection = Detection(camId, objId, eventType, objSubclass, object_cluster_x,
                                                  object_cluster_y)
                        listOfDetections = addObjectToList(listOfDetections, tempDetection, SIZE_OF_MAX_LIST)
                        listOfOpenEvents = handleDetection(camId, eventType, objSubclass, camList, cameraId, listOfOpenEvents, serialId, object_cluster_x, object_cluster_y, detectionStatus)
                    if "PPE_HELMET" in eventTypes:
                        eventType = "PPE_HELMET"
                        tempDetection = Detection(camId, objId, eventType, objSubclass, object_cluster_x,
                                                  object_cluster_y)
                        listOfDetections = addObjectToList(listOfDetections, tempDetection, SIZE_OF_MAX_LIST)
                        listOfOpenEvents = handleDetection(camId, eventType, objSubclass, camList, cameraId,
                                                            listOfOpenEvents, serialId, object_cluster_x,
                                                            object_cluster_y, detectionStatus)
                else:
                    tempDetection = Detection(camId, objId, eventType, objSubclass, object_cluster_x,
                                              object_cluster_y)
                    listOfDetections = addObjectToList(listOfDetections, tempDetection, SIZE_OF_MAX_LIST)
                    if "SMOKE" in eventTypes:
                        lastDetectionsInCameraList = [detection for detection in listOfDetections if detection.cameraId == camId and detection.eventType == "ANOMALY" and time.time() - detection.lastUpdate < 5]
                        #if len(lastDetectionsInCameraList) > 1:
                        listOfOpenEvents = handleDetection(camId, eventType, objSubclass, camList, cameraId,
                                                                listOfOpenEvents, serialId, object_cluster_x, object_cluster_y, detectionStatus)
                    if "ANOMALY" in eventTypes:
                        lastDetectionsInCameraList = [detection for detection in listOfDetections if detection.cameraId == camId and detection.eventType == "PERSONS" and time.time() - detection.lastUpdate < 5]
                        if len(lastDetectionsInCameraList) > 1:
                            anomalyTest = True
                        if not anomalyTest:
                            break
                        tempDetection = Detection(camId, objId, eventType, objSubclass, object_cluster_x,
                                                  object_cluster_y)
                        listOfDetections = addObjectToList(listOfDetections, tempDetection, SIZE_OF_MAX_LIST)
                        listOfOpenEvents = handleDetection(camId, eventType, objSubclass, camList, cameraId,
                                                            listOfOpenEvents, serialId, object_cluster_x,
                                                            object_cluster_y, detectionStatus)
                if DEBUG:
                    print(f"The camera is [{camId}] event type is [{eventType}]")
                listOfOpenEvents = handleNoDetction(camList, listOfOpenEvents)
        except ValueError and IndexError:
            listOfOpenEvents = handleNoDetction(camList, listOfOpenEvents)


def handleNoDetction(camList, listOfTotalEvents):
    counter = -1
    tempPublishedEventList = [tempEvent for tempEvent in listOfTotalEvents if tempEvent.published and tempEvent.type != "WATCHMAN"]
    for obj in tempPublishedEventList:
        if time.time() - obj.lastUpdate > camList[obj.originalCameraId].timeToPublish or time.time() - obj.publishedTime > \
                camList[obj.originalCameraId].timeoutAfterPublish:
            endShipEvent(obj.id)
            listOfTotalEvents.remove(obj)
            camList[obj.originalCameraId].timeoutCount = time.time()
    tempNotPublishedEventList = [tempEvent for tempEvent in listOfTotalEvents if not tempEvent.published and tempEvent.type != "WATCHMAN"]
    for obj in tempNotPublishedEventList:
        if time.time() - obj.startTime > camList[obj.originalCameraId].timeToPublish + 1:
            endShipEvent(obj.id)
            listOfTotalEvents.remove(obj)
    for camera in camList:
        counter += 1
        if "WATCHMAN" in camera.eventTypes and time.time() - camera.lastDetectionInCamera > camera.timeForWatchman:
            tempEvent = Event(camera.id, "WATCHMAN")
            if tempEvent in listOfTotalEvents:
                curr = listOfTotalEvents[listOfTotalEvents.index(tempEvent)]
                if time.time() - curr.startTime > camera.timeoutAfterPublish:
                    endShipEvent(curr.id)
                    curr.published = False
                    curr.open = False
                    camera.WatchmanStarted = False
                    listOfTotalEvents.remove(curr)
                    camera.timeoutCount = time.time()
                    break
                fire_and_forget(curr.id, 1, [0, 1], [0, 1])
                curr.lastUpdate = time.time()
            else:
                if time.time() - float(camera.timeoutCount) < camera.timeToOpenAfterClose:
                    break
                tempId = startShipEvent(tempEvent.cameraId, tempEvent.type)
                camera.WatchmanStarted = True
                if tempId != -1:
                    publishShipEvent(tempId)
                    tempEvent.cameraId = camera.id
                    tempEvent.originalCameraId = counter
                    tempEvent.id = tempId
                    tempEvent.open = True
                    tempEvent.published = True
                    tempEvent.lastUpdate = time.time()
                    tempEvent.startTime = time.time()
                    listOfTotalEvents.append(tempEvent)
    return listOfTotalEvents


def checkBoundaries(camera, object_cluster_x, object_cluster_y):
    detection_x_start = object_cluster_x[0][0]
    detection_x_end = object_cluster_x[0][1]
    detection_x_size = detection_x_end - detection_x_start
    detection_y_start = object_cluster_y[0][0]
    detection_y_end = object_cluster_y[0][1]
    detection_y_size = detection_y_end - detection_y_start
    detectionTotalArea = detection_x_size * detection_y_size
    #print(f" {detection_y_size} = {detection_y_end} - {detection_y_start}")
    if detection_x_start < float(camera.x_start):
        # print("off limits!")
        object_cluster_x[0][0] = camera.x_start
    if detection_x_end > float(camera.x_end):
        # print("off limits!")
        object_cluster_x[0][1] = camera.x_end
    if abs(object_cluster_x[0][1] - object_cluster_x[0][0]) <= 0.05:
        return False
    if detection_y_size < camera.minSize or detection_y_size > camera.maxSize:
        return "Size_Issue"
    if detection_y_start < float(camera.y_start):
        # print("off limits!")
        object_cluster_y[0][0] = camera.y_start
    if detection_y_end > float(camera.y_end):
        # print("off limits!")
        object_cluster_y[0][1] = camera.y_end
    if abs(object_cluster_y[0][1] - object_cluster_y[0][0]) <= 0.05:
        print("problem")
        return False
    detection_x_start = object_cluster_x[0][0]
    detection_x_end = object_cluster_x[0][1]
    detection_x_size = detection_x_end - detection_x_start
    detection_y_start = object_cluster_y[0][0]
    detection_y_end = object_cluster_y[0][1]
    detection_y_size = detection_y_end - detection_y_start
    newDetectionTotalArea = detection_x_size * detection_y_size
    if newDetectionTotalArea / detectionTotalArea < 0.8:
        return False
    return object_cluster_x, object_cluster_y


def handleDetection(camId, eventType, objSubclass, camList, cameraId, eventList, serialId, object_cluster_x, object_cluster_y, detectionStatus):
    #handle WATCHMAN
    if eventType != "ANOMALY":
        tempEvent = Event(camId, "WATCHMAN")
        if tempEvent in eventList:
            curr = eventList[eventList.index(Event(camId, eventType))]
            endShipEvent(curr.id)
            camList[cameraId].WatchmanStarted = False
            curr.open = False
            curr.published = False
            curr.originalCameraId = cameraId
            camList[cameraId].timeoutCount = time.time()
    tempEvent = Event(camId, eventType)
    if tempEvent in eventList:
        curr = eventList[eventList.index(Event(camId, eventType))]
        curr.subClassList = addObjectToList(curr.subClassList, objSubclass, camList[cameraId].queueSize)
        curr.realDetectionLIst = addObjectToList([], detectionStatus, camList[cameraId].queueSize)
        curr.lastUpdate = time.time()
        curr.originalCameraId = cameraId
        time_diff = time.time() - curr.startTime
        if time_diff > camList[cameraId].timeToPublish:
            if len(curr.subClassList) >= camList[cameraId].queueSize:
                if eventType != "PPE_HELMET":
                    if isItRealDetection(curr.realDetectionLIst):
                        if curr.published:
                            fire_and_forget(curr.id, serialId, object_cluster_x, object_cluster_y)
                            if DEBUG:
                                print(f"event {curr.id} has been sent in time {time.time()} in camera {camId}")
                        else:
                            publishShipEvent(curr.id)
                            curr.published = True
                            curr.publishedTime = time.time()
                            if DEBUG:
                                print(f"NO_CROSS_ZONE event published in camera {camId} in time {time.time()}")
                else:
                    if isItRealHelmetDetection(curr.subClassList, camList[cameraId]):
                        if curr.published:
                            fire_and_forget(curr.id, serialId, object_cluster_x, object_cluster_y)
                            if DEBUG:
                                print(f"event {curr.id} has been sent in time {time.time()} in camera {camId}")
                        else:
                            publishShipEvent(curr.id)
                            curr.published = True
                            curr.publishedTime = time.time()
                            if DEBUG:
                                print(f"NO_CROSS_ZONE event published in camera {camId} in time {time.time()}")
    else:
        if eventType != "PPE_HELMET":
            if detectionStatus:
                temp_id = startShipEvent(camId, eventType)
                if temp_id != -1:
                    tempEvent = Event(camId, eventType)
                    updateEvent(tempEvent, temp_id, objSubclass, cameraId)
                    eventList.append(tempEvent)
        else:
            if objSubclass == 2:
                temp_id = startShipEvent(camId, eventType)
                if temp_id != -1:
                    tempEvent = Event(camId, eventType)
                    updateEvent(tempEvent, temp_id, objSubclass, cameraId)
                    eventList.append(tempEvent)
    return eventList


def updateEvent(event, id, objSubclass, cameraId):
    event.id = id
    event.originalCameraId = cameraId
    event.open = True
    event.startTime = time.time()
    event.subClassList.append(objSubclass)
    event.lastUpdate = time.time()


def addObjectToList(listOfDetections, tempDetection, size):
    if len(listOfDetections) > size:
        listOfDetections.pop()
    listOfDetections.append(tempDetection)
    return listOfDetections


def covertStrToFloatList(str_object):
    temp_list = []
    list_object = []
    str_object = str_object.strip("[,]")
    str_object = str_object.split()
    str_object = [i.split(",") for i in str_object]
    for lst in str_object:
        for num in lst:
            temp_list.append(float(num))
        list_object.append(temp_list)
    return list_object


def convertEventIntToSTR(event_type):
    if event_type == PERSONS:
        return "PERSONS"
    elif event_type == NO_CROSS_ZONE:
        return "NO_CROSS_ZONE"
    elif event_type == PPE_HELMET:
        return "PPE_HELMET"
    elif event_type == SMOKE_AND_LEAKAGE:
        return "SMOKE"
    elif event_type == WATCH_MAN_ALERT:
        return "WATCHMAN"
    elif event_type == DEAD_MAN_ALERT:
        return "DEAD_MAN_ALERT"
    elif event_type == ANOMALY:
        return "ANOMALY"
    else:
        return None


def isItRealDetection(detection_queue):
    event_happening_counter = 0
    for detection in detection_queue:
        if detection:
            event_happening_counter += 1
        else:
            continue
    if (event_happening_counter) > len(detection_queue) / 2:
        return True
    return False


def isItRealHelmetDetection(detection_queue, camera):
    event_happening_counter = 0
    # Runs over 60 frames and counts in how many of them there is an event
    for detection in detection_queue:
        if detection == 2:
            event_happening_counter += 1
        else:
            continue
    # Check if at least half of the frames has an event
    try:
        score = float(len(detection_queue)) / 100
    except IndexError:
        score = float(20 / 100)
    try:
        score *= int(camera.detectionRatio)
    except IndexError:
        score *= int(camera.detectionRatio)
    if (event_happening_counter) > score:
        return True
    return False


def startShipEvent(cameraId, object_type):
    try:
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        string_to_send = """
        mutation{
            startShipEvent(event:{ 
              cameraUid: "%d"
              eventType: %s
            }){ 
            id
              }
            }
        """ % (cameraId, object_type)
        request = requests.post(URL, json={'query': string_to_send})
        if request.status_code != 200:
             logging.error(f"Query failed to run by returning code of {request.status_code}")
        else:
            try:
                if DEBUG:
                    logging.debug(request.json())
                event_id = request.json()['data']['startShipEvent']['id']
            except:
                event_id = None
                if WARNINGS:
                    logging.warning("Failed to get id from server")
            if INFO:
                print(f"start event {event_id} type {object_type} in camera {cameraId} in time {current_time}")
        if event_id != None:
            return event_id
        else:
            return -1
    except:
        startShipEvent(cameraId, object_type)


def publishShipEvent(event_id):
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    string_to_send = """
    mutation{
        publishShipEvent(eventId: %d, publish: true){ 
        id
      }
    }"""   % (event_id)
    request = requests.post(URL, json={'query': string_to_send})
    if request.status_code != 200:
         logging.error(f"Query failed to run by returning code of {request.status_code}")
    else:
        if DEBUG:
            logging.debug(request.json())
        if INFO:
            print(f"published event {event_id} in time {current_time}")


def sendDetection(eventId, serialId, object_cluster_x, object_cluster_y):
    try:
        if object_cluster_x and object_cluster_y:
            num_objects = len(object_cluster_x)
            if num_objects <= 0:
                return
            all_rects_str = ""
            if True:
                empty_rect_str = "{x1:%0.3f, y1:%0.3f x2:%0.3f, y2:%0.3f}" % (
                    0, 0, 0, 0)
                all_rects_str += empty_rect_str
            for i in range(num_objects):
                rect_str = "{x1:%0.3f, y1:%0.3f x2:%0.3f, y2:%0.3f}" % (
                    object_cluster_x[i][0],
                    object_cluster_y[i][0], object_cluster_x[i][1],
                    object_cluster_y[i][1])
                all_rects_str += rect_str
            string_to_send = """
            mutation{
                addShipDetection(event:{
                  eventId: %d
                  serialId: %d
                  boundingAreas: [%s]
                }){
                  id,
                  serialId,
                  boundingAreas {
                    x1, y1, x2, y2
                  }
                }
                }""" % (eventId, serialId, all_rects_str)
        else:
            string_to_send = """
            mutation
            {
                addShipDetection(event:{
                  eventId: %d
                  serialId: %d
                  boundingAreas: {x1:0.0,y1:0.0,x2:0.0,y2:0.0}
                }){
                  id,
                  boundingAreas {
                    x1, y1, x2, y2
                  }
                }
            }""" % (eventId)
        if DEBUG:
            logging.debug(string_to_send)
        request = requests.post(URL, json={'query': string_to_send})
        if request.status_code == 400:
            if object_cluster_x and object_cluster_y:
                string_to_send = """
                 mutation
                 {
                     addShipDetection(event:{
                       eventId: %d
                       boundingAreas: {x1:0.0,y1:0.0,x2:0.0,y2:0.0}
                     }){
                       id,
                       boundingAreas {
                         x1, y1, x2, y2
                       }
                     }
                 }""" % (eventId)
            else:
                string_to_send = """
                 mutation
                 {
                     addShipDetection(event:{
                       eventId: %d
                       boundingAreas: {x1:0.0,y1:0.0,x2:0.0,y2:0.0}
                     }){
                       id,
                       boundingAreas {
                         x1, y1, x2, y2
                       }
                     }
                 }""" % (eventId)
            if DEBUG:
                logging.debug(string_to_send)
            request = requests.post(URL, json={'query': string_to_send})
        if request.status_code != 200:
            if WARNINGS:
                logging.warning(f"Query failed to run by returning code of {request.status_code}")
    except:
        pass


def fire_and_forget(eventId, serialId, object_cluster_x, object_cluster_y):
    threading.Thread(target=sendDetection, args=(eventId, serialId, object_cluster_x, object_cluster_y)).start()


def endShipEvent(eventId):
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    try:
        time.sleep(0.5)
        sendDetection(eventId, 0, [], [])
        string_to_send = """
        mutation{
            endShipEvent(eventId: 
              %d
            ){ 
            id,
              }
            }
        """ % (eventId)
        request = requests.post(URL, json={'query': string_to_send})
        if INFO:
            print(f"close event {eventId} in time {current_time}")
        if request.status_code != 200:
            if WARNINGS:
                logging.warning(f"Query failed to run by returning code of {request.status_code}")
    except:
        endShipEvent(eventId)


def test(eventType):
    client = socket(AF_INET, SOCK_STREAM)
    client.connect(ADDR)
    file_exist = False
    list_of_videos_names = []
    list_of_tagging_files = []
    list_of_detections_times = []
    true_counter = []
    finished_list = []
    false_counter = []
    lenght_per_video = []
    time_diffrence_per_camera = []
    subclass_list = []
    list_of_subclass = []
    helmet_false_counter = []
    helmet_true_counter = []
    noDetectionsList = []
    eventType = convertEventIntToSTR(eventType)
    test_start_time = time.time()
    # max_lenght_of_video = input("please enter the longest video lenght in seconds")
    if eventType == "SMOKE":
        stream_files_file = open(VIDEO_STREAMS_SMOKE_PATH, "r")
        helmets = False
    else:
        stream_files_file = open(VIDEO_STREAMS_PATH, "r")
        helmets = True
    names_of_videos_temp = stream_files_file.readlines()
    # [names_of_videos_temp.pop(k) for k in range(len(names_of_videos_temp)) if names_of_videos_temp[k] == "\n"]
    names_of_videos_temp.pop(0)
    names_of_videos = [s[:-1] for s in names_of_videos_temp if s[-1] == "\n" and s[0] != "\n"]
    if len(names_of_videos_temp) > len(names_of_videos) and names_of_videos_temp[-1] != "\n":
        names_of_videos.append(names_of_videos_temp[-1])
    list_of_videos_names.append([os.path.basename(full_path) for full_path in names_of_videos])
    for i in range(len(list_of_videos_names[0])):
        list_of_start_time = []
        list_of_end_time = []
        list_of_line_splitted = []
        subclass_list = []
        true_counter.append(0)
        finished_list.append(False)
        false_counter.append(0)
        helmet_false_counter.append(0)
        helmet_true_counter.append(0)
        time_diffrence_per_camera.append([])
        path = os.path.dirname(names_of_videos[i])
        list_of_videos_names[0][i] += ".txt"
        try:
            list_of_tagging_files.append(open(str(path) + '/' + str(list_of_videos_names[0][i]), "r"))
            file_exist = True
            temp = list_of_tagging_files[i].readline()
            temp_list = temp.split(':')
            lenght = int(temp_list[0]) * 60 + float(temp_list[1])
            lenght *= AVG_FRAME_RATE
            lenght_per_video.append(lenght)
            for line in list_of_tagging_files[i].readlines():
                if line != "\n":
                    line_splitted = line.split()
                    list_of_line_splitted.append(line_splitted)
                    s_time = line_splitted[0]
                    start_time_l = s_time.split(':')
                    start_time = int(start_time_l[0]) * 60 + float(start_time_l[1])
                    start_time *= AVG_FRAME_RATE
                    list_of_start_time.append(start_time)
                    e_time = line_splitted[1]
                    end_time_l = e_time.split(':')
                    end_time = int(end_time_l[0]) * 60 + float(end_time_l[1])
                    end_time *= AVG_FRAME_RATE
                    list_of_end_time.append(end_time)
                    if helmets:
                        try:
                            subclass = line_splitted[2]
                            subclass_list.append(int(subclass))
                        except IndexError:
                            print(f"no subclass, check text file {list_of_tagging_files[i]}")
                            subclass = 0
                else:
                    break
        except FileNotFoundError:
            if not str(list_of_videos_names[0][i]) == ".txt":
                logging.warning(f"There is no file named {list_of_videos_names[0][i]}")
            file_exist = False
            list_of_start_time.append(0)
            list_of_end_time.append(0)
            lenght_per_video.append(1)
        if len(list_of_start_time) == 0 and len(list_of_end_time) == 0:
            noDetectionsList.append(True)
        else:
            noDetectionsList.append(False)
        list_of_detections_times.append((list_of_start_time, list_of_end_time))
        list_of_subclass.append(subclass_list)
        try:
            [time_diffrence_per_camera[i].append(
                (list_of_detections_times[i][1][j] - list_of_detections_times[i][0][j])) for j in
             range(len(list_of_videos_names[0]))]
        except:
            pass
    [fl.close() for fl in list_of_tagging_files]
    stream_files_file.close()
    print(f"The lenghts of the videos are: {lenght_per_video}")
    while True:
        list_of_strings = handle_massage(client)
        try:
            for string in list_of_strings:
                if file_exist:
                    str_list = string.split(" ")
                    if DEBUG and str_list[0] != 'Non':
                        print(str_list)
                    serialId = int(str_list[1])
                    objId = int(str_list[2])
                    objSubclass = int(str_list[3])
                    cameraId = int(str_list[0])
                    for i in range(len(finished_list)):
                        print(serialId)
                        if serialId > lenght_per_video[i] and not finished_list[i]:
                            print(f"{list_of_videos_names[0][i]} has finished")
                            finished_list[i] = True
                    if all(finished_list):
                        test_summary(true_counter, false_counter, helmet_true_counter, helmet_false_counter, time_diffrence_per_camera, list_of_videos_names, helmets)
                    counter = 0
                    for j in range(len(list_of_detections_times[cameraId])):
                        if objId == 1:
                            if noDetectionsList[cameraId] and not finished_list[cameraId]:
                                false_counter[cameraId] += 1
                                break
                            if serialId >= list_of_detections_times[cameraId][1][j] + 15 and counter < len(list_of_detections_times[cameraId]):
                                counter += 1
                                continue
                            if serialId >= list_of_detections_times[cameraId][0][j] and serialId <= list_of_detections_times[cameraId][1][j]:
                                if not finished_list[cameraId]:
                                    true_counter[cameraId] += 1
                                    if helmets:
                                        if objSubclass == 2 and int(list_of_subclass[cameraId][j]) == 0:
                                            helmet_true_counter[cameraId] += 1
                                        elif objSubclass == 1 and int(list_of_subclass[cameraId][j]) == 1:
                                            helmet_true_counter[cameraId] += 1
                                        elif objSubclass == 0:
                                            pass
                                        else:
                                            helmet_false_counter[cameraId] += 1
                                break
                            else:
                                if not finished_list[cameraId]:
                                    if serialId < list_of_detections_times[cameraId][0][j] - 25 or serialId > \
                                            list_of_detections_times[cameraId][1][j] + 25:
                                        false_counter[cameraId] += 1
        except ValueError and IndexError:
            for i in range(len(finished_list)):
                if (time.time() - test_start_time) > lenght_per_video[i] * 12 + 2 and not finished_list[i]:
                    finished_list[i] = True
                    print(f"{list_of_videos_names[0][i]} has finished")
            if all(finished_list):
                test_summary(true_counter, false_counter, helmet_true_counter, helmet_false_counter, time_diffrence_per_camera, list_of_videos_names, helmets)


def test_summary(true_counter, false_counter, helmet_true_counter, helmet_false_counter, time_diffrence_per_camera, list_of_videos_names, helmets):
    test_result_file = open("tag_test_file.txt", "w")
    total_detections_list = []
    total_helmet_detection_list = []
    for i in range(len(true_counter)):
        total_detections_list.append(true_counter[i] + false_counter[i])
        total_helmet_detection_list.append(helmet_true_counter[i] + helmet_false_counter[i])
        try:
            false_ratio = (false_counter[i] / total_detections_list[i]) * 100
        except ZeroDivisionError:
            false_ratio = (false_counter[i] / (total_detections_list[i] + 1)) * 100
        try:
            true_ratio = (true_counter[i] / sum(time_diffrence_per_camera[i])) * 100
        except ZeroDivisionError:
            true_ratio = (true_counter[i] / (sum(time_diffrence_per_camera[i]) + 1)) * 100
        if helmets:
            try:
                helmet_false_ratio = (helmet_false_counter[i] / total_helmet_detection_list[i]) * 100
            except ZeroDivisionError:
                helmet_false_ratio = (helmet_false_counter[i] / (
                        total_helmet_detection_list[i] + 1)) * 100
            try:
                helmet_true_ratio = (helmet_true_counter[i] / sum(time_diffrence_per_camera[i])) * 100
            except ZeroDivisionError:
                helmet_true_ratio = (helmet_true_counter[i] / (sum(time_diffrence_per_camera[i]) + 1)) * 100
        test_result_file.write(f"For video {list_of_videos_names[0][i]}: \n")
        test_result_file.write(f"Number of true detections is: {true_counter[i]} \n")
        test_result_file.write(f"Number of false detections is: {false_counter[i]} \n")
        test_result_file.write(f"The true detection ratio is: {true_ratio} \n")
        if helmets:
            test_result_file.write(f"The false detection ratio is: {false_ratio} \n")
        else:
            test_result_file.write(f"The false detection ratio is: {false_ratio} \n\n")
        if helmets:
            test_result_file.write(
                f"Number of helmet true detections is: {helmet_true_counter[i]} \n")
            test_result_file.write(
                f"Number of helmet false detections is: {helmet_false_counter[i]} \n")
            test_result_file.write(
                f"The true helmet detection ratio is: {helmet_true_ratio} \n")
            test_result_file.write(
                f"The false helmet detection ratio is: {helmet_false_ratio} \n\n")
    test_result_file.close()
    print("finished the test, see results in the file")
    raise Finisihed_Error

test(1)
f.close()


