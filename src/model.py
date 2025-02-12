import torch
from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline, StableDiffusionInpaintPipeline, EulerDiscreteScheduler, PNDMScheduler
from PIL import Image
from diffusers.utils import make_image_grid, load_image
import numpy as np

from imageProcess import resize_image

class Txt2Img:
    def __init__(self, model_name="CompVis/stable-diffusion-v1-4", scheduler_type=None):
        try:
            self.pipeline = StableDiffusionPipeline.from_pretrained(model_name)

            schedulers = {
                "euler": EulerDiscreteScheduler,
                "pndm": PNDMScheduler
            }
            scheduler_class = schedulers.get(scheduler_type, None)

            if scheduler_class:
                self.pipeline.scheduler = scheduler_class.from_config(self.pipeline.scheduler.config)
            
            self.pipeline.to("cuda" if torch.cuda.is_available() else "cpu")
            
        except Exception as e:
            raise Exception(f"Error loading model: {e}")
            self.pipeline = None

    def txt2img(self, pos_prompt, neg_prompt, guidance=7.5, steps=50, width=512, height=512):
        prompts = [pos_prompt]
        if neg_prompt:
            prompts.append(neg_prompt)
        images = self.pipeline(
            prompt=prompts,
            guidance_scale=guidance,
            num_inference_steps=steps,
            width=width,
            height=height
        ).images

        return images[0]
    
class Img2Img:
    def __init__(self, model_name="runwayml/stable-diffusion-v1-5", scheduler_type=None):
        try:
            self.pipeline = StableDiffusionImg2ImgPipeline.from_pretrained(model_name, torch_dtype=torch.float16)
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            
            self.pipeline.to(self.device)
            
            schedulers = {
                "euler": EulerDiscreteScheduler,
                "pndm": PNDMScheduler
            }
            scheduler_class = schedulers.get(scheduler_type, None)

            if scheduler_class:
                self.pipeline.scheduler = scheduler_class.from_config(self.pipeline.scheduler.config)
            
        except Exception as e:
            raise Exception(f"Error loading model: {e}")
            self.pipeline = None
    
    def img2img(self, image, pos_prompt, neg_prompt, guidance=7.5, steps=50, strength=0.75):
        image = Image.open(image)
        image = resize_image(image=image)
        
        prompts = [pos_prompt]
        if neg_prompt:
            prompts.append(neg_prompt)
        
        generated_image = self.pipeline(
            prompt=prompts,
            num_inference_steps=steps,
            image=image,
            strength=strength,
            guidance_scale=guidance
        ).images[0]

        return generated_image

class Inpainting:
    def __init__(self, model_name="runwayml/stable-diffusion-inpainting", scheduler_type=None):
        try:
            self.pipeline = StableDiffusionInpaintPipeline.from_pretrained(model_name, torch_dtype=torch.float16)
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            
            self.pipeline.to(self.device)
            
            schedulers = {
                "euler": EulerDiscreteScheduler,
                "pndm": PNDMScheduler
            }
            scheduler_class = schedulers.get(scheduler_type, None)

            if scheduler_class:
                self.pipeline.scheduler = scheduler_class.from_config(self.pipeline.scheduler.config)
            
        except Exception as e:
            raise Exception(f"Error loading model: {e}")
            self.pipeline = None

    def inpainting(self, image, mask, pos_prompt, neg_prompt, guidance=7.5, steps=50, strength=0.75):
        """
        Runs Stable Diffusion Inpainting with a proper binary mask.
        """

        image = image.convert("RGB")

        mask = mask.convert("RGBA")

        mask_data = np.array(mask)
        alpha_channel = mask_data[:, :, 3]  # 4th channel in RGBA (0 = fully transparent, 255 = fully opaque)

        binary_mask = np.where(alpha_channel > 127, 255, 0).astype(np.uint8)

        mask = Image.fromarray(binary_mask, mode="L")

        target_size = (512, 512)
        image = image.resize(target_size, Image.LANCZOS)
        mask = mask.resize(target_size, Image.NEAREST)

        print(f"Mask converted to binary: unique values = {np.unique(binary_mask)}")
        print(f"Final image size: {image.size}, mode: {image.mode}")
        print(f"Final mask size: {mask.size}, mode: {mask.mode}")

        prompts = [pos_prompt]
        if neg_prompt:
            prompts.append(neg_prompt)

        generated_image = self.pipeline(
            prompt=prompts,
            num_inference_steps=steps,
            image=image,
            mask_image=mask,
            strength=strength,
            guidance_scale=guidance
        ).images[0]

        return generated_image