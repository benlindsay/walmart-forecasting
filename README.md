[![Build Status](https://travis-ci.org/benlindsay/al-takehome-problem.svg?branch=master)](https://travis-ci.org/benlindsay/al-takehome-problem)

air-liquide-takehome-problem
==============================

This repository contains my analysis of ???. I split my analysis into several Jupyter notebooks. To walk through my analysis, click on the links to the notebooks below. Look at the instructions at the bottom of this file if you want to reproduce or modify this analysis on your machine.

## Analysis

1. [Exploratory Data Analysis](notebooks/test_nb.ipynb)
2. [Interactive Dashboard](https://takehomeproblem.herokuapp.com/) made with Plotly Dash and hosted on Heroku

## Reproducing this analysis locally

These are the steps you'll need to take the first time you touch this:

0. Clone this repo:

```
git clone <this repo url>
```

1. Create a conda environment if conda is available, or pip environment otherwise.

```
make create_environment
```

2. Activate the new environment. With conda, this looks like

```
source activate altakehome
```

With pip it looks like

```
workon altakehome
```

3. Install python requirements. (This will use pip even if you have a conda
   environment. That's just fine.)

```
make requirements
```

4. Create `.env` file by running `cp .env.template .env`. Put the correct tokens and passwords there. Several scripts rely on `.env` to find the this project's root directory.

Every time you want to come back and run some analysis code, you'll need to run
`source activate altakehome` first to reactivate the environment you created.

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
