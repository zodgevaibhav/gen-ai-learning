import torch
from diffusers import StableDiffusionPipeline

# Set device
device = "cuda" if torch.cuda.is_available() else "mps"
torch.manual_seed(0) # Control the randomness

# Load model
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", 
    torch_dtype=torch.float16
).to(device)

# Prompt
prompt = "Astronauts on the horse"

# Generate image
image = pipe(prompt).images[0]

# Display (if in Jupyter)
image.show()
