# fitness-tracker-streamlit
 
## 💡 About
I'm a data nerd and fitness enthusiast at heart, so the opportunity to optimize my nutrition and training through my own data has always excited me. Yet despite having tracked results in apps like ``MyFitnessPal``, ``Crossfit btwb``, ``Stronglifts 5x5``, and ``Apple Health`` since 2013, I've always been disappointed by the lack of integration and limited insights among these apps. That's why I decided to create a personal app to show me the insights I want from my own fitness data.

## 🚀 Features
I've kept the app pretty simple as it's for personal use:
* **Data Sources**: Integrate data from ``MyFitnessPal`` (nutrition), ``Crossfit btwb`` (workouts), and ``Apple Health`` (steps). A preprocessed version of data collated from each of these data sources is pulled from an ``S3`` bucket.
  * Pulling data from apps directly: ``MyFitnessPal`` has an API, but it's private - [python-myfitnesspal](https://github.com/coddingtonbear/python-myfitnesspal) is a promising alternative for programmatic access and ``MFP`` also supports bulk exports. ``Crossfit btwb`` only supports bulk csv exports. ``Apple Health`` supports bulk exports and programmatic access via [HealthKit](https://developer.apple.com/documentation/healthkit).
* **Data Transformation**: The app performs some intermediate calculations on the sourced data to generate initial summary results and format the data for visualizations in the app.
* **Multi-Page Streamlit App**:
  * **Overview**: A summary table with weekly aggregated stats on metrics for health (weight, delta from prevous week), nutrition (calories, protein intake), and training (#lifting and condition days, step count). I've found this useful to get a rough sense of how much I need to eat and how often I need to exercise to see a meaningful change in metrics like weight/body fat percentage. This table can be exported to csv via a Download button.
  * **Visualizations**: Here's the fun stuff. This page generates a few time-series plots (interactive via ``plotly``) to show trends for weight, caloric intake, steps, and workouts. You can filter on dates and aggregate over days, weeks, and months to visualize the trends on different scales. There's also a summary table for which exercises I do most frequently.
  * **Raw Data**: It's often useful to see the underlying raw data used for calculations and visualizations, so I've made this available for viewing/download.

## 🌐 Getting Started

### Configuration
The dashboard is set up to run with ``Docker`` and ``AWS``, so the former should be installed and credentials for the latter should be configured/present.

### Installation
```
git clone https://github.com/hsrishi/fitness-tracker-streamlit.git
cd fitness-tracker-streamlit

docker build . -t fitness-tracker-streamlit
```

### Running the App
```
docker run -d -p 8501:8501 -v ~/.aws:/root/.aws fitness-tracker-streamlit
```

### Hosting the App

I don't recommend hosting the app on a server as it's primarily intended for personal use (trivial to run locally, expense of hosting is unnecessary), but it's built with ``docker`` so deploying to the cloud is fairly straightforward. A small ``EC2`` instance (e.g. ``t2.micro``) is more than enough compute to run the app and you can use container services (``ECR``, ``ECS``) to manage docker deployment.

# ⚖️ License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
