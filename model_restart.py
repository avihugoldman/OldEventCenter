import time
import model_avihu_classes


def try_to_connect(restart_counter, event_type):
    try:
        if event_type == 10:
            model_avihu_classes.test(event_type)
        elif event_type == 11:
            model_avihu_classes.test(6)
        elif event_type == 12:
            model_avihu_classes.test(7)
        else:
            model_avihu_classes.createEventInThread(event_type)
        restart_counter = 0
        exit(0)
    except model_avihu_classes.Finisihed_Error:
        time.sleep(1000)
        exit(0)
    except:
        time.sleep(1)
        print("Model has been crashed from some reason, trying to reconnect")
        restart_counter += 1
        if restart_counter < 1000:
            try_to_connect(restart_counter, event_type)
        else:
            print("Failed to reconnect")
            exit(0)

while True:
    trainingType = None
    ccc = input("Please choose event type: (p: PERSONS s: SMOKE AND LEAKAGE t:test training q: quit) ? ")
    if (ccc == 'p'):
        try_to_connect(0, 1)
    if (ccc == 's'):
        try_to_connect(0, 6)
    if (ccc == "t"):
        c = input("What do you want to test: (p: PERSONS s: SMOKE l: LEAKAGE : ")
        if c == 'p':
            try_to_connect(0, 10)
        elif c == 's':
            try_to_connect(0, 11)
        elif c == 'l':
            try_to_connect(0, 12)
        else:
            try_to_connect(0, 10)
    if (ccc == 'q'):
        print("closing program")
        exit(0)











