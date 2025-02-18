# 🎨 Image_Generator_SD

## Overview

**Image_Generator_SD** is a web application that allows you to generate or modify images using **Stable Diffusion** models through a user-friendly **Gradio** interface. This project combines three core functionalities:

1. **Txt2Img**: Generate images from scratch using text prompts.
2. **Img2Img**: Transform an existing image guided by text prompts.
3. **Inpainting**: Modify or fill specific regions of an image using masks and text prompts.

---

## 🎥 Demonstration Video

Below is a personal demonstration video showcasing how to use and interact with the application:

![txt2img-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/4bf6c263-f515-4617-bedc-5993c6452c98)

---

## 🔎 What is Gradio?

[Gradio](https://gradio.app/) is an open-source Python library that enables developers to create customizable web interfaces for machine learning models with minimal code. Founded in 2019 by Abubakar Abid and colleagues, Gradio was designed to make machine learning models more accessible and interactive for users without requiring specialized software or expertise. 

In 2021, Gradio was acquired by Hugging Face.

Gradio interfaces are practical for developers and data scientists during the development and testing phases and are also highly valuable for showcasing models to stakeholders, clients, or users. By providing an interactive and user-friendly interface, Gradio allows non-technical users to quickly understand and interact with the underlying machine learning models, fostering collaboration and feedback.

---

## 🧠 What is Stable Diffusion?

[Stable Diffusion](https://github.com/CompVis/stable-diffusion) is a deep learning text-to-image model released in 2022, leveraging diffusion technology and latent space for efficient processing. This significantly reduces hardware requirements, allowing it to run on consumer GPUs.

This model has inspired major open-source projects like **ControlNet**, which enables fine control over image generation using depth maps, pose estimation, and edge detection. **ComfyUI** offers a node-based, visual workflow to build complex Stable Diffusion pipelines without coding. **AnimateDiff** brings AI-driven animations to life by applying Stable Diffusion consistently across frames.

---

## 🛠 Code Structure

This project is organized around three major classes to handle different image generation workflows: [**Txt2Img**](https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/text2img), [**Img2Img**](https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/img2img), and [**Inpainting**](https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/inpaint). Each class is located in `model.py` and is utilized within different Gradio interfaces in `app.py`.

### 1️⃣ Txt2Img
<details>
  <summary><em>Code Explanation</em></summary>

- **Location**: `class Txt2Img` in `model.py`
- **Purpose**: Generate images from textual prompts (positive and optionally negative).
- **Key Steps**:
  1. Load a **StableDiffusionPipeline** (default: `"CompVis/stable-diffusion-v1-4"`).
  2. Move the pipeline to the available device (CUDA if available).
  3. Call `txt2img()` with the following parameters:
     - `pos_prompt` (required)
     - `neg_prompt` (optional negative prompt)
     - `guidance` scale
     - `steps` (number of inference steps)
     - `width` and `height` (image dimensions)

In `app.py`, the function `generate_img_from_txt(...)` orchestrates this process and returns the generated image to the user interface.
</details>

### 2️⃣ Img2Img
<details>
  <summary><em>Code Explanation</em></summary>

- **Location**: `class Img2Img` in `model.py`
- **Purpose**: Transform an existing image based on new prompts and parameters.
- **Key Steps**:
  1. Load a **StableDiffusionImg2ImgPipeline** (default: `"runwayml/stable-diffusion-v1-5"`).
  2. Resize the input image if necessary (via `resize_image()` in `imageProcess.py`).
  3. Call `img2img()` with parameters:
     - `image` (the original image file path)
     - `pos_prompt` & `neg_prompt`
     - `strength` (how strongly the prompt influences the final image)
     - `guidance` scale
     - `steps` (number of inference steps)

In `app.py`, the function `generate_img_from_img(...)` is triggered upon user interaction in the Img2Img tab.
</details>

### 3️⃣ Inpainting
<details>
  <summary><em>Code Explanation</em></summary>

- **Location**: `class Inpainting` in `model.py`
- **Purpose**: Fill or modify specific regions of an image using a mask.
- **Key Steps**:
  1. Load a **StableDiffusionInpaintPipeline** (default: `"runwayml/stable-diffusion-inpainting"`).
  2. Convert and prepare the mask from the user’s edits. This involves converting the alpha channel to a binary mask.
  3. Call `inpainting()` with parameters:
     - `image` (the original image)
     - `mask` (the area to modify)
     - `pos_prompt` & `neg_prompt`
     - `guidance` scale
     - `steps` (inference steps)
     - `strength` (influence of the prompt on changes)

In `app.py`, the function `generate_image_from_paint(...)` processes the edited image and mask from the Gradio `ImageEditor` component, then performs the inpainting.
</details>

---

## 🚀 Installation & Setup

To run this application on a Linux or Windows environment, follow these steps:

#### Linux / Mac
```bash
git clone https://github.com/YourUsername/Image_Generator_SD.git
cd Image_Generator_SD
./setup-linux.sh
```

#### Windows
```cmd
git clone https://github.com/YourUsername/Image_Generator_SD.git
cd Image_Generator_SD
.\setup-windows.bat
```

Once installed, open your browser and go to ``` http://127.0.0.1:7860 ```
