from herget import *
from observation import *
from parser import *

obs1 = MPC80Parser("     K17C54J 4C2017 01 30.40253 09 59 49.96 +02 06 21.9          22.8 i1     T09")
obs2 = MPC80Parser("     K17C54J 4C2017 02 02.47353 09 57 48.50 +02 20 57.1          23.0 r1     T09")

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
