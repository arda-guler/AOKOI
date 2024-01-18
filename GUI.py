import tkinter as tk

from gauss_solver import *
from orbit_map import *

# I named this 'dummy_function' while developing the GUI
# and here it still stands to this day
#
# it takes the entry field inputs and calls the orbit computing function
def dummy_function(*args):
    for idx_arg, arg in enumerate(args):
        if idx_arg != 7 and idx_arg != 15 and idx_arg != 23:
            try:
                float(arg)
            except:
                return "Could not convert input to float.\nPlease check your inputs."
            
    RA1 = RightAscension(float(args[0]), float(args[1]), float(args[2]))
    DEC1 = Declination(float(args[3]), float(args[4]), float(args[5]))
    time1 = float(args[6])
    datetime1 = args[7]

    RA2 = RightAscension(float(args[8]), float(args[9]), float(args[10]))
    DEC2 = Declination(float(args[11]), float(args[12]), float(args[13]))
    time2 = float(args[14])
    datetime2 = args[15]

    RA3 = RightAscension(float(args[16]), float(args[17]), float(args[18]))
    DEC3 = Declination(float(args[19]), float(args[20]), float(args[21]))
    time3 = float(args[22])
    datetime3 = args[23]

    obs1 = Observation(RA1, DEC1, time1, datetime1)
    obs2 = Observation(RA2, DEC2, time2, datetime2)
    obs3 = Observation(RA3, DEC3, time3, datetime3)

    orbital_elements = gauss(obs1, obs2, obs3)
    generate_orbits(orbital_elements["e"], orbital_elements["arg_peri"],
                    orbital_elements["a"], orbital_elements["lon_asc"],
                    orbital_elements["i"])

    result = ""
    for key, value in orbital_elements.items():
       result += f"{key}: {value}\n"
    
    return f"Orbital Elements:\n\n{result}"

def on_button_click():
    entry_values = [entry.get() for row in entry_rows for entry in row]

    # Check if all entry fields are filled
    if all(entry_values):
        result = dummy_function(*entry_values)
    else:
        result = "Please enter all inputs!"

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, result)

root = tk.Tk()
root.iconbitmap("astrometry.ico")
root.title("AOKOI - Preliminary Minor Planet Orbit Determinator (Gauss)")

# Creating three rows of entry fields with labels
entry_rows = []
for i in range(3):
    row_label = tk.Label(root, text=f"Observation {i + 1}:")
    row_label.grid(row=i, column=0)

    entry_labels = ["RA (h, m, s):", "DEC (deg, m, s):", "dt (s):", "datetime (JPL Horizons API Format):"]

    entry_fields = []

    for j, label_text in enumerate(entry_labels, start=1):
        entry_label = tk.Label(root, text=label_text)
        entry_label.grid(row=i, column=(j - 1) * 4 + 1)

        entry_field = tk.Entry(root)
        entry_field.grid(row=i, column=(j - 1) * 4 + 2)

        entry_fields.append(entry_field)

        if j < 3:
            for k in range(2):
                extra_entry_field = tk.Entry(root)
                extra_entry_field.grid(row=i, column=(j - 1) * 4 + 2 + k + 1)
                entry_fields.append(extra_entry_field)

        for idx_e, e in enumerate(entry_fields):
            if idx_e < 7:
                e.config(width=5)

    entry_rows.append(entry_fields)

# Large text field with a label
result_label = tk.Label(root, text="Computation Results:")
result_label.grid(row=3, column=0, columnspan=20)

result_text = tk.Text(root, height=8, width=100)
result_text.grid(row=4, column=0, columnspan=20)

welcome_msg = "Preliminary Orbit Determination Software for Heliocentric Keplerian orbits.\n"
welcome_msg += "Uses Gauss' orbit determination method - requires three observation points.\n"
welcome_msg += "Results are PRELIMINARY and will likely have large errors, depending on\n"
welcome_msg += "observation interval (arc length).\n"
welcome_msg += "This program doesn't calculate residuals and errors (not yet anyway.)\n"
welcome_msg += "No guarantees on accuracy (or correct implementation to begin with). Untested (so far).\n"
welcome_msg += "\n"
welcome_msg += "https://github.com/arda-guler/AOKOI"
result_text.delete(1.0, tk.END)
result_text.insert(tk.END, welcome_msg)

# Button to call the dummy function with the input values
button = tk.Button(root, text="Compute Orbit", command=on_button_click)
button.grid(row=5, column=4, columnspan=9)

root.mainloop()
