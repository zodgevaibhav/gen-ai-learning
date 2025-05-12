# Ensamble Learning : Getting the answer of multiple models and combine together
    # It is a machine learning paradigm that combines multiple models to improve performance.
    # It can be used for both classification and regression tasks.
    # Can it combinely use classification and regression models? 
        # Yes, ensemble learning can combine both classification and regression models.
        # For example, you can create an ensemble that includes decision trees (for classification) and linear regression (for regression).
# Ensemble learning methods can be broadly categorized into two types:
# 1. Bagging: It involves training multiple models independently and then combining their predictions.
#    Bagging methods are typically used to reduce variance and improve the stability of the model.
#    Examples of bagging methods include:
#    - Random Forest: An ensemble of decision trees trained on different subsets of the data.
#    - Bootstrap Aggregating (Bagging): A general technique for creating ensembles by training models on bootstrapped samples of the data.
#
# 2. Boosting: It involves training models sequentially, where each model tries to correct the errors of the previous one.
#    Boosting methods are typically used to reduce bias and improve the accuracy of the model.
#    Examples of boosting methods include:
#    - AdaBoost: An ensemble method that combines weak classifiers to create a strong classifier.
#    - Gradient Boosting: An ensemble method that builds models sequentially, optimizing a loss function.
#    - XGBoost: An optimized version of gradient boosting that is faster and more efficient.
#    - LightGBM: A gradient boosting framework that uses tree-based learning algorithms.
#    - CatBoost: A gradient boosting library that handles categorical features automatically.
#
# 3. Stacking: It involves training multiple models and then using their predictions as input to a meta-model.
#    Stacking can be used to combine different types of models, such as decision trees, linear models, and neural networks.
#    The meta-model learns to make predictions based on the outputs of the base models.
#    Stacking can improve the overall performance of the ensemble by leveraging the strengths of different models.
#
# Ensemble learning is widely used in machine learning competitions and real-world applications due to its ability to improve model performance and robustness.
#