from multiprocessing import Process, Pipe
from os import getpid
from datetime import datetime


def local_time(time_counter):
    return f' Lamport time is {time_counter}. Real time is {datetime.now()}'


def calculate_received_timestamp(received_time_stamp, time_counter):
    return max(received_time_stamp, time_counter) + 1


def event(proc_id, time_counter):
    time_counter += 1
    time = str(proc_id) + local_time(time_counter)
    print(f'Event happened in {time} time')
    return time_counter


def send_message(pipe, proc_id, time_counter):
    time_counter += 1
    pipe.send(('Empty shell', time_counter))
    print('Message sent from ' + str(proc_id) + "process in " + local_time(time_counter))
    return time_counter


def recv_message(pipe, proc_id, counter):
    message, timestamp = pipe.recv()
    counter = calculate_received_timestamp(timestamp, counter)
    print('Message received at ' + str(proc_id) + "process  in " + local_time(counter))
    return counter


def process_one(pipe12):
    pid = getpid()
    counter = 0
    counter = event(pid, counter)
    counter = send_message(pipe12, pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe12, pid, counter)
    counter = event(pid, counter)


def process_two(pipe21, pipe23):
    proc_id = getpid()
    counter = 0
    counter = recv_message(pipe21, proc_id, counter)
    counter = send_message(pipe21, proc_id, counter)
    counter = event(proc_id, counter)
    counter = recv_message(pipe23, proc_id, counter)


def process_three(pipe32):
    proc_id = getpid()
    counter = 0
    counter = event(proc_id, counter)
    counter = recv_message(pipe32, proc_id, counter)
    counter = send_message(pipe32, proc_id, counter)
    counter = event(proc_id, counter)
    counter = event(proc_id, counter)


if __name__ == '__main__':
    oneandtwo, twoandone = Pipe()
    twoandthree, threeandtwo = Pipe()

    process1 = Process(target=process_one,
                       args=(oneandtwo,))
    process2 = Process(target=process_two,
                       args=(twoandone, twoandthree))
    process3 = Process(target=process_three,
                       args=(threeandtwo,))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()
