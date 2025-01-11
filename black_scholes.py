# File path: app.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma, option_type='call'):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    if option_type == 'call':
        return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

# Sidebar
linkedin_link='https://www.linkedin.com/in/manasi-mundada-89a904205/'
github_link='https://github.com/manasimundada'
with st.sidebar:
    st.header("My Links!")
    st.markdown("""
        <style>
            .sidebar-link {
                display: flex;
                align-items: center;
                text-decoration: none;
                background-color: #f0f0f0;
                padding: 10px;
                border-radius: 5px;
                margin: 10px 0;
            }
            .sidebar-link img {
                margin-right: 10px;
            }
            .sidebar-link span {
                font-family: monospace;
                color: black;
                font-size: 1rem;
            }
            .sidebar-link:hover {
                background-color: #e0e0e0;
            }
        </style>
        <a class="sidebar-link" href="https://github.com/manasimundada" target="_blank">
            <img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="30"/>
            <span>GitHub</span>
        </a>
        <a class="sidebar-link" href="https://www.linkedin.com/in/manasi-mundada-89a904205/" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" width="30"/>
            <span>LinkedIn</span>
        </a>
    """, unsafe_allow_html=True)


# Title and Description
st.title("Black-Scholes Option Pricing Model")
st.write("""
This app calculates the price of European call and put options using the Black-Scholes model.
Enter the parameters below to get the option prices and see how the prices change with varying spot price and volatility.
""")

# LaTeX formula for Black-Scholes model
st.write("### Black-Scholes Formula")
st.latex(r"""
    C = S_t \cdot N(d_1) - K \cdot e^{-rT} \cdot N(d_2)
""")
st.latex(r"""
    P = K \cdot e^{-rT} \cdot N(-d_2) - S_t \cdot N(-d_1)
""")
st.latex(r"""
    d_1 = \frac{\ln(S_t / K) + (r + \frac{\sigma^2}{2})T}{\sigma \sqrt{T}}
""")
st.latex(r"""
    d_2 = d_1 - \sigma \sqrt{T}
""")

# Definitions for each parameter
st.write("### Parameter Definitions")
st.latex(r"""
    \begin{align*}
    C &= \text{call option price} \\
    N &= \text{CDF of the normal distribution} \\
    S_t &= \text{spot price of an asset} \\
    K &= \text{strike price} \\
    r &= \text{risk-free interest rate} \\
    t &= \text{time to maturity} \\
    \sigma &= \text{volatility of the asset}
    \end{align*}
""")



# User inputs
S = st.number_input("Current Asset Price (S)", value=100.0)
K = st.number_input("Strike Price (K)", value=100.0)
T = st.number_input("Time to Maturity (T) in years", value=1.0)
sigma = st.number_input("Volatility (sigma) as a decimal", value=0.2)
r = st.number_input("Risk-Free Interest Rate (r) as a decimal", value=0.05)

# Calculate option prices
call_price = black_scholes(S, K, T, r, sigma, 'call')
put_price = black_scholes(S, K, T, r, sigma, 'put')

# Display prices
st.markdown(f"""
<div style='display: flex; justify-content: center;'>
    <div style='background-color:#28a745; padding: 10px; border-radius: 10px; margin: 10px;'>
        <h3 style='color:#fff;'>CALL Option Price: {call_price:.2f}</h3>
    </div>
    <div style='background-color:#dc3545; padding: 10px; border-radius: 10px; margin: 10px;'>
        <h3 style='color:#fff;'>PUT Option Price: {put_price:.2f}</h3>
    </div>
</div>
""", unsafe_allow_html=True)

# Heatmap inputs
st.write("### Interactive Options Pricing Heatmap")
min_spot = st.number_input("Min Spot Price", value=50.0)
max_spot = st.number_input("Max Spot Price", value=150.0)
min_volatility = st.slider("Min Volatility", min_value=0.0, max_value=1.0, value=0.1)
max_volatility = st.slider("Max Volatility", min_value=min_volatility, max_value=1.0, value=0.5)

# Generate heatmaps
spots = np.linspace(min_spot, max_spot, 10)
volatilities = np.linspace(min_volatility, max_volatility, 10)
call_prices = np.zeros((len(volatilities), len(spots)))
put_prices = np.zeros((len(volatilities), len(spots)))

for i, sigma in enumerate(volatilities):
    for j, S in enumerate(spots):
        call_prices[i, j] = black_scholes(S, K, T, r, sigma, 'call')
        put_prices[i, j] = black_scholes(S, K, T, r, sigma, 'put')

# Plot heatmaps
fig, ax = plt.subplots(1, 2, figsize=(20, 8))

sns.heatmap(call_prices, xticklabels=np.round(spots, 2), yticklabels=np.round(volatilities, 2), ax=ax[0], cmap='cividis', annot=True, fmt=".2f")
ax[0].set_title('CALL Option Prices',fontsize=24)
ax[0].set_xlabel('Spot Price',fontsize=20)
ax[0].set_ylabel('Volatility',fontsize=20)

sns.heatmap(put_prices, xticklabels=np.round(spots, 2), yticklabels=np.round(volatilities, 2), ax=ax[1], cmap='magma', annot=True, fmt=".2f")
ax[1].set_title('PUT Option Prices',fontsize=24)
ax[1].set_xlabel('Spot Price',fontsize=20)
ax[1].set_ylabel('Volatility',fontsize=20)

st.pyplot(fig)

# Secret section at the bottom
# with st.expander("What is the Black-Scholes Model?"):
#     st.write("""
#     The Black-Scholes model is a mathematical model for pricing an options contract. The model 
#     assumes that the price of the underlying asset follows a geometric Brownian motion with constant 
#     volatility and that the market is frictionless, meaning there are no transaction costs or taxes.
#     I started this project while learning about options trading and pricing models to better understand
#     how call and put option prices can change when you vary certain parameters. This project idea was
#     heavily inspired from a video on CodingJesus' channel about quant projects.""")
