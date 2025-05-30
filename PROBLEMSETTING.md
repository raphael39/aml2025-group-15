# Problem Setting AML 2025 Group 15
## Overview

The aim of this project is to forecast hourly electricity prices in the Netherlands. We chose the Netherlands because it has a liberalised electricity market and is a single bidding zone. In addition, it is a relatively small geographical area and therefore has fewer weather differences. To predict prices, we will use a **State Space Model (SSM)** on multivariate time series data consisting of historical prices, electricity consumption and weather characteristics. Accurate forecasting is critical for market participants to optimise energy production and consumption, reduce costs and improve grid reliability and sustainability.

We will begin our pipeline with a lightweight Deep State‐Space Model (DSSM)—its small neural transition and emission networks let us validate end-to-end data ingestion, incorporate exogenous features (weather, load, time) and produce probabilistic forecasts. Once our DSSM baseline is established, we will swap in a Structured State Space (S4) layer—leveraging its FFT‐accelerated, long‐dependency dynamics—to quantify and capture additional gains in accuracy and uncertainty calibration over extended horizons.

---

## Problem Formulation

We consider a multivariate time series of hourly observations, including:
- Electricity prices  
- Electricity consumption  
- Weather variables  
- Generation mix  

Our objective is to forecast electricity prices over a specified horizon \(H\), producing hourly predictions.



### Formal Setup

Let the dataset be a multivariate time series, defined as:

$\[
D = \{(X_t, y_t)\}_{t=1}^{N}
\]$

Where:

- $\( X_t \in \mathbb{R}^n \)$ is the input feature vector at time $\( t \)$, including:
    - weather indicators (e.g., temperature, humidity, wind speed)
    - electricity load/consumption
    - calendar-based features (hour of day, day of week, holidays)
    - lagged price values
- $\( y_t \in \mathbb{R} \)$ is the target electricity price at time $\( t \)$

The goal is to train a model $\( f )$, specifically a state space model, that predicts:

$\[
\hat{y_t} = f(X_{1:t})
\]$

minimizing the error between $\( y_t \)$ and $\( \hat{y}_t \)$.

To validate our model on real-world historical data, we simulate forecasting a previous day by using only the data available up to that point. For example, to forecast prices on day $d$, we use input features from the past up to time $t=d−1$, and evaluate the model’s predictions $y_{t+1:t+24}$ against the true prices on day $d$.

---

## Model Inputs

Our model will use the following features:

- **Historical Prices**  
  - Lagged values  
  - Rolling statistics  

- **Electricity Consumption**  
  - Smart meter readings  
  - Aggregated load data  

- **Weather Features**  
  - Temperature  
  - Humidity  
  - Wind speed  
  - Radiation  
  - Precipitation  

- **Time Features**  
  - Hour of day  
  - Day of week  
  - Holiday indicators  

---

## Baselines

- **Structured State Space for Sequence Modelling (S4)**
    - https://github.com/state-spaces/s4
    - We will initialize the S4 layer using the HiPPO matrix, to preserve input memory and accurately represent long sequences of data.

- **Mamba**
    - https://github.com/state-spaces/mamba
    - We will use pretrained Mamba models provided in the Github, adapting them to our electricity price forecasting task to evaluate performance and uncertainty calibration.

- **Linear Regression**  
  - Trained on lagged values, weather, and time-based inputs  

---

## Datasets

We will use the following publicly available data sources for the Netherlands:

### Electricity Prices
- [ENTSO-E Transparency Platform](https://transparency.entsoe.eu/)

### Electricity Consumption
- [ENTSO-E Load Data](https://transparency.entsoe.eu/)

### Weather Data
- [Open-Meteo API](https://open-meteo.com/)

Weather data includes:
- Temperature  
- Humidity  
- Wind speed  
- Radiation  
- Precipitation

To align the datasets, we will use the shortest time interval (1 hour) of the 3 datasets. 

### Data Splitting Strategy
To ensure realistic forecasting and avoid data leakage, we apply a strictly chronological split. We go back three years and divide the data as follows:

Training set: first 18 months
Validation set: next 18 months
Test set: strictly future window beyond the 3-year history

At each prediction time t, the model is only provided with features and labels up to t. The test set simulates a real-world deployment scenario by evaluating the trained model on completely unseen future data, ensuring no look-ahead bias.

---

## Evaluation Metrics

We split the 7-day horizon into 28 consecutive 6 h blocks (Block 1 = 0–6 h … Block 28 = 162–168 h), matching the update cadence of meteorological forecasts. Then, for each block, we evaluate:

- **Mean Squared Error (MSE)**
- **Mean Absolute Error (MAE)**
- **Mean Absolute Percentage Error (MAPE)**

To get a better overview of the reliability, we further aggregate these blocks into three horizon tiers:

- **Short-term (0–24 h, Blocks 1–4)**
- **Medium-term (24–72 h, Blocks 5–12)**
- **Long-term (72–168 h, Blocks 13–28)**





---


