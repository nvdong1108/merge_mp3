from diffusers import StableDiffusionPipeline
import torch

def generate_image(prompt, output_path="generated_image.png"):
    # Load pre-trained model from Hugging Face
    model_id = "CompVis/stable-diffusion-v1-4"
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")  # Chuyển sang GPU nếu có

    # Generate image
    print(f"Generating image for prompt: '{prompt}'")
    image = pipe(prompt).images[0]

    # Save the image
    image.save(output_path)
    print(f"Image saved to {output_path}")

if __name__ == "__main__":
    user_prompt = input("Enter a description for the image: ")
    generate_image(user_prompt)
