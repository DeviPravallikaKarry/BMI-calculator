import streamlit as st

# Configure page early
st.set_page_config(page_title="BMI Calculator", page_icon="✅", layout="centered")


# --- Pure functions (no UI state) ---
def compute_bmi_metric(weight_kg: float, height_cm: float) -> float:
    """BMI = kg / m^2 for metric inputs."""
    m = height_cm / 100.0
    return weight_kg / (m ** 2)


def compute_bmi_imperial(weight_lb: float, height_in: float) -> float:
    """BMI = (lb / in^2) * 703 for imperial inputs."""
    return (weight_lb * 703) / (height_in ** 2)


def classify_bmi(bmi_val: float) -> str:
    """Adult BMI categories per CDC."""
    if bmi_val < 18.5:
        return "Underweight"
    elif bmi_val < 25:
        return "Healthy weight"
    elif bmi_val < 30:
        return "Overweight"
    elif bmi_val < 35:
        return "Obesity (Class I)"
    elif bmi_val < 40:
        return "Obesity (Class II)"
    else:
        return "Obesity (Class III)"


# --- App UI wrapped to avoid module-level globals ---
def main():
    st.title("BMI Calculator")
    st.caption("Adult screening only; BMI is not a diagnostic measure.")

    units = st.radio("Choose units", ["Metric (kg, cm)", "Imperial (lb, in)"])

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Name", value="")

    if units.startswith("Metric"):
        with col1:
            weight_kg = st.number_input("Weight (kg)", min_value=0.0, step=0.1, value=70.0)
        with col2:
            height_cm = st.number_input("Height (cm)", min_value=0.0, step=0.1, value=170.0)
    else:
        with col1:
            weight_lb = st.number_input("Weight (lb)", min_value=0.0, step=0.1, value=154.0)
        with col2:
            height_in = st.number_input("Height (in)", min_value=0.0, step=0.1, value=67.0)

    if st.button("Calculate BMI"):
        if units.startswith("Metric"):
            if weight_kg <= 0 or height_cm <= 0:
                st.error("Please enter positive values.")
            else:
                bmi_value = compute_bmi_metric(weight_kg, height_cm)
                category = classify_bmi(bmi_value)
                st.success(f"{name or 'Person'}: BMI = {bmi_value:.1f} → {category}")
        else:
            if weight_lb <= 0 or height_in <= 0:
                st.error("Please enter positive values.")
            else:
                bmi_value = compute_bmi_imperial(weight_lb, height_in)
                category = classify_bmi(bmi_value)
                st.success(f"{name or 'Person'}: BMI = {bmi_value:.1f} → {category}")


if __name__ == "__main__":
    main()
