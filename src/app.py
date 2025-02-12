import gradio as gr
from model import Txt2Img, Img2Img, Inpainting
from imageProcess import convert_to_png
from PIL import Image
import numpy as np

def generate_img_from_txt(pos_prompt, neg_prompt, guidance, step, width, height):
    model_txt2img = Txt2Img()
    generated_image = model_txt2img.txt2img(
        pos_prompt,
        neg_prompt,
        guidance=guidance,
        steps=step,
        width=width,
        height=height
    )
    del model_txt2img
    return generated_image

def generate_img_from_img(image_path, pos_prompt, neg_prompt, strength, guidance, step):
    model_img2img = Img2Img()
    generated_image = model_img2img.img2img(
        image=image_path,
        pos_prompt=pos_prompt,
        neg_prompt=neg_prompt,
        guidance=guidance,
        steps=step,
        strength=strength
    )
    del model_img2img
    return generated_image

def generate_image_from_paint(editor_value, pos_prompt, neg_prompt, strength, guidance, step):
    model_paint2img = Inpainting()
    original_image = editor_value["background"]
    mask_layers = editor_value["layers"]

    if not mask_layers:
        raise ValueError("No mask layers found!")

    merged_mask = np.zeros_like(np.array(mask_layers[0]))  

    for layer in mask_layers:
        merged_mask = np.maximum(merged_mask, np.array(layer))  

    merged_mask = (merged_mask > 127).astype(np.uint8) * 255
    mask_image = Image.fromarray(merged_mask)

    generated_image = model_paint2img.inpainting(
        image=original_image,
        mask=mask_image,
        pos_prompt=pos_prompt,
        neg_prompt=neg_prompt,
        guidance=guidance,
        steps=step,
        strength=strength
    )
    del model_paint2img
    return generated_image

def create_txt2img_interface():
    with gr.Blocks() as txt2img_interface:
        gr.Markdown("# Text to Image Generator")
        
        with gr.Row():  # Row to separate input, parameters, and output
            with gr.Column():
                pos_prompt = gr.Textbox(label="Positive Prompt")
                neg_prompt = gr.Textbox(label="Negative Prompt", placeholder="Optional prompt", value="")
            with gr.Column():
                guidance = gr.Slider(1.0, 10.0, value=7.5, label="Guidance Scale")
                steps = gr.Slider(1, 50, value=25, label="Number of Steps")
                width = gr.Slider(128, 1024, value=512, label="Width")
                height = gr.Slider(128, 1024, value=512, label="Height")
                generate_button = gr.Button("Generate")
            with gr.Column():
                output_image = gr.Image(label="Generated Image")

        generate_button.click(generate_img_from_txt, 
                              inputs=[pos_prompt, neg_prompt, guidance, steps, width, height], 
                              outputs=output_image)
    return txt2img_interface

def create_img2img_interface():
    with gr.Blocks() as img2img_interface:
        gr.Markdown("# Image to Image Generator")
        
        with gr.Row():
            with gr.Column():
                image_input = gr.Image(label="Input Image", type="filepath")
                pos_prompt = gr.Textbox(label="Positive Prompt")
                neg_prompt = gr.Textbox(label="Negative Prompt", placeholder="Optional prompt", value="")
            with gr.Column():
                strength = gr.Slider(0.0, 1.0, value=0.75, label="Strength")
                guidance = gr.Slider(1.0, 10.0, value=7.5, label="Guidance Scale")
                steps = gr.Slider(1, 50, value=25, label="Number of Steps")
                generate_button = gr.Button("Generate")
            with gr.Column():
                output_image = gr.Image(label="Generated Image")

        generate_button.click(generate_img_from_img, 
                              inputs=[image_input, pos_prompt, neg_prompt, strength, guidance, steps], 
                              outputs=output_image)
    return img2img_interface

def create_paint_interface():
    with gr.Blocks() as paint_interface:
        gr.Markdown("# Image and Mask Editor")

        with gr.Row():
            with gr.Column():
                image_editor = gr.ImageEditor(
                    label="Upload and Edit Image",
                    type="pil",
                    brush=gr.Brush(colors=["#FFFFFF"], color_mode="fixed"),
                    layers=True,
                )
                pos_prompt = gr.Textbox(label="Positive Prompt")
                neg_prompt = gr.Textbox(label="Negative Prompt", placeholder="Optional prompt", value="")
            with gr.Column():
                strength = gr.Slider(0.0, 1.0, value=0.75, label="Strength")
                guidance = gr.Slider(1.0, 10.0, value=8.0, label="Guidance Scale")
                steps = gr.Slider(1, 50, value=25, label="Number of Steps")
                process_button = gr.Button("Generate")
            with gr.Column():
                output_mask = gr.Image(label="Generated Mask")

        process_button.click(generate_image_from_paint,
                             inputs=[image_editor, pos_prompt, neg_prompt, strength, guidance, steps],
                             outputs=output_mask)

    return paint_interface

def create_footer():
    with gr.Row():
        gr.Markdown(
            """
            <div style="display: flex; justify-content: center; align-items: center;">
                <a href="https://github.com/Lilien86" style="font-size:18px; text-decoration:none; color:#5C6BC0; margin-right:16px; display: flex; align-items: center;">
                    <img src="https://github.com/user-attachments/assets/f2f07e31-5f0f-426a-b047-30e217ff26cf" width="24" height="24" style="vertical-align:middle; margin-right:8px;" /> GitHub
                </a>
                <a href="https://www.linkedin.com/in/lilien-auger-93b1b2258/" style="font-size:18px; text-decoration:none; color:#0077b5; display: flex; align-items: center;">
                    <img src="https://github.com/user-attachments/assets/4f196275-03b9-4950-818a-71d2d5e68946" width="24" height="24" style="vertical-align:middle; margin-right:8px;" /> LinkedIn
                </a>
            </div>
            """
        )
        
def combined_interface():
    with gr.Blocks() as interface:
        gr.Markdown(
            """
            <div style="text-align:center;">
                <img src="https://github.com/user-attachments/assets/1eabd996-3b37-480c-b27c-57f392ee7f36" alt="Welcome Image" width="100" />
                <h1>Welcome to My Image Generator App</h1>
                <p>This app allows you to generate images from text, modify images, or inpaint with prompts.</p>
            </div>
            """
        )
        
        create_footer()
        
        with gr.Row():
            gr.Markdown("### Explore the features below:")

        with gr.Tab("Text to Image"):
            create_txt2img_interface()
        
        with gr.Tab("Image to Image"):
            create_img2img_interface()

        with gr.Tab("Image Inpainting"):
            create_paint_interface()

    interface.launch()

if __name__ == "__main__":
    combined_interface()
