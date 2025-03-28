"""
# Experience vs Salary Prediction

This program demonstrates how to use a simple linear regression model to predict salaries based on years of experience. The dataset used contains two columns: `Experience` (in years) and `Salary`.

## Features of the Program

1. **Data Loading**:
    ```python
    # Load the dataset from a CSV file
    data = pd.read_csv('salary_data.csv')
    ```
    - The dataset is loaded from a CSV file named `salary_data.csv`.

2. **Data Visualization**:
    ```python
    # Create a scatter plot to visualize the relationship
    plt.scatter(data['Experience'], data['Salary'])
    plt.xlabel('Experience (Years)')
    plt.ylabel('Salary')
    plt.title('Experience vs Salary')
    ```
    - A scatter plot is created to visualize the relationship between `Experience` and `Salary`.

3. **Statistical Analysis**:
    ```python
    # Calculate covariance and correlation
    covariance = np.cov(data['Experience'], data['Salary'])[0, 1]
    correlation = np.corrcoef(data['Experience'], data['Salary'])[0, 1]
    ```
    - Covariance and correlation between `Experience` and `Salary` are calculated to understand the relationship between the two variables.

4. **Model Training**:
    ```python
    # Train a linear regression model
    model = LinearRegression()
    model.fit(data[['Experience']], data['Salary'])
    ```
    - A linear regression model is trained using the `Experience` as the independent variable and `Salary` as the dependent variable.

5. **Prediction**:
    ```python
    # Predict salary for a given number of years of experience
    years_of_experience = 5
    predicted_salary = model.predict([[years_of_experience]])
    print(f"Salary of {years_of_experience} years of experience is: {predicted_salary[0]}")
    ```
    - The program predicts the salary for a given number of years of experience (e.g., 5 years).

## Notes

- Ensure the dataset is clean and contains no missing values for accurate predictions.
- The model assumes a linear relationship between `Experience` and `Salary`.
- Modify the `pd.DataFrame` input in the `model.predict` function to predict salaries for other experience values.
- Uncomment the print statements to view detailed dataset information.
"""
