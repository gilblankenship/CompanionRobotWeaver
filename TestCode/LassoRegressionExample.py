import numpy as np

def lasso_regression(X, y, lamb):
    """
    Perform lasso regression on the data.

    Parameters
    ----------
    X : ndarray
        The feature matrix.
    y : ndarray
        The target vector.
    lam : float
        The regularization parameter.

    Returns
    -------
    theta : ndarray
        The coefficients of the lasso regression model.
    """

    theta = np.zeros(X.shape[1])

    for i in range(100000):
        J = 1/(2*len(y)) * np.sum((y - X @ theta)**2) + lamb * np.sum(np.abs(theta))
        gradient = 1/(2*len(y)) * (X.T @ (X @ theta - y)) + lamb * np.sign(theta)
        theta = theta - gradient

    return theta

def main():
    # Generate some data.
    X = np.random.rand(100, 2)
    y = 2*X[:, 0] + 3*X[:, 1] + np.random.rand(100)

    # Fit the lasso regression model.
    theta = lasso_regression(X, y, 0.1)

    # Print the coefficients.
    print(theta)

if __name__ == "__main__":
    main()
