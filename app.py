import streamlit as st

st.title("UI Test")
st.write("If you can see this, Streamlit is rendering correctly.")
import streamlit as st
import numpy as np
from scipy.stats import t

# --- Your t-test function (unchanged) ---
def ttest(data, mu0, alpha=0.05, alternative="two-sided"):
    data = np.array(data)
    n = len(data)

    xbar = np.mean(data)
    s = np.std(data, ddof=1)
    se = s / np.sqrt(n)

    t_cal = (xbar - mu0) / se
    df = n - 1

    if alternative == "two-sided":
        t_crit = t.ppf(1 - alpha / 2, df)
        p_value = 2 * (1 - t.cdf(abs(t_cal), df))
        reject = abs(t_cal) > t_crit

    elif alternative == "greater":
        t_crit = t.ppf(1 - alpha, df)
        p_value = 1 - t.cdf(t_cal, df)
        reject = t_cal > t_crit

    elif alternative == "less":
        t_crit = t.ppf(alpha, df)
        p_value = t.cdf(t_cal, df)
        reject = t_cal < t_crit

    return {
        "xbar": xbar,
        "s": s,
        "t_cal": t_cal,
        "df": df,
        "p_value": p_value,
        "decision": "reject" if reject else "accept",
        "t_crit": t_crit,
    }


# --- Streamlit Frontend ---
st.set_page_config(page_title="One-Sample t-Test", layout="centered")
st.title("📊 One-Sample t-Test (Streamlit App)")

st.write("Enter your sample data and hypothesis test parameters.")

# Inputs
data_str = st.text_area(
    "Sample Data (comma-separated)",
    placeholder="e.g. 12.3, 11.8, 12.1, 12.6, 11.9"
)

mu0 = st.number_input("Hypothesized Mean (μ₀)", value=0.0, step=0.1)

alpha = st.selectbox(
    "Significance Level (α)",
    options=[0.10, 0.05, 0.01],
    index=1
)

alternative = st.selectbox(
    "Alternative Hypothesis",
    options=["two-sided", "greater", "less"],
    help="two-sided: μ ≠ μ₀, greater: μ > μ₀, less: μ < μ₀"
)

run_test = st.button("Run t-Test")

# Processing
if run_test:
    try:
        # Parse data
        data = [float(x.strip()) for x in data_str.split(",") if x.strip() != ""]

        if len(data) < 2:
            st.error("Please enter at least two numeric values.")
        else:
            result = ttest(data, mu0, alpha, alternative)

            st.subheader("✅ Results")
            col1, col2 = st.columns(2)

            with col1:
                st.metric("Sample Mean (x̄)", f"{result['xbar']:.4f}")
                st.metric("Sample Std Dev (s)", f"{result['s']:.4f}")
                st.metric("t Statistic", f"{result['t_cal']:.4f}")

            with col2:
                st.metric("Degrees of Freedom", result["df"])
                st.metric("p-value", f"{result['p_value']:.6f}")
                st.metric("Critical t", f"{result['t_crit']:.4f}")

            if result["decision"] == "reject":
                st.error("❌ Decision: Reject H₀ (null hypothesis)")
            else:
                st.success("✅ Decision: Fail to reject H₀ (accept)")

    except ValueError:
        st.error("Invalid input. Please enter only numbers separated by commas.")