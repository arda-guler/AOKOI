import sys

from parser import *
from herget import *
from observation import *

def main(args):
    r0 = 0.2
    ri = 0.01
    rf = 5
    input_filename = None
    tol = 0.0002

    current_argtype = "-f"
    if len(args) > 2:
        for arg in args:
            if arg in ["-f", "-r0", "-ri", "-rf", "-tol"]:
                current_argtype = arg
            else:
                if current_argtype == "-r0":
                    r0 = float(arg)
                elif current_argtype == "-ri":
                    ri = float(arg)
                elif current_argtype == "-rf":
                    rf = float(arg)
                elif current_argtype == "-f":
                    input_filename = arg
                elif current_argtype == "-tol":
                    tol = float(arg)
                else:
                    print("Invalid argtype. How the hell did this happen?")

    while not input_filename:
        input_filename = input("Observation filename: ")

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
    for i in range(int((rf - r0)/ri)):
        rs.append((r0 + i * ri) * AU)

    os = []
    for r in rs:
        oe = herget(obs1, obs2, r, [E1, E2], tol)
        os.append(oe)

    for o in os:
        print(o)
        print("*************")

    input("Press Enter to quit.")

if __name__ == "__main__":
    main(sys.argv)
