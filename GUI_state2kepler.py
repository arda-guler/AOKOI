import tkinter as tk
from tkinter import ttk
import numpy as np

from orbit_map import *
from kepler import *

def show_hide_date():
    if helio_or_terran.get() == "helio":
        date_label.grid_remove()
        date_entry.grid_remove()
    else:
        date_label.grid(row=4, column=0)
        date_entry.grid(row=4, column=1)

def compute_orbit():
    if helio_or_terran.get() == "helio":
        orbital_elements = state2kepler(eval(pos_entry.get("1.0", "end-1c")), eval(vel_entry.get("1.0", "end-1c")))
    else:
        earth_pos, earth_vel = get_earth_position_vector(date_entry.get("1.0", "end-1c"))
        earth_pos = np.array(earth_pos)
        earth_vel = n.parray(earth_vel)
        
        orbital_elements = state2kepler(np.array(eval(pos_entry.get("1.0", "end-1c"))) - earth_pos, np.array(eval(vel_entry.get("1.0", "end-1c"))) - earth_vel)
    
    result = ""
    for key, value in orbital_elements.items():
        result += f"{key}: {value}\n"
    result += "\n"

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, result)

    generate_orbits(orbital_elements["e"],
                    orbital_elements["arg_peri"],
                    orbital_elements["a"],
                    orbital_elements["lon_asc"],
                    orbital_elements["i"])

root = tk.Tk()
root.iconbitmap("astrometry.ico")
root.title("AOKOI - Keplerian Orbital Elements by State Vector")

pos_label = tk.Label(root, text="Position Vector (km)")
vel_label = tk.Label(root, text="Velocity Vector (km/s)")

helio_or_terran = tk.StringVar()
helio_or_terran.set("helio")
r1 = ttk.Radiobutton(root, text='Heliocentric', value='helio', variable=helio_or_terran, command=show_hide_date)
r2 = ttk.Radiobutton(root, text='Terran', value='terran', variable=helio_or_terran, command=show_hide_date)

pos_entry = tk.Text(root)
vel_entry = tk.Text(root)
pos_entry.config(width=20, height=1)
vel_entry.config(width=20, height=1)

pos_label.grid(row=1, column=0)
vel_label.grid(row=1, column=1)

pos_entry.grid(row=2, column=0)
vel_entry.grid(row=2, column=1)

r1.grid(row=3, column=0)
r2.grid(row=3, column=1)

date_label = tk.Label(root, text="Date and Time:")
date_entry = tk.Text(root)
date_entry.config(width=20, height=1)
date_label.grid(row=4, column=0)
date_entry.grid(row=4, column=1)
date_label.grid_remove()
date_entry.grid_remove()

compute_button = tk.Button(root, text="Compute", command=compute_orbit)
compute_button.config(width=15, height=1)
compute_button.grid(row=5, column=0, columnspan=2)

result_label = tk.Label(root, text="Computed Orbital Elements")
result_label.grid(row=6, column=0, columnspan=2)

result_text = tk.Text(root)
result_text.config(width=40, height=10)
result_text.grid(row=7, column=0, columnspan=2)

root.mainloop()
