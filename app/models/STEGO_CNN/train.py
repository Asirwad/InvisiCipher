import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from app.models.STEGO_CNN.neuralNet import define_model

# Define the input shape of the images
input_shape = (256, 256, 3)

# Define the batch size and number of epochs
batch_size = 32
epochs = 10

# Define the paths to the training and validation directories
train_dir = "C:/1 My Files/test_256/"
val_dir = "C:/1 My Files/validation/"

# Define the data generators for the training and validation sets
train_datagen = ImageDataGenerator(rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
train_generator = train_datagen.flow_from_directory(train_dir, target_size=input_shape[:2], batch_size=batch_size, class_mode='binary')
val_datagen = ImageDataGenerator(rescale=1./255)
val_generator = val_datagen.flow_from_directory(val_dir, target_size=input_shape[:2], batch_size=batch_size, class_mode='binary')

# Define the neural network architecture
model = define_model(output_shape=1)

# compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(train_generator, epochs=epochs, validation_data=val_generator)

# Save the trained model as an .h5 file
model.save("model.h5")
