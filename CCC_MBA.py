# Import the necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Ensure the directory path is properly set
directory = ()  # Update this with your actual directory path

# Call the appropriate columns from the DataFrame and convert them to NumPy arrays
measurement_1 = np.loadtxt('M_PELVIS_BC_X_combined.csv', delimiter=',', dtype=float) # Update this with your independent variable
measurement_2 = np.loadtxt('ML_PELVIS_BC_X_combined.csv', delimiter=',', dtype=float) # Update this with your dependent variable

# Calculate the mean of the measurements
mean_measurements = np.mean([measurement_1, measurement_2], axis=0)

# Calculate the difference between the measurements
diff_measurements = measurement_1 - measurement_2

# Calculate the mean and standard deviation of the differences
mean_diff = np.mean(diff_measurements)
std_diff = np.std(diff_measurements, ddof=1)

# Calculate the limits of agreement (mean ± 1.96*std)
loa_upper = mean_diff + 1.96 * std_diff
loa_lower = mean_diff - 1.96 * std_diff

# Calculate the 95% confidence interval for the limits of agreement
n = len(diff_measurements)
t_value = 1.96  # For a 95% confidence interval
ci_loa = t_value * std_diff / np.sqrt(n)

# Calculate the confidence interval for the limits of agreement
ci_upper = loa_upper - ci_loa
ci_lower = loa_lower + ci_loa

# Reassign the variable names
x = measurement_1
y = measurement_2

def concordance_correlation_coefficient(x, y):
    """Compute the Concordance Correlation Coefficient (CCC) between two sets of measurements."""
    
    # Calculate means
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    
    # Calculate variances
    var_x = np.var(x, ddof=1)
    var_y = np.var(y, ddof=1)
    
    # Calculate covariance
    covariance_xy = np.cov(x, y, ddof=1)[0, 1]
    
    # Calculate CCC
    ccc = (2 * covariance_xy) / (var_x + var_y + (mean_x - mean_y)**2)
    
    return ccc

# Calculate the CCC to three decimal places
ccc_value = concordance_correlation_coefficient(x, y)

print("Concordance Correlation Coefficient:", ccc_value)

# Plotting the Bland-Altman plot
plt.figure(figsize=(8, 6))
plt.scatter(x=mean_measurements, y=diff_measurements, color='black', alpha=1)

# Set the limits of the plot and plot the CCC value
x_lim = plt.gca().get_xlim()
y_lim = plt.gca().get_ylim()
plt.xlim(x_lim)
plt.ylim(y_lim)

# Horizontal lines for the mean and limits of agreement
plt.text(-7, -10, f"CCC: {ccc_value:.3f}", fontsize=8, color='black', fontstyle='italic')
plt.axhline(mean_diff, color='black', linestyle=':', label='Mean difference')
plt.text(-7, mean_diff + .2, f"Mean: {mean_diff:.3f}", fontsize=8, color='black', fontstyle='italic')
plt.axhline(loa_upper, color='black', linestyle='-', label='_nolegend_')
plt.axhline(loa_lower, color='black', linestyle='-', label='_nolegend_')
plt.axhline(loa_upper - ci_loa, color='black', linestyle='-')
plt.axhline(loa_lower + ci_loa, color='black', linestyle='-')
plt.axhline(0, color='black', linestyle='-')

# Fill between the limitis of agreement and the confidence interval
plt.fill_between(x_lim, loa_upper, ci_upper, color='gray', alpha=0.8)
plt.fill_between(x_lim, loa_lower, ci_lower, color='gray', alpha=0.8)

# Add labels and title
plt.title('Pelvic Angle X at Ball Contact')
plt.xlabel('Mean of Measurements(deg)')
plt.ylabel('Difference Between Measurements(deg)')
plt.legend(loc= 'upper left', fontsize= 'small')
plt.show()