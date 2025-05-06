# Problemsetting AML 2025 Group 15
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

Let the dataset be defined as:

$\[
D = \{(X_t, y_t)\}_{t=1}^{N}
\]$

Where:

- $\( X_t \in \mathbb{R}^n \)$ is the input feature vector at time $\( t \)$, including:
  - lagged price values
  - consumption metrics
  - weather variables
  - time-based features
- $\( y_t \in \mathbb{R} \)$ is the target electricity price at time $\( t \)$

The goal is to train a model $\( f_\theta \)$, specifically a state space model, that predicts:

$\[
\hat{y_t} = f_\theta(X_{1:t})
\]$

minimizing the error between $\( y_t \)$ and $\( \hat{y}_t \)$.

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

## Evaluation Metrics

- Mean Squared Error (MSE)  
- Mean Absolute Error (MAE)  
- Mean Absolute Percentage Error (MAPE)  
- Calibration of probabilistic forecasts (if applicable)

---


