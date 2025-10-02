import torch
from diffusers import DiffusionPipeline

pipe_sd = DiffusionPipeline.from_pretrained("emilianJR/CyberRealistic_V3", torch_dtype=torch.float16)
pipe_sd.to("mps")
# load long prompt weighting pipeline
pipe_lpw = DiffusionPipeline.from_pipe(
    pipe_sd,
    custom_pipeline="lpw_stable_diffusion",
).to("mps")

prompt = ", hiding in the leaves, ((rain)), zazie rainyday, beautiful eyes, macro shot, colorful details, natural lighting, amazing composition, subsurface scattering, amazing textures, filmic, soft light, ultra-detailed eyes, intricate details, detailed texture, light source contrast, dramatic shadows, cinematic light, depth of field, film grain, noise, dark background, hyperrealistic dslr film still, dim volumetric cinematic lighting"
neg_prompt = "(deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime, mutated hands and fingers:1.4), (deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, disconnected limbs, mutation, mutated, ugly, disgusting, amputation"
generator = torch.Generator(device="mps").manual_seed(20)
out_lpw = pipe_lpw(
    prompt,
    negative_prompt=neg_prompt,
    width=512,
    height=512,
    max_embeddings_multiples=3,
    num_inference_steps=50,
    generator=generator,
    ).images[0]

out_lpw.show()