from PIL import Image
from diffusers import DiffusionPipeline
import torch


class StableDiffusionGenerator:
    def __init__(self):
        self.model_id = "stabilityai/stable-diffusion-xl-base-1.0"
        self.base = DiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-base-1.0",
            torch_dtype=torch.float16,
            variant="fp16",
            use_safetensors=True,
        )
        self.base.enable_model_cpu_offload()

        self.refiner = DiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-refiner-1.0",
            text_encoder_2=self.base.text_encoder_2,
            vae=self.base.vae,
            torch_dtype=torch.float16,
            use_safetensors=True,
            variant="fp16",
        )
        self.refiner.enable_model_cpu_offload()

    def generate_image(self, prompt, name):
        augmented_prompt = f"In a colorful hand-drown comic horror style: {prompt}"
        negative_prompt = f"lowres, text, error, cropped, worst quality, low quality, jpeg artifacts, duplicate, out of frame, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck, speech bubbles, comic frames, words, titles"
        base_generation = self.base(
            prompt=augmented_prompt,
            negative_prompt=negative_prompt,
            denoising_end=0.75,
            output_type="latent",
        ).images
        generation = self.refiner(
            prompt=prompt,
            image=base_generation,
            num_inference_steps=40,
            denoising_start=0.75,
        ).images[0]
        generation.save(f"./images/{name}.png")
        return generation
