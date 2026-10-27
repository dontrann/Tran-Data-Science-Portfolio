# Tidy Data Project

## Project Overview

This project focuses on cleaning, organizing, and visualizing data from the 2008 Summer Olympics using Python and pandas. The goal is to transform the original dataset into a tidy format that is easier to analyze.

The three principles of tidy data are:

1. Each variable should have its own column.

2. Each observation should have its own row.

3. Each type of observational unit should form its own table.

## Instructions for Running the Notebook
1. Download TidyData_Olympics_2008_Class_Aligned.ipynb and olympics_08_medalists.csv from this GitHub folder.
2. Open the notebook 
3. Make sure Python and the required libraries are installed.
4. Keep the CSV file in the same folder as the notebook.
5. Run all the cells in order.

To install the required libraries, use: "pip install pandas matplotlib seaborn"

## Dataset Description 
The dataset used in this project is olympics_08_medalists.csv, which was provided as part of the class assignment. It contains information about medalists from the 2008 Summer Olympics.

The original dataset contains 1,875 rows and 71 columns. It includes medalist names and separate columns for sports and genders, with medal values recorded as gold, silver, or bronze.

To clean and organize the dataset, I:

- Used pd.melt() to reshape the data from wide format to long format.
- Used dropna() to remove rows without recorded medals.
- Used str.split() to separate gender and sport into their own columns.
- Used str.replace() to clean unwanted characters.
- Checked for missing values and duplicate records.

After cleaning, the dataset contains four columns: medalist_name, gender, sport, and medal. This makes the data easier to organize, analyze, and visualize.

## References 
- Pandas Cheat Sheet (https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf)
- Tidy Data Principles by Hadley Wickham (https://vita.had.co.nz/papers/tidy-data.pdf)

## Visualizations
<img width="573" height="317" alt="Screenshot 2026-10-27 at 2 00 54 AM" src="https://github.com/user-attachments/assets/1a3c345e-a88c-4be0-8a60-a8d7e398563c" />

<img width="573" height="379" alt="Screenshot 2026-10-27 at 2 01 09 AM" src="https://github.com/user-attachments/assets/89e0f700-62ab-40bf-a551-057307c626e6" />

