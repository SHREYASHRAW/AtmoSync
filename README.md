# AtmoSync — Micro-Climate Arbitrage Analytics

**An end-to-end data analytics project for agricultural shipment monitoring, spoilage estimation, financial impact analysis, and rerouting recommendations.**

AtmoSync simulates IoT telemetry from agricultural shipping containers and transforms environmental readings into actionable business insights. It combines Python, Apache Kafka, Snowflake, dbt, SQL, and Power BI to demonstrate a modern analytics pipeline.

> **Project status:** Core data pipeline and analytical models implemented; executive Power BI dashboard and project review presentation completed. Telemetry and financial estimates are simulation-based, not production predictions.

---

## Table of Contents

- [Business Problem](#business-problem)
- [Project Objectives](#project-objectives)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Data Pipeline](#data-pipeline)
- [Key Analytics](#key-analytics)
- [Dashboard and Deliverables](#dashboard-and-deliverables)
- [Repository Structure](#repository-structure)
- [Key Results](#key-results)
- [Data Quality and Validation](#data-quality-and-validation)
- [Getting Started](#getting-started)
- [Limitations and Future Improvements](#limitations-and-future-improvements)
- [Author](#author)

## Business Problem

Agricultural shipments can be exposed to unsuitable temperature, humidity, and vibration conditions during transportation. These conditions may affect product quality, increase spoilage risk, and reduce shipment value.

AtmoSync demonstrates how simulated environmental telemetry and analytical models can help answer questions such as:

- Which containers are experiencing critical climate conditions?
- How much produce may be affected under the current simulation assumptions?
- What is the estimated financial impact of spoilage?
- Could an alternative destination produce a better estimated net value after route costs?

## Project Objectives

- Simulate environmental telemetry for agricultural shipping containers.
- Stream telemetry events through Apache Kafka.
- Store raw telemetry in Snowflake.
- Transform data into analytical models using dbt and SQL.
- Classify climate risk and estimate exposure and spoilage.
- Calculate spoilage-related financial impact.
- Compare alternative destinations using simulated market prices and route costs.
- Present operational and financial insights through Power BI.

## System Architecture

```text
Python IoT Simulator
        |
        v
Apache Kafka
        |
        v
Snowflake RAW Layer
        |
        v
dbt Transformations and Tests
        |
        v
Analytical Models
        |
        +--> Climate Risk and Exposure
        +--> Spoilage Estimation
        +--> Financial Impact
        +--> Arbitrage and Rerouting
        |
        v
Power BI Executive Dashboard
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Telemetry simulation and event generation |
| Apache Kafka | Streaming telemetry events |
| Snowflake | Cloud data warehouse and raw data storage |
| SQL | Data transformation and analytical calculations |
| dbt Core | Model dependencies, transformations, and data-quality tests |
| Power BI | Executive dashboard and visual analytics |
| Git and GitHub | Version control and project documentation |

## Data Pipeline

### 1. Telemetry simulation

A Python simulator generates environmental readings for three example containers carrying avocados, bananas, and mangoes. Events include timestamps, container details, temperature, humidity, and vibration.

The simulator includes normal, warning, and critical scenarios based on configured commodity profiles.

### 2. Event streaming

A Kafka producer publishes JSON telemetry events to the `atmosync-telemetry` topic. A consumer supports reading and validating the event stream.

### 3. Data warehousing

Kafka Connect delivers telemetry to the `ATMOSYNC.RAW.TELEMETRY` table in Snowflake.

### 4. Analytical transformations

dbt models clean and structure the telemetry, calculate exposure intervals, classify climate risk, estimate spoilage, evaluate financial impact, and compare alternative destinations.

### 5. Business intelligence

Power BI presents key indicators, climate risk distribution, estimated spoilage, financial impact by container, and rerouting recommendations.

The current dashboard uses **Import mode** and requires a refresh to retrieve updated data.

## Key Analytics

### Climate risk and exposure

- Classifies readings into `NORMAL`, `WARNING`, and `CRITICAL` categories.
- Uses `LAG()` and timestamp differences to estimate the interval between successive readings.
- Aggregates climate readings and exposure at container level.

### Spoilage estimation

The model combines warning exposure, critical exposure, temperature severity, humidity severity, and vibration into a weighted heuristic, capped at 25%.

The coefficients are simulation assumptions and are not a scientifically validated food-spoilage model.

### Financial impact

The analytical layer estimates spoiled quantity, remaining usable quantity, spoilage-related financial loss, and usable shipment value using simulated market prices.

### Arbitrage and rerouting

Alternative destinations are evaluated using estimated usable value and simulated route costs. The model recommends rerouting only when the estimated net opportunity is positive.

Market prices and route costs are illustrative assumptions, not live market data or actual shipping quotes.

## Dashboard and Deliverables

### Power BI dashboard

The executive overview includes:

- Total containers monitored
- Critical containers
- Estimated spoiled quantity
- Estimated spoilage-related financial loss
- Rerouting opportunities
- Climate risk distribution
- Spoilage by commodity
- Financial loss by container
- Rerouting recommendations

Dashboard file: [`powerbi/dashboards/AtmoSync_Dashboard.pbix`](powerbi/dashboards/AtmoSync_Dashboard.pbix)

### Project review presentation

The final project review presentation is available here:

[`powerbi/documentation/AtmoSync_Final_Review_Presentation.pptx`](powerbi/documentation/AtmoSync_Final_Review_Presentation.pptx)

## Repository Structure

```text
AtmoSync/
├── atmosync/                  # dbt project, models, seeds and tests
├── docs/
│   └── project/
│       └── data_dictionary.md
├── powerbi/
│   ├── dashboards/
│   │   └── AtmoSync_Dashboard.pbix
│   └── documentation/
│       └── AtmoSync_Final_Review_Presentation.pptx
├── simulator/                 # Python telemetry simulator
├── streaming/
│   ├── producers/              # Kafka producer
│   └── consumers/              # Kafka consumer
├── .gitignore
└── README.md
```

## Key Results

The validated example output from the current analytical models includes:

| Indicator | Example result |
|---|---:|
| Containers analyzed | 3 |
| Containers with critical readings | 2 |
| Estimated spoiled quantity | 473.06 kg |
| Estimated spoilage-related financial loss | ₹57,217.30 |
| Containers with positive estimated rerouting opportunities | 1 |
| dbt data-quality tests passed | 25 of 25 |

These results describe the current simulated dataset and model assumptions. They should not be interpreted as actual commercial losses or validated operational forecasts.

## Data Quality and Validation

The dbt project includes tests for key fields, unique identifiers, accepted risk and routing values, and expected analytical model structure.

**Validation result:** 25 tests passed, with no warnings or errors in the recorded test run.

## Getting Started

### Prerequisites

- Python
- Apache Kafka
- A Snowflake account with the required database, schemas, tables, and permissions
- dbt Core with the dbt Snowflake adapter
- Power BI Desktop for viewing the dashboard

### 1. Clone the repository

```bash
git clone https://github.com/SHREYASHRAW/AtmoSync.git
cd AtmoSync
```

### 2. Create and activate a Python environment

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the Python dependencies required by the simulator and streaming components. If a project dependency file is available, use it to install the pinned dependencies.

### 3. Configure the infrastructure

Set up Kafka and the `atmosync-telemetry` topic. Configure Snowflake database access and the Kafka Connect Snowflake connector.

Keep credentials and private keys outside version control. Do not commit passwords, private keys, or local environment files.

### 4. Configure dbt

Install the dbt Snowflake adapter and configure the `atmosync` profile in your local dbt profiles file.

From the dbt project directory:

```bash
dbt debug
dbt test
```

Run `dbt run` after confirming the Snowflake connection and required raw tables and seeds are available.

### 5. View the dashboard

Open `powerbi/dashboards/AtmoSync_Dashboard.pbix` in Power BI Desktop. Configure access to the required Snowflake objects if prompted, then refresh the imported data when needed.

> Infrastructure configuration and credentials are environment-specific. The steps above describe the setup requirements; they do not imply that a fresh installation has been tested on every machine.

## Limitations and Future Improvements

- Replace simulated telemetry with real sensor data when available.
- Validate climate thresholds and spoilage estimates with domain experts and labeled historical data.
- Replace illustrative market prices and route costs with verified data sources.
- Add automated alerting for critical climate conditions.
- Evaluate predictive models when sufficient reliable historical data becomes available.
- Automate dashboard refresh and deployment for a more operational workflow.

## Author

**Shreyash Rawate**

Computer Science Engineer | Data Analytics and Data Science

GitHub: [@SHREYASHRAW](https://github.com/SHREYASHRAW)

---

*AtmoSync is a portfolio project demonstrating data engineering, analytics, and business intelligence concepts using simulated agricultural shipment telemetry.*
