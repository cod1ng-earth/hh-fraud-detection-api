from keras.models import load_model
import numpy as np

autoencoder = load_model('model.h5')


def transform(originalValues):
    # the first line of "X_test_AE"
    return [[-2.83734569e+00,  9.83227741e-01,  2.73217562e-01, -4.78524696e-03,
             5.23113546e-02, -1.04610328e-03,  4.69188007e-02,  2.90218719e-02,
             1.25953972e-02, -3.60372131e-01,  9.00870408e-02,  7.19589387e-02,
             -7.79629676e-02, -3.79993916e-02,  1.02092528e-01, -3.35155292e-02,
             -1.48795630e-02,  1.97393418e-02, -1.22867991e-01,  4.32997898e-02,
             -1.42723225e-03, -9.13176842e-02,  1.81666606e-02, -4.26211488e-02,
             -4.27991657e-02,  4.06663542e-02,  4.96137126e-02, -4.97330536e-03,
             3.21861799e-02]]


def callModel(input):

    q = transform(input)
    prediction = autoencoder.predict(np.array(q))
    return prediction.tolist()
