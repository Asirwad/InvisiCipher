import os
import glob
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Input, concatenate, Conv2D, GaussianNoise
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam
import tensorflow.keras.backend as K
from tensorflow.keras.utils import plot_model
from tensorflow.keras.callbacks import TensorBoard, ModelCheckpoint, Callback, ReduceLROnPlateau
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import mean_squared_error
# from tensorflow.keras.utils import multi_gpu_model
from PIL import Image
import matplotlib.pyplot as plt
from random import randint
import imageio
from io import StringIO, BytesIO
from app.models.DEEP_STEGO.Utils.preprocessing import normalize_batch, denormalize_batch
from app.models.DEEP_STEGO.Utils.customLossWeight import custom_loss_1, custom_loss_2

tf.compat.v1.disable_v2_behavior()

# %matplotlib inline

# Configure file paths
TRAIN = "dataset/train_data"
VALIDATION = "dataset/val_data"
TRAIN_NUM = len(glob.glob(TRAIN + "/*/*"))
VAL_NUM = len(glob.glob(VALIDATION + "/*/*"))
TEST_DATA = "test/testdata.npy"

CHECKPOINT = "checkpoints/steg_model-{epoch:02d}-{val_loss:.2f}.hdf5"
PRETRAINED = 'checkpoints/steg_model-04-0.03.hdf5'

# Configure batch size
BATCH_SIZE = 12

# Load test data as numpy arrays
test_images = np.load(TEST_DATA)

# Sample test data
test_secret = test_images[0].reshape((1, 224, 224, 3))
test_cover = test_images[1].reshape((1, 224, 224, 3))


# Image data generator
input_image_gen = ImageDataGenerator(rescale=1. / 255)
test_image_gen = ImageDataGenerator(rescale=1. / 255)


# Custom generator for loading training images from directory
def generate_generator_multiple(generator, direct):
    gen_X1 = generator.flow_from_directory(direct, target_size=(224, 224), batch_size=BATCH_SIZE, shuffle=True, seed=3, class_mode=None)
    gen_X2 = generator.flow_from_directory(direct, target_size=(224, 224), batch_size=BATCH_SIZE, shuffle=True, seed=8, class_mode=None)

    while True:
        X1i = normalize_batch(gen_X1.next())
        X2i = normalize_batch(gen_X2.next())

        yield ({'secret': X1i, 'cover': X2i},
               {'hide_conv_f': X2i, 'revl_conv_f': X1i})  # Yield both images and their mutual label


# Train data generator
input_generator = generate_generator_multiple(generator=input_image_gen, direc=TRAIN)

# Validation data generator
test_generator = generate_generator_multiple(test_image_gen, direc=VALIDATION)


# Custom loss dictionary
losses = {
    "hide_conv_f": custom_loss_2,
    "revl_conv_f": custom_loss_1,
}

# Loss weights
lossWeights = {"hide_conv_f": 1.0, "revl_conv_f": 0.75}


# Model architecture
def steg_model(pretrain=False):
    if pretrain:
        pretrained_model = load_model(PRETRAINED, custom_objects={'custom_loss_1': custom_loss_1, 'custom_loss_2': custom_loss_2})
        return pretrained_model

    # Inputs
    secret = Input(shape=(224, 224, 3), name='secret')
    cover = Input(shape=(224, 224, 3), name='cover')

    # Prepare network - patches [3*3,4*4,5*5]
    prepare_conv_3x3 = Conv2D(50, kernel_size=3, padding="same", activation='relu', name='prep_conv3x3_1')(secret)
    prepare_conv_3x3 = Conv2D(50, kernel_size=3, padding="same", activation='relu', name='prep_conv3x3_2')(prepare_conv_3x3)
    prepare_conv_3x3 = Conv2D(50, kernel_size=3, padding="same", activation='relu', name='prep_conv3x3_3')(prepare_conv_3x3)
    prepare_conv_3x3 = Conv2D(50, kernel_size=3, padding="same", activation='relu', name='prep_conv3x3_4')(prepare_conv_3x3)

    prepare_conv_4x4 = Conv2D(50, kernel_size=4, padding="same", activation='relu', name='prep_conv4x4_1')(secret)
    prepare_conv_4x4 = Conv2D(50, kernel_size=4, padding="same", activation='relu', name='prep_conv4x4_2')(prepare_conv_4x4)
    prepare_conv_4x4 = Conv2D(50, kernel_size=4, padding="same", activation='relu', name='prep_conv4x4_3')(prepare_conv_4x4)
    prepare_conv_4x4 = Conv2D(50, kernel_size=4, padding="same", activation='relu', name='prep_conv4x4_4')(prepare_conv_4x4)

    prepare_conv_5x5 = Conv2D(50, kernel_size=5, padding="same", activation='relu', name='prep_conv5x5_1')(secret)
    prepare_conv_5x5 = Conv2D(50, kernel_size=5, padding="same", activation='relu', name='prep_conv5x5_2')(prepare_conv_5x5)
    prepare_conv_5x5 = Conv2D(50, kernel_size=5, padding="same", activation='relu', name='prep_conv5x5_3')(prepare_conv_5x5)
    prepare_conv_5x5 = Conv2D(50, kernel_size=5, padding="same", activation='relu', name='prep_conv5x5_4')(prepare_conv_5x5)

    prepare_concat_1 = concatenate([prepare_conv_3x3, prepare_conv_4x4, prepare_conv_5x5], axis=3, name="prep_concat_1")

    prepare_conv_5x5 = Conv2D(50, kernel_size=5, padding="same", activation='relu', name='prep_conv5x5_f')(prepare_concat_1)
    prepare_conv_4x4 = Conv2D(50, kernel_size=4, padding="same", activation='relu', name='prep_conv4x4_f')(prepare_concat_1)
    prepare_conv_3x3 = Conv2D(50, kernel_size=3, padding="same", activation='relu', name='prep_conv3x3_f')(prepare_concat_1)

    prepare_prepare_concat_f1 = concatenate([prepare_conv_5x5, prepare_conv_4x4, prepare_conv_3x3], axis=3, name="prep_concat_2")

    # Hiding network - patches [3*3,4*4,5*5]
    hide_concat_h = concatenate([cover, prepare_prepare_concat_f1], axis=3, name="hide_concat_1")

    hide_conv_3x3 = Conv2D(50, kernel_size=3, padding="same", activation='relu', name='hide_conv3x3_1')(hide_concat_h)
    hide_conv_3x3 = Conv2D(50, kernel_size=3, padding="same", activation='relu', name='hide_conv3x3_2')(hide_conv_3x3)
    hide_conv_3x3 = Conv2D(50, kernel_size=3, padding="same", activation='relu', name='hide_conv3x3_3')(hide_conv_3x3)
    hide_conv_3x3 = Conv2D(50, kernel_size=3, padding="same", activation='relu', name='hide_conv3x3_4')(hide_conv_3x3)

    hide_conv_4x4 = Conv2D(50, kernel_size=4, padding="same", activation='relu', name='hide_conv4x4_1')(hide_concat_h)
    hide_conv_4x4 = Conv2D(50, kernel_size=4, padding="same", activation='relu', name='hide_conv4x4_2')(hide_conv_4x4)
    hide_conv_4x4 = Conv2D(50, kernel_size=4, padding="same", activation='relu', name='hide_conv4x4_3')(hide_conv_4x4)
    hide_conv_4x4 = Conv2D(50, kernel_size=4, padding="same", activation='relu', name='hide_conv4x4_4')(hide_conv_4x4)

    hide_conv_5x5 = Conv2D(50, kernel_size=5, padding="same", activation='relu', name='hide_conv5x5_1')(hide_concat_h)
    hide_conv_5x5 = Conv2D(50, kernel_size=5, padding="same", activation='relu', name='hide_conv5x5_2')(hide_conv_5x5)
    hide_conv_5x5 = Conv2D(50, kernel_size=5, padding="same", activation='relu', name='hide_conv5x5_3')(hide_conv_5x5)
    hide_conv_5x5 = Conv2D(50, kernel_size=5, padding="same", activation='relu', name='hide_conv5x5_4')(hide_conv_5x5)

    hide_concat_1 = concatenate([hide_conv_3x3, hide_conv_4x4, hide_conv_5x5], axis=3, name="hide_concat_2")

    hide_conv_5x5 = Conv2D(50, kernel_size=5, padding="same", activation='relu', name='hide_conv5x5_f')(hide_concat_1)
    hide_conv_4x4 = Conv2D(50, kernel_size=4, padding="same", activation='relu', name='hide_conv4x4_f')(hide_concat_1)
    hide_conv_3x3 = Conv2D(50, kernel_size=3, padding="same", activation='relu', name='hide_conv3x3_f')(hide_concat_1)

    hide_concat_f1 = concatenate([hide_conv_5x5, hide_conv_4x4, hide_conv_3x3], axis=3, name="hide_concat_3")

    cover_predict = Conv2D(3, kernel_size=1, padding="same", name='hide_conv_f')(hide_concat_f1)

    # Noise layer
    noise_ip = GaussianNoise(0.1)(cover_predict)

    # Reveal network - patches [3*3,4*4,5*5]
    reveal_conv_3x3 = Conv2D(50, kernel_size=3, padding="same", activation='relu', name='revl_conv3x3_1')(noise_ip)
    reveal_conv_3x3 = Conv2D(50, kernel_size=3, padding="same", activation='relu', name='revl_conv3x3_2')(reveal_conv_3x3)
    reveal_conv_3x3 = Conv2D(50, kernel_size=3, padding="same", activation='relu', name='revl_conv3x3_3')(reveal_conv_3x3)
    reveal_conv_3x3 = Conv2D(50, kernel_size=3, padding="same", activation='relu', name='revl_conv3x3_4')(reveal_conv_3x3)

    reveal_conv_4x4 = Conv2D(50, kernel_size=4, padding="same", activation='relu', name='revl_conv4x4_1')(noise_ip)
    reveal_conv_4x4 = Conv2D(50, kernel_size=4, padding="same", activation='relu', name='revl_conv4x4_2')(reveal_conv_4x4)
    reveal_conv_4x4 = Conv2D(50, kernel_size=4, padding="same", activation='relu', name='revl_conv4x4_3')(reveal_conv_4x4)
    reveal_conv_4x4 = Conv2D(50, kernel_size=4, padding="same", activation='relu', name='revl_conv4x4_4')(reveal_conv_4x4)

    reveal_conv_5x5 = Conv2D(50, kernel_size=5, padding="same", activation='relu', name='revl_conv5x5_1')(noise_ip)
    reveal_conv_5x5 = Conv2D(50, kernel_size=5, padding="same", activation='relu', name='revl_conv5x5_2')(reveal_conv_5x5)
    reveal_conv_5x5 = Conv2D(50, kernel_size=5, padding="same", activation='relu', name='revl_conv5x5_3')(reveal_conv_5x5)
    reveal_conv_5x5 = Conv2D(50, kernel_size=5, padding="same", activation='relu', name='revl_conv5x5_4')(reveal_conv_5x5)

    reveal_concat_1 = concatenate([reveal_conv_3x3, reveal_conv_4x4, reveal_conv_5x5], axis=3, name="revl_concat_1")

    reveal_conv_5x5 = Conv2D(50, kernel_size=5, padding="same", activation='relu', name='revl_conv5x5_f')(reveal_concat_1)
    reveal_conv_4x4 = Conv2D(50, kernel_size=4, padding="same", activation='relu', name='revl_conv4x4_f')(reveal_concat_1)
    reveal_conv_3x3 = Conv2D(50, kernel_size=3, padding="same", activation='relu', name='revl_conv3x3_f')(reveal_concat_1)

    reveal_concat_f1 = concatenate([reveal_conv_5x5, reveal_conv_4x4, reveal_conv_3x3], axis=3, name="revl_concat_2")

    secret_predict = Conv2D(3, kernel_size=1, padding="same", name='revl_conv_f')(reveal_concat_f1)

    model = Model(inputs=[secret, cover], outputs=[cover_predict, secret_predict])

    # Multi GPU training  (Uncomment the following line)
    # model = multi_gpu_model(model, gpus=2)

    # Compile model
    model.compile(optimizer='adam', loss=losses, loss_weights=lossWeights)

    return model


# Model object
model = steg_model(pretrain=False)

# Summarize layers
print(model.summary())

# Plot graph
# plot_model(model, to_file='steg_model.png')

# Tensorboard
tensorboard = TensorBoard(log_dir='./logs', histogram_freq=0,
                          write_graph=True, write_images=True)

# TF file writer for images
im_writer = tf.summary.FileWriter('./logs/im')


# TF image logger
def log_images(tag, images, step):
    """Logs a list of images."""

    im_summaries = []
    for nr, img in enumerate(images):
        # Write the image to a string
        s = BytesIO()
        plt.imsave(s, img, format='png')

        # Create an Image object
        img_sum = tf.Summary.Image(encoded_image_string=s.getvalue(),
                                   height=img.shape[0],
                                   width=img.shape[1])
        # Create a Summary value
        im_summaries.append(tf.Summary.Value(tag='%s/%d' % (tag, nr),
                                             image=img_sum))

    # Create and write Summary
    summary = tf.Summary(value=im_summaries)
    im_writer.add_summary(summary, step)


# Custom keras image callback
class TensorBoardImage(Callback):
    def __init__(self, tag):
        super().__init__()
        self.tag = tag

    def on_epoch_end(self, epoch, logs={}):
        # Load random test images
        secret_in = test_images[np.random.choice(len(test_images), size=4, replace=False)]
        cover_in = test_images[np.random.choice(len(test_images), size=4, replace=False)]

        # Predict on batch
        cover_out, secret_out = model.predict([normalize_batch(secret_in), normalize_batch(cover_in)])

        # Post process output cover image
        cover_out = denormalize_batch(cover_out)
        cover_out = np.squeeze(cover_out) * 255.0
        cover_out = np.uint8(cover_out)

        # Post process output secret image
        secret_out = denormalize_batch(secret_out)
        secret_out = np.squeeze(secret_out) * 255.0
        secret_out = np.uint8(secret_out)

        # Convert images to UINT8 format (0-255)
        cover_in = np.uint8(np.squeeze(cover_in * 255.0))
        secret_in = np.uint8(np.squeeze(secret_in * 255.0))

        # Log image summary
        log_images("cover_in", cover_in, epoch)
        log_images("secret_in", secret_in, epoch)
        log_images("cover_out", cover_out, epoch)
        log_images("secret_out", secret_out, epoch)

        return


# Custom image logger
image_summary = TensorBoardImage('Image Example')

# Checkpoint path
filepath = CHECKPOINT

# Callback functions
checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_weights_only=False, save_best_only=True,
                             mode='min')
reduce_lr = ReduceLROnPlateau(factor=0.5, patience=3, min_lr=0.000001, verbose=1)
callbacks_list = [checkpoint, tensorboard, image_summary, reduce_lr]

# Train the model
model.fit_generator(input_generator, epochs=100,
                    steps_per_epoch=TRAIN_NUM // BATCH_SIZE,
                    validation_data=test_generator,
                    validation_steps=VAL_NUM // BATCH_SIZE,
                    use_multiprocessing=True,
                    callbacks=callbacks_list)

'''
Sample run: python train.py
'''
