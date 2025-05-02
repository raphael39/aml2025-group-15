# Problemsetting AML 2025 Group XX
## Overview

The goal of this project is to forecast electricity prices using a **state space model (SSM)** on multivariate time series data consisting of historical prices, electricity consumption, and weather features. Accurate forecasting is critical for market participants to optimize energy production and consumption, reduce costs, and improve grid reliability.

Recent advances in machine learning have shown that state space models can effectively model temporal dependencies in sequential data while accounting for uncertainty and latent dynamics. Our aim is to develop a probabilistic or neural SSM that captures the underlying structure of electricity price movements driven by both internal dynamics (e.g., autoregressive behavior) and external variables (e.g., temperature, consumption).

We will evaluate our model on real-world electricity and weather datasets and compare it to strong baselines including a persistence model and linear regression.

---

## Problem Formulation

Given a multivariate time series:

- Electricity prices  
- Electricity consumption  
- Weather data  

our objective is to predict electricity prices for a defined **forecast horizon H**.

### Formal Setup

Let the dataset be defined as:

\[
D = \{(X_t, y_t)\}_{t=1}^{N}
\]

Where:

- \( X_t \in \mathbb{R}^n \) is the input feature vector at time \( t \), including:
  - lagged price values
  - consumption metrics
  - weather variables
  - time-based features
- \( y_t \in \mathbb{R} \) is the target electricity price at time \( t \)

The goal is to train a model \( f_\theta \), specifically a state space model, that predicts:

\[
\hat{y}_t = f_\theta(X_{1:t})
\]

minimizing the error between \( y_t \) and \( \hat{y}_t \).

---

## Model Description

We will implement a **State Space Model (SSM)** for time series forecasting. Our approach may include:

- Classical linear Gaussian SSM (e.g., Kalman Filter)
- Neural SSMs such as:
  - Deep State Space Models (DSSM)
  - Structured State Space Models (S4)
  - DeepAR with probabilistic forecasting
- Latent variable modeling to capture hidden market dynamics

The model will be trained to minimize forecasting error using regression-based loss (e.g., MSE) or probabilistic loss (e.g., negative log-likelihood).

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

We will benchmark our model against:

- **Persistence Model**  
  - Predicts the next value as the last observed price  

- **Linear Regression**  
  - Trained on lagged values, weather, and time-based inputs  

---

## Datasets

We will use publicly available data sources:

### Electricity Prices
- [ENTSO-E Transparency Platform](https://transparency.entsoe.eu/)
- [Swissgrid](https://www.swissgrid.ch/)

### Electricity Consumption
- [UCI Smart Meter Dataset](https://archive.ics.uci.edu/ml/datasets/individual+household+electric+power+consumption)
- [ENTSO-E Load Data](https://transparency.entsoe.eu/)

### Weather Data
- [Open-Meteo API](https://open-meteo.com/)
- [Visual Crossing Weather API](https://www.visualcrossing.com/weather-data)

Weather data includes:
- Temperature  
- Humidity  
- Wind speed  
- Radiation  
- Precipitation  

---

## Optional Extensions (if time permits)

- Incorporate uncertainty estimation (e.g., prediction intervals)
- Evaluate model performance in different countries or seasonal periods
- Visualize latent dynamics learned by the state space model

---

## Evaluation Metrics

- Mean Squared Error (MSE)  
- Mean Absolute Error (MAE)  
- Mean Absolute Percentage Error (MAPE)  
- Calibration of probabilistic forecasts (if applicable)

---
