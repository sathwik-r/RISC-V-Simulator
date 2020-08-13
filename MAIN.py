import subprocess

print('\n')
print("::::::::::  RISC V SIMULATOR :::::::::::::")
print('\n')

# cmd = input("Enable cache ? (y/n) ")

op = input("Press 1 for GUI and 2 to continue in terminal: ")

if op == "2":  # in terminal
    print(":: Modes ::")
    print("1) Without Pipelining")
    print("2) With Pipelining but no data forwarding")
    print("3) With Pipelining and data forwarding")
    print('\n')

    mode = input("Enter Mode 1/2/3: ")

    if mode != "1":
        knob1 = input("Enable 1-bit branch predictor ? (y/n) ")

    if mode == "1":
        subprocess.call(['python3', 'unpipelined.py'])  # unpipelined
    elif mode == "2" and knob1 != "y":
        subprocess.call(['python3', 'stall_no_dataforwarding.py'])  # pipline without datafrwd
    elif mode == "3" and knob1 != "y":
        subprocess.call(['python3', 'stalling_dataforwarding.py'])  # pipline with dataforwd
    elif knob1 == "y":
        subprocess.call(['python3', 'pipeline_predictor.py'])  # pipeline with 1 bit predictor


elif op == "1":  # in GUI
    subprocess.call(['python3', 'simulator_front_end.py'])
