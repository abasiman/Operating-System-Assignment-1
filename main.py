import threading
import queue
import random

# Constants
LOWER_NUM = 1
UPPER_NUM = 10000
MAX_COUNT = 10000
BUFFER_SIZE = 100

# Shared queue
buffer = queue.Queue(maxsize=BUFFER_SIZE)

# File names
ALL_NUMBERS_FILE = "all.txt"
ODD_NUMBERS_FILE = "odd.txt"
EVEN_NUMBERS_FILE = "even.txt"


def producer():
    with open(ALL_NUMBERS_FILE, 'w') as all_file:
        for _ in range(MAX_COUNT):
            num = random.randint(LOWER_NUM, UPPER_NUM)
            buffer.put(num)
            all_file.write(f"{num}\n")


def consumer_odd():
    with open(ODD_NUMBERS_FILE, 'w') as odd_file:
        while True:
            num = buffer.get()
            if num % 2 != 0:
                odd_file.write(f"{num}\n")
            buffer.task_done()


def consumer_even():
    with open(EVEN_NUMBERS_FILE, 'w') as even_file:
        while True:
            num = buffer.get()
            if num % 2 == 0:
                even_file.write(f"{num}\n")
            buffer.task_done()


producer_thread = threading.Thread(target=producer)
consumer_odd_thread = threading.Thread(target=consumer_odd)
consumer_even_thread = threading.Thread(target=consumer_even)

producer_thread.start()
consumer_odd_thread.start()
consumer_even_thread.start()


producer_thread.join()
