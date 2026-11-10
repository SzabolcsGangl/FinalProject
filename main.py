import numpy as np
import os
import importlib.util
import matplotlib.pyplot as plt

body1 = {
    "weight": 5.972e24,  # Mass of the Earth in kg
    "position": np.array([0, 0, 0]),  # Position of the Earth in meters
    "velocity": np.array([0, 0, 0]),  # Velocity of the Earth in m/s
}

body2 = {
    "weight": 7.348e22,  # Mass of the Moon in kg
    "position": np.array([384400000, 0, 0]),  # Position of the Moon in meters
    "velocity": np.array([0, 1022, 0]),  # Velocity of the Moon in m/s
}

body3 = {
    "weight": 1.989e30,  # Mass of the Sun in kg
    "position": np.array([149600000000, 0, 0]),  # Position of the Sun in meters
    "velocity": np.array([0, 0, 0]),  # Velocity of the Sun in m/s
}

bodies = [body1, body2, body3]

dt = 60 * 60  # Time step in seconds (1 hour)
total_time = 60 * 60 * 24 * 365  # Total simulation time in seconds (1 year)

solvers = os.listdir("solvers")
print("Available solvers:")
for i, solver in enumerate(solvers):
    print(f"[{i + 1}] - {solver}")

print("Select a solver by entering its number:")
selected_solver_index = int(input()) - 1
selected_solver_file = solvers[selected_solver_index]
spec = importlib.util.spec_from_file_location("solver_module", f"solvers/{selected_solver_file}")
solver_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(solver_module)
print(f"Selected solver: {solver_module.name()}")

positions = []
velocities = []

for t in range(0, total_time, dt):
    solver_module.solve(bodies, dt)

    positions.append([body["position"].copy() for body in bodies])
    velocities.append([body["velocity"].copy() for body in bodies])

plt.figure(figsize=(10, 10))
for i, body in enumerate(bodies):
    body_positions = np.array([pos[i] for pos in positions])
    plt.plot(body_positions[:, 0], body_positions[:, 1], label=f"Body {i + 1}")

plt.xlabel("X Position (m)")
plt.ylabel("Y Position (m)")
plt.title("Orbital Simulation")
plt.legend()
plt.axis("equal")
plt.grid()
plt.show()