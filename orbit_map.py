import json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.lines import Line2D
import numpy as np

class Planet:
    def __init__(self, name, a, e, i, OMG, o, L):
        self.name = name
        self.a = a
        self.e = e
        self.i = i
        self.OMG = OMG # big omega
        self.o = o # small omega with a tilda
        self.L = L

def readJSON(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print("Error: File", filename, "not found!")
    except json.JSONDecodeError as e:
        print("Error: Failed to decode JSON in", filename, "\n", e)

def generate_orbits(eccentricity, argument_perihelion, semimajor_axis, ascending_node, inclination, poly=1000):
    planets = []
    # print("Reading JSON major planet data...")
    planet_data = readJSON("orbits/planets.json")
    for p in planet_data:
        name = p["name"]
        a = float(p["a"])
        e = float(p["e"])
        i = float(p["i"])
        OMG = float(p["Omega"])
        o = float(p["-omega"])
        L = float(p["L"])

        new_planet = Planet(name, a, e, i, OMG, o, L)
        planets.append(new_planet)

    planet_colors =\
                  ["gray",
                   "sandybrown",
                   "royalblue",
                   "firebrick",
                   "peru",
                   "moccasin",
                   "powderblue",
                   "slateblue"]
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    argument_perihelion = np.deg2rad(argument_perihelion)
    ascending_node = np.deg2rad(ascending_node)
    inclination = np.deg2rad(inclination)
    
    true_anomaly = np.linspace(0, 2 * np.pi, poly)

    r = (semimajor_axis * (1 - eccentricity**2)) / (1 + eccentricity * np.cos(true_anomaly))

    x = r * np.cos(true_anomaly)
    y = r * np.sin(true_anomaly)
    z = np.zeros_like(true_anomaly)

    x_rot = x * (np.cos(argument_perihelion) * np.cos(ascending_node) - np.sin(argument_perihelion) * np.sin(ascending_node) * np.cos(inclination)) - \
            y * (np.sin(argument_perihelion) * np.cos(ascending_node) + np.cos(argument_perihelion) * np.sin(ascending_node) * np.cos(inclination))

    y_rot = x * (np.cos(argument_perihelion) * np.sin(ascending_node) + np.sin(argument_perihelion) * np.cos(ascending_node) * np.cos(inclination)) + \
            y * (np.cos(argument_perihelion) * np.cos(ascending_node) - np.sin(argument_perihelion) * np.sin(ascending_node) * np.cos(inclination))

    z_rot = x * np.sin(argument_perihelion) * np.sin(inclination) + y * np.sin(argument_perihelion) * np.sin(inclination)

    color = "k"

    ax.plot(x_rot, y_rot, z_rot, color=color)

    for p_idx in range(len(planets)):
        p = planets[p_idx]
        
        eccentricity = p.e
        argument_perihelion = np.radians(p.o)
        semimajor_axis = p.a
        ascending_node = np.radians(p.OMG)
        inclination = np.radians(p.i)
        
        true_anomaly = np.linspace(0, 2 * np.pi, 1000)

        r = (semimajor_axis * (1 - eccentricity**2)) / (1 + eccentricity * np.cos(true_anomaly))

        x = r * np.cos(true_anomaly)
        y = r * np.sin(true_anomaly)
        z = np.zeros_like(true_anomaly)

        x_rot = x * (np.cos(argument_perihelion) * np.cos(ascending_node) - np.sin(argument_perihelion) * np.sin(ascending_node) * np.cos(inclination)) - \
                y * (np.sin(argument_perihelion) * np.cos(ascending_node) + np.cos(argument_perihelion) * np.sin(ascending_node) * np.cos(inclination))

        y_rot = x * (np.cos(argument_perihelion) * np.sin(ascending_node) + np.sin(argument_perihelion) * np.cos(ascending_node) * np.cos(inclination)) + \
                y * (np.cos(argument_perihelion) * np.cos(ascending_node) - np.sin(argument_perihelion) * np.sin(ascending_node) * np.cos(inclination))

        z_rot = x * np.sin(argument_perihelion) * np.sin(inclination) + y * np.sin(argument_perihelion) * np.sin(inclination)

        color = planet_colors[p_idx]
        ax.plot(x_rot, y_rot, z_rot, color=color, lw=3)

    custom_legend = [Line2D([0], [0], color="olive", lw=1),
                     Line2D([0], [0], color="cyan", lw=1),
                     Line2D([0], [0], color="red", lw=1),
                     Line2D([0], [0], color="orange", lw=1),
                     Line2D([0], [0], color="purple", lw=1),
                     Line2D([0], [0], color="pink", lw=1),
                     Line2D([0], [0], color="gray", lw=1),
                     Line2D([0], [0], color="green", lw=1),
                     Line2D([0], [0], color="brown", lw=1),
                     Line2D([0], [0], color="aquamarine", lw=1),
                     Line2D([0], [0], color="navy", lw=1)]
    
    ax.legend(custom_legend, ['Atira', 'Aten', 'Apollo', 'Amor',
                              'Obj. w/ peri. dist. < 1.665 AU',
                              'Hungaria', 'MBA', 'Phocaea',
                              'Hilda', 'Jupiter Trojan', 'Distant Object'])
    
    ax.scatter(0, 0, 0, color='yellow', label='Sol Barycenter')
    
    ax.set_title('Orbit Plot')
    ax.set_xlabel('X (AU)')
    ax.set_ylabel('Y (AU)')
    ax.set_zlabel('Z (AU)')
    ax.set_xlim(-50, 50) # set map limits here
    ax.set_ylim(-50, 50)
    ax.set_zlim(-50, 50)
    plt.show()
