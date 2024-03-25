import sys

from parser import *
from herget import *
from observation import *

def main(args):
    if len(args) > 1:
        input_filename = args[1]
    else:
        input_filename = input("Observation filename: ")

    if not input_filename:
        print("Input file not provided! Quitting...")
        return

    f = open(input_filename, "r")
    lines = f.readlines()

    obs1_line = lines[0]
    obs2_line = lines[-1]

    obs1 = MPC80Parser(obs1_line)
    obs2 = MPC80Parser(obs2_line)

    E1 = np.array(get_earth_position_vector(obs1.date_time.str_precise()))
    E2 = np.array(get_earth_position_vector(obs2.date_time.str_precise()))

    AU = 1.495979e8
    rs = []
    for i in range(300):
        rs.append(1 + i / 100 * AU)

    os = []
    for r in rs:
        oe = herget(obs1, obs2, r, [E1, E2])
        os.append(oe)

    for o in os:
        print(o)
        print("*************")

    input("Press Enter to quit.")

if __name__ == "__main__":
    main(sys.argv)
