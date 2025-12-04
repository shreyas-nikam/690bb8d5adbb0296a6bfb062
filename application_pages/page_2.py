import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


@st.cache_data
def plot_alert_frequency_trend(base_df, attacked_df, attack_type, attack_intensity, font_size):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(base_df['timestamp'], label='Baseline')
    ax.plot(attacked_df['timestamp'], label=f'Attacked ({attack_type})', linestyle='dashed')
    ax.set_title('Alert Frequency Over Time')
    ax.legend()
    return fig


def main():
    st.title('AI Security Vulnerability Simulation Lab - Simulation')
    st.markdown('''\n    Simulate various attack types and intensities.\n    ''')

    # Example synthetic data generation
    sensor_data_baseline = generate_synthetic_safety_data(10, 2, 5, 2.5, 42)
    security_metrics_attacked, attack_events = simulate_vulnerability_impact(
        sensor_data_baseline, 'Data Poisoning', 0.5, 5, {}
    )

    st.subheader('Trend Plot')
    fig_trend = plot_alert_frequency_trend(sensor_data_baseline, security_metrics_attacked, 'Data Poisoning', 0.5, 14)
    st.pyplot(fig_trend)

if __name__ == '__main__':
    main()
