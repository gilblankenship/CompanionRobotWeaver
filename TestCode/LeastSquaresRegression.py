import numpy as np

def simple_least_squares_fit(X, y):
    """
    Perform simple least squares fit on the data.

    Parameters
    ----------
    X : ndarray
        The feature matrix.
    y : ndarray
        The target vector.

    Returns
    -------
    theta : ndarray
        The coefficients of the simple least squares model.
    """

    theta = np.linalg.inv(X.T @ X) @ X.T @ y

    return theta

def main():
    # Generate some data.
    X = np.random.rand(100, 2)
    y = 2*X[:, 0] + 3*X[:, 1] + np.random.rand(100)

    # Fit the simple least squares model.
    theta = simple_least_squares_fit(X, y)

    # Print the coefficients.
    print(theta)

if __name__ == "__main__":
    main()
