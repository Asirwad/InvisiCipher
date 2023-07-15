<h1 align="center">
  InvisiCipher : Deep Learning-Based image Steganography with Chaotic Encryption and
Enhanced Super Resolution
</h1>

<p align="center">
  <img src="app/ui/logo.png" alt="Project Logo" width="100">
</p>

<p align="center">
  <strong>Hide secrets, enhance images!</strong>
</p>

## Overview

Welcome to our Steganography and Super Resolution project! This project combines the power of steganography techniques and super-resolution using deep learning models. Our goal is to hide a secret image within a cover image using advanced convolutional neural networks (CNNs) and then enhance the quality of the hidden image using an Enhanced Super Resolution Generative Adversarial Network (ESRGAN). We also provide an option to encrypt the steg image using various chaos encryption algorithms for added security.

## Features

✨ **Interactive Hiding**: Utilize our intuitive hide network powered by CNNs to embed secret images within cover images effortlessly.

🔒 **Secure Encryption**: Choose from multiple chaos encryption algorithms such as AES, Blowfish to encrypt your steg image and protect your secrets.

🌟 **Enhanced Super Resolution**: Witness the magic of our ESRGAN model as it enhances the resolution and quality of the hidden image, revealing every detail.

🎨 **Easy-to-Use**: Our project provides a user-friendly interface and simple scripts to perform hiding, encryption, decryption, and image enhancement with just a few lines of code.

## Project Architecture

The project architecture consists of the following components:

1. **Prepare Network**: A CNN-based network that prepares the secret image for hiding by extracting essential features and encoding it.

2. **Hide Network**: Another CNN-based network that embeds the prepared secret image within the cover image, producing the steg image.

3. **Chaos Encryption**: Choose between AES encryption, Blowfish encryption to secure your steg image.

4. **Chaos Decryption**: Decrypt the encrypted steg image using the corresponding decryption algorithm to retrieve the steg image.

5. **Reveal Network**: A CNN-based network that extracts the secret image from the steg image by decoding the hidden information.

6. **ESRGAN**: Our Enhanced Super Resolution Generative Adversarial Network (ESRGAN) model enhances the quality and resolution of the extracted secret image.

## Getting Started

To get started with our project, follow these steps:

1. **Clone the Repository**: `git clone https://github.com/Asirwad/InvisiCipher.git`

2. **Install Dependencies**: Install the required dependencies by running `pip install -r requirements.txt`.

3. **Prepare Your Dataset**: Organize your cover and secret images dataset and place them in the appropriate directories.

4. **Customize Configuration**: Modify the configuration files to set the desired parameters for the models and encryption algorithms.

5. **Train the Models**: Run the training script to train the CNN models and ESRGAN: `python train.py`.

6. **Explore the Scripts**: Utilize the provided scripts to hide, encrypt, reveal, and enhance images based on your specific requirements.

## Welcome screen

<p align="center">
  <img src="app/ui/assets/readme_assets/main_window.png" alt="Welcome" width="1000">
</p>

## Image hide

<p align="center">
  <img src="app/ui/assets/readme_assets/hide.png" alt="Image hide" width="1000">
</p>

## Image reveal

<p align="center">
  <img src="app/ui/assets/readme_assets/reveal.png" alt="Image reveal" width="1000">
</p>

## Super resolution

<p align="center">
  <img src="app/ui/assets/readme_assets/superres.png" alt="Super resolution" width="1000">
</p>

## Contributing

We welcome contributions from the open source community. If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

## Acknowledgements

We would like to acknowledge the following resources and libraries used in this project:

- <img src="https://www.tensorflow.org/images/tf_logo_social.png" alt="TensorFlow" width="80" align="center"> TensorFlow: [https://www.tensorflow.org/](https://www.tensorflow.org/)
- <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/10/PyTorch_logo_icon.svg/1200px-PyTorch_logo_icon.svg.png"
 alt="PyTorch" width="25" align="center"> PyTorch: [https://pytorch.org/](https://pytorch.org/)

## Contact

For any questions or inquiries, please contact us at [asirwadsali@gmail.com](mailto:asirwadsali@gmail.com).

</div>
