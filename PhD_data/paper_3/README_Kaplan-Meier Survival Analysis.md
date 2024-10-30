README: Kaplan-Meier Survival Analysis for *C. elegans*

This repository provides tools to perform Kaplan-Meier survival analysis on your *C. elegans* lifespan data and generate informative plots. Even with minimal Python knowledge, you can follow these steps to analyze your data.

**1. Prepare your data:**

* Open the `c_elegans_data_template.csv` file in a spreadsheet program (like Excel or Google Sheets).
* **For each experimental group, time point, and replicate:**
    * Enter the number of dead worms in the "Dead" column.
    * Enter the initial total number of worms in the "Total" column.
* **Important:** Make sure your time points are in hours.
* Save the file after entering your data.

**Example:**

|Group|Time|Replicate|Dead|Total|
|:---|:---|:---|:---|:---|
|Control|0|Rep1|2|50|
|Control|24|Rep1|5|50|
|Group1|0|Rep1|3|50|
|Group1|24|Rep1|8|50|

**2. Run the Python script:**

* Make sure you have Python installed on your computer.
* You'll also need to install the required Python packages (`pandas`, `lifelines`, `matplotlib`). You can do this by running the command `pip install pandas lifelines matplotlib` in your terminal or command prompt.
* Place your filled-in CSV file and the `KaplanMeier_script.py` script in the same folder.
* Open a terminal or command prompt, navigate to that folder, and run the script using the command `python KaplanMeier_script.py`.

**3. Interpret the results:**

* The script will generate a plot with two subplots:
    * **A:** Kaplan-Meier curves for all groups.
    * **B:** Kaplan-Meier curves for groups that are statistically significantly different from the control group.
* The script will also print the p-values of the log-rank tests, which compare each group to the control group.

**Key points:**

* The Kaplan-Meier curves show the probability of survival over time for each group.
* The log-rank test determines if there are significant differences in survival between groups.
* A p-value less than 0.05 indicates a statistically significant difference.

This README provides a basic guide for using the provided scripts. With a little effort, you can use these tools to gain valuable insights from your *C. elegans* survival data.
