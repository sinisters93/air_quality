import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime, timedelta
from matplotlib.lines import Line2D
from matplotlib.widgets import Button
import warnings
import os
import json
import zipfile
import matplotlib.dates as mdates

warnings.filterwarnings("ignore", category=UserWarning)

# === CONFIGURATION ===
latitude = 12.9716
longitude = 77.5946
start_date = "2025-03-27"
end_date = "2025-03-31"
grid_size = 11
grid_spacing_km = 1.0
plot_interval = 500
moisture_removal_effectiveness = 0.5
vp_desiccant = 10.0
min_delta_vp = 0.2

# === CONSTANTS ===
Lv = 2.45e6
Cp = 1005
rho_air = 1.2
Rd = 287.05
Rv = 461.5

# === GRID SETUP ===
km_per_deg_lat = 110.574
km_per_deg_lon = 111.320 * np.cos(np.radians(latitude))
offset_lat = (grid_size // 2) * (grid_spacing_km / km_per_deg_lat)
offset_lon = (grid_size // 2) * (grid_spacing_km / km_per_deg_lon)
lat_grid = np.linspace(latitude - offset_lat, latitude + offset_lat, grid_size)
lon_grid = np.linspace(longitude - offset_lon, longitude + offset_lon, grid_size)
LAT, LON = np.meshgrid(lat_grid, lon_grid)

# === INPUTS ===
scenario = input("Choose Scenario A (stacked 2000 LPD) or B (unstacked 30000 LPD): ").strip().upper()
required_lpd = int(input("Enter total LPD required: "))
available_area = float(input("Enter available ground area (m²): "))

if scenario == "A":
    unit_capacity_lpd = 2000
    device_length = 6.0 + 4.0
    device_width = 2.4 + 1.5
    per_device_area = device_length * device_width
else:
    unit_capacity_lpd = 30000
    device_length = 12.0 + 4.0
    device_width = 4.0 + 2.0
    per_device_area = device_length * device_width

required_devices = int(np.ceil(required_lpd / unit_capacity_lpd))
max_ground_devices = int(np.floor(available_area / per_device_area))

if max_ground_devices == 0:
    raise ValueError("Insufficient area: Cannot place even 1 device.")

ground_devices = min(required_devices, max_ground_devices)
stacked_layers = int(np.ceil(required_devices / max_ground_devices)) if scenario == "A" else 1
total_devices = required_devices

print("\n=== DEVICE PLACEMENT SUMMARY ===")
print(f"➔ Total LPD required: {required_lpd}")
print(f"➔ Ground area available: {available_area} m²")
print(f"➔ Device footprint: {per_device_area:.1f} m²")
print(f"➔ Max devices possible in area: {max_ground_devices}")
print(f"➔ Required devices for {required_lpd} LPD: {required_devices}")
print(f"➔ Placement: {ground_devices} on ground, stacked in {stacked_layers} layer(s)\n")


# === DEVICE PLACEMENT ===
def manual_multi_level_placement(grid_size, max_per_level, stacked_layers, total_required_devices):
    all_positions = {}
    selected_count = 0
    for level in range(stacked_layers):
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.set_title(f"Manual Device Placement - Level {level}\n(Each level max: {max_per_level}, Total max: {total_required_devices})",
                     fontsize=12, pad=30)
        ax.set_xticks(np.arange(grid_size))
        ax.set_yticks(np.arange(grid_size))
        ax.set_xlim(-0.5, grid_size - 0.5)
        ax.set_ylim(-0.5, grid_size - 0.5)
        ax.set_xticklabels([f"{lon:.2f}" for lon in lon_grid], rotation=45, ha='right')
        ax.set_yticklabels([f"{lat:.4f}" for lat in lat_grid])
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.grid(True)

        placed = np.zeros((grid_size, grid_size), dtype=bool)
        overlay_previous = np.zeros((grid_size, grid_size), dtype=bool)
        placement_text = ax.text(0.5, 1.03,
            f"Level {level} | Selected: 0 / {max_per_level} | Total: {selected_count}/{total_required_devices}",
            transform=ax.transAxes, ha="center", fontsize=10)
        warning_text = ax.text(0.5, 1.01, "", transform=ax.transAxes, ha="center", fontsize=10, color="red")

        for prev_level in range(level):
            for i, j in all_positions[prev_level]:
                overlay_previous[i, j] = True
                ax.plot(j, i, marker='s', color='gray', alpha=0.3, markersize=20)

        def onclick(event):
            nonlocal selected_count
            if event.inaxes != ax:
                return
            j, i = int(np.round(event.xdata)), int(np.round(event.ydata))
            if not (0 <= i < grid_size and 0 <= j < grid_size):
                return
            if not overlay_previous[i, j] and level > 0:
                warning_text.set_text("⚠️ Must stack only above previous level devices.")
                fig.canvas.draw_idle()
                return
            if placed[i, j]:
                placed[i, j] = False
                selected_count -= 1
                ax.plot(j, i, marker='s', color='white', markersize=20)
                warning_text.set_text("")
            else:
                if selected_count >= total_required_devices:
                    warning_text.set_text(f"⚠️ Total limit {total_required_devices} reached.")
                    fig.canvas.draw_idle()
                    return
                if np.sum(placed) >= max_per_level:
                    warning_text.set_text(f"⚠️ Level {level} limit is {max_per_level}.")
                    fig.canvas.draw_idle()
                    return
                placed[i, j] = True
                selected_count += 1
                ax.plot(j, i, marker='s', color=plt.get_cmap('tab10')(level % 10), markersize=20)
                warning_text.set_text("")
            placement_text.set_text(
                f"Level {level} | Selected: {int(np.sum(placed))} / {max_per_level} | Total: {selected_count}/{total_required_devices}")
            fig.canvas.draw_idle()

        def submit(event):
            plt.close()

        ax_submit = plt.axes([0.8, 0.01, 0.1, 0.05])
        btn = Button(ax_submit, 'Confirm')
        btn.on_clicked(submit)
        fig.canvas.mpl_connect('button_press_event', onclick)
        plt.show(block=True)

        selected = [(i, j) for i in range(grid_size) for j in range(grid_size) if placed[i, j]]
        if not selected:
            raise ValueError(f"No devices placed for Level {level}. Please re-run.")
        all_positions[level] = selected
    return all_positions

use_manual = input("Do you want to manually place devices on the grid? (yes/no): ").strip().lower()
center = (grid_size // 2, grid_size // 2)

def generate_spiral_positions(center, num_devices, grid_size):
    directions = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1),
                  (-2, 0), (2, 0), (0, -2), (0, 2),
                  (-2, -1), (-2, 1), (2, -1), (2, 1),
                  (-1, -2), (-1, 2), (1, -2), (1, 2),
                  (-3, 0), (3, 0), (0, -3), (0, 3)]
    cx, cy = center
    positions = []
    for dx, dy in directions:
        i, j = cx + dx, cy + dy
        if 0 <= i < grid_size and 0 <= j < grid_size:
            positions.append((i, j))
        if len(positions) >= num_devices:
            break
    return positions

if use_manual == 'yes':
    print(f"\nMulti-level manual placement enabled. Each level allows up to {ground_devices} devices.")
    device_positions = manual_multi_level_placement(grid_size, ground_devices, stacked_layers, required_devices)
else:
    base_positions = generate_spiral_positions(center, ground_devices, grid_size)
    device_positions = {lvl: base_positions for lvl in range(stacked_layers)}

num_devices = sum(len(p) for p in device_positions.values())

# === WEATHER DATA FETCHING ===
url = (
    f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}"
    f"&start_date={start_date}&end_date={end_date}"
    f"&hourly=temperature_2m,dewpoint_2m,relative_humidity_2m,surface_pressure,wind_speed_10m,wind_direction_10m&timezone=auto"
)
response = requests.get(url)
data = response.json()['hourly']
df = pd.DataFrame(data)

T = np.array(df['temperature_2m'])
RH = np.array(df['relative_humidity_2m'])
WS = np.array(df['wind_speed_10m'])
WD = np.array(df['wind_direction_10m'])
P = np.array(df['surface_pressure']) * 100  # Pa
time_steps = len(T)


# === HELPER FUNCTIONS ===
def saturation_vp(T):
    return 6.112 * np.exp((17.67 * T) / (T + 243.5))

def actual_vp(T, RH):
    return RH * saturation_vp(T) / 100

def calc_AH(T, RH):
    Es = saturation_vp(T)
    return (Es * RH * 2.1674) / ((273.15 + T) * 100)

# === CALCULATE ABSOLUTE HUMIDITY ===
AH_base = calc_AH(T, RH)  # shape: (time_steps,)

# === SPATIAL VARIATION OF AH BASED ON WIND ===
AH_initial_grid = np.zeros((time_steps, grid_size, grid_size))
for t in range(time_steps):
    base_val = AH_base[t]
    angle = np.radians(WD[t])  # wind direction at time t
    for i in range(grid_size):
        for j in range(grid_size):
            dx = j - (grid_size // 2)
            dy = i - (grid_size // 2)
            downwind = dx * np.cos(angle) + dy * np.sin(angle)
            crosswind = -dx * np.sin(angle) + dy * np.cos(angle)
            weight = np.exp(-0.05 * downwind) * np.exp(-0.1 * crosswind ** 2)
            noise = np.random.normal(0, 0.2)
            AH_initial_grid[t, i, j] = base_val * weight + noise

AH_initial_grid = np.clip(AH_initial_grid, 0, None)

# === DISPLAY MEAN AH TIME-SERIES FIRST ===
def animate_mean_ah_time_series(AH_grid, time_list, filename="animated_mean_absolute_humidity"):
    mean_ah = np.nanmean(AH_grid, axis=(1, 2))
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_title("Average Atmospheric Water Content Over Time", fontsize=14)
    ax.set_xlabel("Time")
    ax.set_ylabel("Absolute Humidity (g/m³)")
    ax.set_xlim(pd.to_datetime(time_list[0]), pd.to_datetime(time_list[-1]))
    ax.set_ylim(0, np.max(mean_ah) * 1.1)
    ax.grid(True)

    line, = ax.plot([], [], color='blue', lw=2)
    point, = ax.plot([], [], 'ro')
    timestamp = ax.text(0.5, 1.02, '', transform=ax.transAxes, ha='center', fontsize=12)

    def update(frame):
        time_vals = pd.to_datetime(time_list)
        line.set_data(time_vals[:frame+1], mean_ah[:frame+1])
        point.set_data(time_vals[frame], mean_ah[frame])
        return line, point, timestamp

    ani = animation.FuncAnimation(fig, update, frames=len(time_list), interval=plot_interval, blit=True)
    ani.save(f"{filename}.gif", writer='pillow')
    plt.close()


# Call before device simulation to assess raw water content
animate_mean_ah_time_series(AH_initial_grid, df['time'].tolist(), "initial_absolute_humidity")


# === VECTOR COMPONENTS ===
U = WS * np.cos(np.radians(WD))
V = WS * np.sin(np.radians(WD))
time_steps = len(T)

# === DECAY MAP FOR MULTIPLE DEVICES ===
decay_map = np.zeros((time_steps, grid_size, grid_size))
for t in range(time_steps):
    angle = np.radians((180 + np.degrees(np.arctan2(U[t], V[t]))) % 360)
    for level, positions in device_positions.items():
        for cx, cy in positions:
            for i in range(grid_size):
                for j in range(grid_size):
                    dx, dy = j - cy, i - cx
                    downwind = dx * np.cos(angle) + dy * np.sin(angle)
                    if -0.5 <= downwind <= 5:
                        crosswind = abs(-dx * np.sin(angle) + dy * np.cos(angle))
                        if crosswind <= 5:
                            decay_map[t, i, j] += (1 - downwind / 5) * (1 - crosswind / 5)

decay_map = np.clip(decay_map, 0, 1)

# === CALCULATE VAPOR PRESSURE DEFICIT ===
VP_air = actual_vp(T, RH)
delta_vp = np.maximum(VP_air - vp_desiccant, min_delta_vp)
delta_vp_grid = delta_vp.reshape(-1, 1, 1).repeat(grid_size, axis=1).repeat(grid_size, axis=2)

# === RAW FLUX BASED ON MULTIPLE SOURCES ===
raw_flux = delta_vp_grid * decay_map * moisture_removal_effectiveness  # in g/m²/hr

# === NORMALIZE AND SCALE TO TOTAL DEVICE CAPACITY ===
flux_sum = np.sum(raw_flux, axis=(1, 2), keepdims=True)
flux_sum[flux_sum == 0] = 1
total_capacity_lpd = unit_capacity_lpd * num_devices
flux_mL = (raw_flux / flux_sum) * (total_capacity_lpd * 1000)  # total mL per hour
cell_area_m2 = (grid_spacing_km * 1000) ** 2
flux_mL_per_m2_day = flux_mL / cell_area_m2  # mL/m²/hr --> mL/m²/day

# === GRID BROADCASTS FOR T, P ===
T_grid = T.reshape(-1, 1, 1).repeat(grid_size, axis=1).repeat(grid_size, axis=2)
P_grid = P.reshape(-1, 1, 1).repeat(grid_size, axis=1).repeat(grid_size, axis=2)

# === POST-FLUX ABSOLUTE HUMIDITY ===
AH_after = AH_base.reshape(-1, 1, 1) - raw_flux / 1000 / 24  # g/m³/hr converted to daily average effect

# === RH AFTER ===
def calc_RH_from_AH(T, AH):
    Es = saturation_vp(T)
    return (AH * (273.15 + T) * 100) / (2.1674 * Es)

RH_after_grid = calc_RH_from_AH(T_grid, AH_after)

# === TEMPERATURE CHANGE ===
DT_grid = - (Lv * (raw_flux / 1000 / 24)) / (Cp * rho_air * 5)  # latent cooling
delta_T_exo = 2.0  # °C exothermic heating
T_after = T_grid + DT_grid + delta_T_exo

# === DEW POINT ===
def calc_DewPoint(T, RH):
    return (243.5 * (np.log(RH / 100) + (17.67 * T) / (243.5 + T))) / (17.67 - np.log(RH / 100))

DP_initial = calc_DewPoint(T_grid, calc_RH_from_AH(T_grid, AH_base.reshape(-1, 1, 1)))
DP_after = calc_DewPoint(T_grid, RH_after_grid)
DP_change = DP_initial - DP_after

# === ENTHALPY ===
def calc_Enthalpy(T, AH):
    return Cp * T + Lv * (AH / 1000.0)

Enthalpy_initial = calc_Enthalpy(T_grid, AH_base.reshape(-1, 1, 1))
Enthalpy_after = calc_Enthalpy(T_grid + DT_grid, AH_after)
Enthalpy_change = (Enthalpy_initial - Enthalpy_after) / 1000  # in kJ/kg

# === AIR DENSITY ===
def calc_AirDensity(P, T, AH):
    e = AH * (T + 273.15) / 2.1674
    Pd = P - e
    return (Pd / (Rd * (T + 273.15))) + (e / (Rv * (T + 273.15)))

Density_initial = calc_AirDensity(P_grid, T_grid, AH_base.reshape(-1, 1, 1))
Density_after = calc_AirDensity(P_grid, T_grid + DT_grid, AH_after)
Density_change = Density_after - Density_initial

# === MIXING RATIO ===
def calc_MixingRatio(AH, T):
    return (AH / 1000.0) / (1.204 - (AH / 1000.0))

MR_initial = calc_MixingRatio(AH_base.reshape(-1, 1, 1), T_grid)
MR_after = calc_MixingRatio(AH_after, T_grid)
MR_change = MR_initial - MR_after

# === SATURATION DEFICIT ===
def calc_SaturationDeficit(T, RH):
    Es = saturation_vp(T)
    E = Es * RH / 100
    return Es - E

SD_initial = calc_SaturationDeficit(T_grid, calc_RH_from_AH(T_grid, AH_base.reshape(-1, 1, 1)))
SD_after = calc_SaturationDeficit(T_grid, RH_after_grid)
SD_change = SD_after - SD_initial

# === PRESSURE DROP AND AIRFLOW RATE ===
Pressure_drop_grid = decay_map * 30  # max 30 Pa
Airflow_rate_grid = decay_map * 2000  # max 2000 m³/h per cell


def animate_combined(data, title, units, filename):
    cmap = plt.get_cmap('tab10')
    z_levels = np.arange(0, 210, 10)
    decay_scale = 75.0
    time_vals = pd.to_datetime(df['time']).tolist()

    center_x, center_y = grid_size // 2, grid_size // 2
    center_vals = data[:, center_y, center_x]
    vertical_profiles = np.array([v * np.exp(-z_levels / decay_scale) for v in center_vals])
    vertical_profiles = vertical_profiles.T

    mean_vals = np.array([
        np.nanmean(np.where((data[t] != 0) & (~np.isnan(data[t])), data[t], np.nan))
        for t in range(data.shape[0])
    ])
    mean_vals = pd.Series(mean_vals).fillna(method='ffill').fillna(0).values

    fig = plt.figure(figsize=(18, 10), dpi=150)
    gs = fig.add_gridspec(4, 2, height_ratios=[3, 0.2, 1.2, 0.1], hspace=0.4)

    ax_map = fig.add_subplot(gs[0, 0])
    ax_vp = fig.add_subplot(gs[0, 1])
    ax_spacer = fig.add_subplot(gs[1, :]); ax_spacer.axis("off")
    ax_ts = fig.add_subplot(gs[2, :])
    ax_time = fig.add_subplot(gs[3, :]); ax_time.axis("off")
    timestamp = ax_time.text(0.5, 0.5, '', ha='center', va='center', fontsize=14)

    vmin, vmax = np.nanmin(data), np.nanmax(data)
    if vmin == vmax: vmax = vmin + 1e-5
    levels = np.linspace(vmin, vmax, 50)
    cont = ax_map.contourf(LON, LAT, data[0], levels=levels, cmap='plasma', vmin=vmin, vmax=vmax)

    for lon in lon_grid:
        ax_map.axvline(x=lon, color='gray', linewidth=0.5, linestyle='--', alpha=0.6)
    for lat in lat_grid:
        ax_map.axhline(y=lat, color='gray', linewidth=0.5, linestyle='--', alpha=0.6)

    fig.colorbar(cont, ax=ax_map, label=units)
    ax_map.set_title(f"{title} (Spatial Map)")
    ax_map.set_xlabel("Longitude")
    ax_map.set_ylabel("Latitude")

    # Device markers
    legend_handles = []
    for level, positions in device_positions.items():
        color = cmap(level % 10)
        for cx, cy in positions:
            offset = level * 0.0003
            ax_map.plot(lon_grid[cy], lat_grid[cx] + offset, marker='o', color=color, markersize=6, linestyle='None')
        handle = Line2D([0], [0], marker='o', color=color, linestyle='None', markersize=6, label=f'{level}')
        legend_handles.append(handle)

    img_vp = ax_vp.imshow(np.zeros_like(vertical_profiles),
                          extent=[mdates.date2num(time_vals[0]), mdates.date2num(time_vals[-1]), 0, z_levels[-1]],
                          aspect='auto', origin='lower', cmap='plasma', vmin=vmin, vmax=vmax)
    fig.colorbar(img_vp, ax=ax_vp, label=units)
    ax_vp.set_title("Vertical Profile (Heatmap)")
    ax_vp.set_ylabel("Height (m)")
    ax_vp.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H'))

    for label in ax_vp.get_xticklabels():
        label.set_rotation(30)
        label.set_horizontalalignment('right')

    line_ts, = ax_ts.plot([], [], 'b-', lw=2)
    point_ts, = ax_ts.plot([], [], 'ro')
    ax_ts.set_xlim(min(time_vals), max(time_vals))
    min_val = np.nanmin(mean_vals)
    max_val = np.nanmax(mean_vals)
    buffer = (max_val - min_val) * 0.1 if max_val != min_val else 0.01
    ax_ts.set_ylim(min_val - buffer, max_val + buffer)
    ax_ts.set_title("Variation with Time", pad=15)
    ax_ts.set_xlabel("Time")
    ax_ts.set_ylabel(f"Avg {units}")
    ax_ts.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H'))
    ax_ts.tick_params(axis='x', which='major', pad=10)

    def update(frame):
        ax_map.clear()
        cont = ax_map.contourf(LON, LAT, data[frame], levels=levels, cmap='plasma', vmin=vmin, vmax=vmax)
        for lon in lon_grid:
            ax_map.axvline(x=lon, color='gray', linewidth=0.5, linestyle='--', alpha=0.6)
        for lat in lat_grid:
            ax_map.axhline(y=lat, color='gray', linewidth=0.5, linestyle='--', alpha=0.6)
        ax_map.set_title(f"{title} (Spatial Map)")
        ax_map.set_xlabel("Longitude")
        ax_map.set_ylabel("Latitude")

        for level, positions in device_positions.items():
            color = cmap(level % 10)
            for cx, cy in positions:
                offset = level * 0.0003
                ax_map.plot(lon_grid[cy], lat_grid[cx] + offset, marker='o', color=color, markersize=6, linestyle='None')
        ax_map.legend(handles=legend_handles, loc='upper right')

        heatmap_frame = np.full_like(vertical_profiles, np.nan)
        heatmap_frame[:, :frame + 1] = vertical_profiles[:, :frame + 1]
        img_vp.set_data(heatmap_frame)

        line_ts.set_data(time_vals[:frame + 1], mean_vals[:frame + 1])
        point_ts.set_data(time_vals[frame], mean_vals[frame])
        return cont.collections + [img_vp, timestamp, line_ts, point_ts]

    ani = animation.FuncAnimation(fig, update, frames=data.shape[0], interval=plot_interval, blit=False)
    ani.save(f"{filename}_combined.gif", writer='pillow')
    plt.close()

# === ANIMATE ALL PARAMETERS ===
animate_combined(flux_mL_per_m2_day, "Water Vapor Flux", "mL/m²/day", "uravu_water_vapor_flux")
animate_combined(DT_grid, "Temperature Change due to Latent Cooling", "°C", "uravu_temperature_change")
animate_combined(raw_flux, "Absolute Humidity Reduction", "g/m³/hr", "uravu_absolute_humidity")
animate_combined(RH_after_grid, "Relative Humidity", "%", "uravu_relative_humidity")
animate_combined(DP_change, "Dew Point Reduction", "°C", "uravu_dew_point")
animate_combined(Density_change, "Air Density Change", "kg/m³", "uravu_air_density")
animate_combined(MR_change, "Mixing Ratio Change", "kg/kg", "uravu_mixing_ratio")
animate_combined(SD_change, "Saturation Deficit Change", "hPa", "uravu_saturation_deficit")
animate_combined(Enthalpy_change, "Enthalpy Change", "kJ/kg", "uravu_enthalpy_of_air")
animate_combined(Pressure_drop_grid, "Pressure Drop", "Pa", "uravu_pressure_drop")
animate_combined(Airflow_rate_grid, "Airflow Rate", "m³/h", "uravu_airflow_rate")

def export_to_disk(data_dict, output_dir="exported_earth2_ready"):
    os.makedirs(output_dir, exist_ok=True)
    meta = {
        "lat": lat_grid.tolist(),
        "lon": lon_grid.tolist(),
        "times": df['time'][:len(data_dict[next(iter(data_dict))])].tolist(),
        "device_positions": {
            str(level): [(int(i), int(j)) for i, j in positions]
            for level, positions in device_positions.items()
        }
    }
    with open(os.path.join(output_dir, "metadata.json"), "w") as f:
        json.dump(meta, f, indent=2)

    for name, arr in data_dict.items():
        np.save(os.path.join(output_dir, f"{name}.npy"), arr)
        flat_df = pd.DataFrame(arr.reshape((arr.shape[0], -1)))
        flat_df.to_csv(os.path.join(output_dir, f"{name}.csv"), index=False)

def zip_results(folder_path):
    zip_path = f"{folder_path}.zip"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, folder_path)
                zipf.write(full_path, arcname)
    return zip_path

# === EXPORT ALL OUTPUTS TO DISK ===
export_to_disk({
    "Water_Vapor_Flux": flux_mL_per_m2_day,
    "Temperature_Change": DT_grid,
    "Absolute_Humidity_Reduction": raw_flux,
    "Relative_Humidity": RH_after_grid,
    "Dew_Point_Change": DP_change,
    "Air_Density_Change": Density_change,
    "Mixing_Ratio_Change": MR_change,
    "Saturation_Deficit_Change": SD_change,
    "Enthalpy_Change": Enthalpy_change,
    "Pressure_Drop": Pressure_drop_grid,
    "Airflow_Rate": Airflow_rate_grid
})

# === ZIP PACKAGE FOR PLATFORM DELIVERY ===
zip_results("exported_earth2_ready")

print("✅ Simulation complete. All outputs exported and packaged in 'exported_earth2_ready.zip'.")
