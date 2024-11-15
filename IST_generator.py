# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 15:47:12 2024

@author: ros
"""

def generate_strain_data(max_strain, strain_rate, steps, filename=r"D:\Versuche schub\strain_data.txt"):
    time_values = []
    strain_values = []

    # Initial conditions
    current_strain = 0.0
    current_time = 0.0

    # Add the initial condition to the lists
    time_values.append(current_time)
    strain_values.append(current_strain)

    # Calculate the step size for strain values
    strain_step = max_strain / steps

    # Generate strain data with correct alternating pattern
    for i in range(1, 2 * steps + 1):
        # Calculate strain value for the current step
        if i <= steps:
            current_strain = round(i * strain_step, 2)
        elif i == steps+1:
            current_strain = round(steps * strain_step, 2)
        else:
            current_strain = round((2 * steps - i + 1) * strain_step, 2)

        # Alternate the sign based on the current step number
        if (i % 2) == 0:  # Switch sign every alternate step
            current_strain = -current_strain

        # Update time based on strain rate and add to the list
        current_time += (abs(current_strain) + abs(strain_values[-1])) / strain_rate
        time_values.append(round(current_time, 3))
        strain_values.append(round(current_strain, 2))
    
    # Add return to 0 strain
    current_time += strain_step / strain_rate
    time_values.append(round(current_time, 3))
    strain_values.append(round(current_strain + strain_step, 2))
    
    # Write the data to a text file
    with open(filename, "w") as file:
        # Add the header row
        file.write("-77777\t-77777\n")
        for t, s in zip(time_values, strain_values):
            file.write(f"{t:.3f}\t{s:.2f}\n")
    print(f"Data successfully written to {filename}")

# Example usage
# generate_strain_data(max_strain=1.5, strain_rate=0.1, steps=30)

# Console interaction to get input from the user
if __name__ == "__main__":
    try:
        # Prompt the user to enter values for max_strain, strain_rate, and steps
        max_strain = float(input("Enter the maximum strain in % (e.g., 1.0): "))
        strain_rate = float(input("Enter the strain rate in % per second (e.g., 0.1): "))
        steps = int(input("Enter the number of steps (e.g., 20 <-- must be an even number): "))
        if steps % 2 != 0:
            raise ValueError("The number of steps must be an even number.")
        # Optional: Prompt for the filename
        filename = input("Enter the output filename (default: C:\Temp\strain_data.txt): ")
        if not filename:
            filename = r"C:\Temp\strain_data.txt"
        
        # Generate the strain data with the user-provided values
        generate_strain_data(max_strain, strain_rate, steps, filename)
        
    except ValueError:
        print("Invalid input. Please enter numerical values for strain and strain rate, and an integer for steps.")