
# ML model to predict flight duration

## Project Overview

This project involves processing flight data and developing a machine learning model to predict flight duration. The dataset consists of two main files:
- **positions.csv**: Contains aircraft position data with time, latitude, longitude, altitude, ground speed, aircraft ID, and model.
- **airports.csv**: Contains airport details, including codes, names, locations, and altitude.

The project has three primary tasks:
1. **Listing Flights**: Extract flight departure and arrival information, ordered by departure time.
2. **Longest Sequence of Flights**: Determine the maximum number of flights for each aircraft within a 2-day sliding window.
3. **Flight Duration Prediction Model**: Train a machine learning model to predict flight duration.

---

## Setup Instructions

### Prerequisites
- Python 3.x
- Pandas
- Scikit-learn

### Installation

Clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/deeptera/flight-data-processing.git
cd flight-data-processing
pip install -r requirements.txt
```

---

## Data Files

- **positions.csv**: 395,183 instances of aircraft positions over time.
- **airports.csv**: 4,005 instances of airport details.

The structure of each file is as follows:

**positions.csv**
| Time            | Latitude       | Longitude      | Altitude | GroundSpeed | IdAircraft | ModelAircraft |
|-----------------|----------------|----------------|----------|-------------|------------|---------------|
| datetime (UTC)  | decimal (18,12) | decimal (18,12) | km       | km/h        | int        | char (50)     |

**airports.csv**
| Name        | Code | Latitude       | Longitude      | Altitude | Country     | City     |
|-------------|------|----------------|----------------|----------|-------------|----------|
| char (50)   | char (5) | decimal (18,12) | decimal (18,12) | km       | char (50)   | char (50)|

---

## Tasks Breakdown

### 1. Flight Listing
The script processes the `positions.csv` and `airports.csv` files, generating a list of flights. Each flight is defined by its first and last recorded positions in time, indicating departure and arrival respectively.

**Output:**
- Departure Date and Time
- Departure Airport (Code, Name, City)
- Arrival Date and Time
- Arrival Airport (Code, Name, City)
- Aircraft ID and Model

The flights are ordered by departure time.

### 2. Longest Sequence of Flights
For each aircraft, we calculate the maximum number of flights that occur within any two consecutive days. The data is processed using a sliding window approach, which ensures that the maximum sequence is identified efficiently.

**Output:**
- 2-day period
- Aircraft ID and Model
- Number of flights in the period

### 3. Flight Duration Prediction Model
The model is designed to predict the flight duration in minutes based on the following input features:
- Departure Airport Code
- Arrival Airport Code
- Day of the Week (1-7)
- Departure Hour (0-23)
- Aircraft Model (A319 or A320)

**Steps:**
- Data preprocessing to format the input features.
- Training a model (e.g., Random Forest or Gradient Boosting) using Scikit-learn.
- Evaluating model accuracy using cross-validation.

---

## Key Challenges & Solutions

### Flight Segmentation
A critical challenge was determining the time threshold that separates flights. To address this:
1. **Option 1**: Calculate a dynamic threshold based on airport distances—high computational complexity.
2. **Option 2**: Use a fixed time threshold and iteratively refine it to minimize errors. This approach was more feasible and was chosen for implementation.

### Memory Management
Segmenting flights based on aircraft IDs allowed the data to be processed in memory, preventing memory overload. The records were pre-sorted by time to simplify processing.

### Outliers & Noise
Flights with implausibly short durations, such as those involving remote locations, were flagged as outliers and excluded from further analysis.

---

## Running the Scripts

1. **Flight Listing**: Run the following command to generate the list of flights:
    ```bash
    python flight_listing.py
    ```

2. **Longest Flight Sequence**: Run the sliding window script to find the longest sequence of flights within 2 days:
    ```bash
    python flight_sequence.py
    ```

3. **Flight Duration Prediction**: Train and evaluate the machine learning model:
    ```bash
    python flight_duration_model.py
    ```

---

## Improvements & Future Work

- **Feature Engineering**: Incorporating additional features such as weather data or historical delays could improve model accuracy.
- **Threshold Optimization**: A more sophisticated method for determining flight segmentation thresholds could further reduce noise and errors.
- **Model Tuning**: Hyperparameter optimization and testing more advanced algorithms (e.g., XGBoost) could yield better prediction results.

---

## Conclusion

This project successfully implemented flight data processing and an initial machine learning model for flight duration prediction. The results provide a foundation for further exploration and refinement.
