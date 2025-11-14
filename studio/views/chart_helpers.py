"""
Chart Helper Functions - HidroStudio Professional
Funciones auxiliares para generar datos de gráficos (hietogramas e hidrogramas)
"""

import json


def calculate_optimal_timestep(storm, custom_timestep=None):
    """
    Calculate optimal timestep for hyetograph discretization

    Based on:
    - HEC-HMS: Δt ≤ Tc/5
    - NRCS: Δt = 0.2 × Tc
    - Duration-based rules for large storms

    Args:
        storm: DesignStorm instance
        custom_timestep: Optional user-defined timestep in minutes

    Returns:
        float: Optimal timestep in minutes
    """
    if custom_timestep:
        return float(custom_timestep)

    watershed = storm.watershed
    duration_hours = float(storm.duration_hours)

    # If watershed has Tc, use it to calculate timestep
    if watershed and watershed.tc_minutes:
        tc_minutes = float(watershed.tc_minutes)

        # Rule: Δt ≤ Tc/5 (HEC-HMS)
        timestep_from_tc = tc_minutes / 5

        # Cap at reasonable limits
        if timestep_from_tc < 1:
            timestep = 1  # Minimum 1 minute
        elif timestep_from_tc > 30:
            timestep = 30  # Maximum 30 minutes
        else:
            # Round to nearest 5 minutes for practical purposes
            timestep = round(timestep_from_tc / 5) * 5
            if timestep == 0:
                timestep = 5
    else:
        # Fallback: Duration-based rules (when Tc not available)
        if duration_hours <= 1:
            timestep = 5  # 5 min for short storms
        elif duration_hours <= 6:
            timestep = 10  # 10 min for medium storms
        elif duration_hours <= 24:
            timestep = 15  # 15 min for daily storms
        else:
            timestep = 30  # 30 min for multi-day storms

    return timestep


def generate_hyetograph_data(storm, custom_timestep=None):
    """
    Generate hyetograph data (rainfall distribution over time)
    Uses Alternating Block Method

    Timestep priority:
    1. custom_timestep parameter (if provided)
    2. storm.time_step_minutes (if not default)
    3. Auto-calculated from Tc (Δt ≤ Tc/5 per HEC-HMS)
    4. Auto-calculated from duration (fallback)

    Args:
        storm: DesignStorm instance
        custom_timestep: Optional override timestep in minutes

    Returns:
        dict: {
            'time_steps': [...],
            'intensity': [...],
            'timestep': float,
            'method': str
        }
    """
    duration_hours = float(storm.duration_hours)
    total_rainfall = float(storm.total_rainfall_mm)

    # Determine timestep with priority
    if custom_timestep:
        interval = float(custom_timestep)
        method = f"Custom override ({interval} min)"
    elif storm.time_step_minutes and storm.time_step_minutes != 5:
        # User explicitly set a timestep (not default)
        interval = float(storm.time_step_minutes)
        method = f"User-defined ({interval} min)"
    else:
        # Auto-calculate optimal timestep
        interval = calculate_optimal_timestep(storm, None)
        if storm.watershed and storm.watershed.tc_minutes:
            method = f"Auto Tc-based ({interval} min, Tc={storm.watershed.tc_minutes:.0f} min)"
        else:
            method = f"Auto duration-based ({interval} min)"

    num_intervals = int((duration_hours * 60) / interval)
    time_steps = []
    intensity = []

    # Alternating Block: peak in the middle
    peak_index = num_intervals // 2

    for i in range(num_intervals):
        time_steps.append(round(i * interval, 1))

        # Distance from peak
        dist_from_peak = abs(i - peak_index)
        # Intensity decreases with distance from peak
        relative_intensity = 1 - (dist_from_peak / num_intervals)
        # Calculate intensity (convert mm to mm/h)
        intensity_value = (total_rainfall / duration_hours) * (1 + relative_intensity)

        intensity.append(round(intensity_value, 2))

    return {
        'time_steps': time_steps,
        'intensity': intensity,
        'timestep': interval,
        'method': method
    }


def generate_hydrograph_data(hydrograph):
    """
    Generate hydrograph data from stored hydrograph_data JSON
    or create sample triangular hydrograph

    Args:
        hydrograph: Hydrograph instance

    Returns:
        dict: {'time_steps': [...], 'discharge': [...], 'name': '...'}
    """
    # If hydrograph_data exists, use it
    if hydrograph.hydrograph_data:
        data = json.loads(hydrograph.hydrograph_data) if isinstance(hydrograph.hydrograph_data, str) else hydrograph.hydrograph_data
        return {
            'name': hydrograph.get_method_display(),
            'time_steps': data.get('time_steps', []),
            'discharge': data.get('discharge', [])
        }

    # Otherwise, generate sample triangular hydrograph
    peak_discharge = float(hydrograph.peak_discharge_m3s)
    time_to_peak = float(hydrograph.time_to_peak_minutes)
    base_time = time_to_peak * 3  # Approximate base time
    interval = 5  # 5 minutes

    time_steps = []
    discharge = []

    t = 0
    while t <= base_time:
        time_steps.append(t)

        if t <= time_to_peak:
            # Rising limb
            q = (peak_discharge / time_to_peak) * t
        else:
            # Falling limb
            time_from_peak = t - time_to_peak
            falling_time = base_time - time_to_peak
            q = peak_discharge * (1 - (time_from_peak / falling_time))

        discharge.append(round(max(0, q), 2))
        t += interval

    return {
        'name': hydrograph.get_method_display(),
        'time_steps': time_steps,
        'discharge': discharge
    }
