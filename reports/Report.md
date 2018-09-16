# Introduction

The goal of this analysis was to compare methods to for forecasting sales in
different stores and departments of Wal-Mart across the country. This was an
interesting challenge for me, because I am not as experienced with time-series
data as other forms of data. Most of my work is shown in Jupyter Notebooks which
I link to and provide a narrative for below.

The first thing I did to work on this problem was explore how others solved it.
This was a past Kaggle competition, so there were discussions from the top two
performers. The first place entry was described
[here](https://www.kaggle.com/c/walmart-recruiting-store-sales-forecasting/discussion/8125).
The contestant said that only the time-series data were used and none of the
other features. He combined several different models, most of which involved
using Singular Value Decomposition (SVD) to regularize the data during
preprocessing. His top performing model was STLF, but ARIMA did well too.

The [second place
solution](https://www.kaggle.com/c/walmart-recruiting-store-sales-forecasting/discussion/8023)
also made use of ARIMA, as well as Random Forest and a few other methods. It's
notable that neither of them used deep learning.

For the sake of time, I implemented SVD, ARIMA, and began an implementation of
Random Forest to compare. I developed reusable tools along the way as well.

# Exploratory Data Analysis

Before proceeding further, I analyzed the data, looking for obvious patterns and
observing where data are missing. My work is shown
[here](../notebooks/00_Exploratory-Data-Analysis.ipynb), but there were a few key
takeaways:

1. The data don't seem to have obvious increasing or decreasing trends over time
2. The data have strong seasonality, in that there are large spikes on holidays
   in some departments.
3. There was a lot of missing data, about 20% of the time series data. It didn't
   seem like there was an obvious pattern, so interpolating seemed like a
   reasonable strategy, and that's what I implemented for the remainder of the
   work.

# Baseline Model

Before implementing statistical learning models, I developed a baseline
model that simply looks up the previous year's sales for each particular
store/department combination. The work for this is shown [here](../notebooks/01_Baseline-Models.ipynb) I found that this simple baseline did quite well,
and submitting the results to Kaggle showed it would place around 180th out of
600 or so.

# ARIMA Model

Next, I implemented an ARIMA Model [here](../notebooks/03_ARIMA-Model.ipynb).
Unfortunately, the model was taking prohibitively long to run, as a separate
model was fit to each column. In order to reduce the time, I fit and predicted
on just Store 1. I showed that doing so, an SVD regularization with 10
components was optimal for reducing the error, and going much more or less
increased the error. Unfortunately without forecasting all the stores, I wasn't
able to submit to Kaggle for a comparison to the baseline on their holdout data.

# Random Forest

I was low on time, but I began setting up a Random Forest model
[here](../notebooks/04_Random-Forest.ipynb). I didn't get far, but if I had more time,
I would have set up a dataframe such that each store/department/time combination
would be paired with $m$ features representing the previous $m$ time points for
that store/department, and $n$ features centered around the time point a year
prior to that time at that store/department. Those features would be fairly
predictive.

# Conclusion

I demonstrated the value of SVD preprocessing, implemented a solid baseline, and
implemented an ARIMA model. The code was written in a way that makes it easy for
others to reuse. With more time I would have run the ARIMA model on the full
data and implemented a Random Forest to provide a full comparison between
different models.