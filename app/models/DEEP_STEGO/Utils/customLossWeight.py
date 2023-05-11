from tensorflow.keras.losses import mean_squared_error


# Loss functions
def custom_loss_1(secret, secret_pred):
    # Compute L2 loss(MSE) for secret image
    secret_mse = mean_squared_error(secret, secret_pred)
    return secret_mse


def custom_loss_2(cover, cover_predict):
    # Compute L2 loss(MSE) for cover image
    cover_mse = mean_squared_error(cover, cover_predict)
    return cover_mse
