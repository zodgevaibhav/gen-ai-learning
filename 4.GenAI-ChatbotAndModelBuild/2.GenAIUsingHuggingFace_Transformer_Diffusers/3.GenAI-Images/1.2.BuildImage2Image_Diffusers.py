import torch
from diffusers import StableDiffusionImg2ImgPipeline
from PIL import Image

# Load the pre-trained Stable Diffusion Img2Img pipeline
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16
)
pipe = pipe.to("mps")  # use GPU if available

# Load your input image
init_image = Image.open("image.png").convert("RGB")
init_image = init_image.resize((512, 512))  # Stable Diffusion expects 512x512

# Define prompt
prompt = "A fantasy castle at sunset, digital art, highly detailed"

# Run the pipeline
images = pipe(
    prompt=prompt,
    image=init_image,
    strength=0.75,    # how much to transform the init image (0 = preserve, 1 = ignore)
    guidance_scale=7.5, # how strongly the text prompt influences result
    num_inference_steps=50
).images

# Save result
images[0].save("result.png")
