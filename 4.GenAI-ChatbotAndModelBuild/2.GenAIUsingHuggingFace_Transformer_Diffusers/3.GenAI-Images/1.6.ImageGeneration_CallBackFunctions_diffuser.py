import torch

from diffusers import DPMSolverMultistepScheduler, StableDiffusionXLPipeline
from diffusers.callbacks import SDXLCFGCutoffCallback


callback = SDXLCFGCutoffCallback(cutoff_step_ratio=0.4)
# can also be used with cutoff_step_index
# callback = SDXLCFGCutoffCallback(cutoff_step_ratio=None, cutoff_step_index=10)

pipeline = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    variant="fp16",
).to("mps")
pipeline.scheduler = DPMSolverMultistepScheduler.from_config(pipeline.scheduler.config, use_karras_sigmas=True)

prompt = "a buffalo on the road, best quality, high quality, high detail, 8k resolution"

generator = torch.Generator(device="mps").manual_seed(2628670641)

out = pipeline(
    prompt=prompt,
    negative_prompt="",
    guidance_scale=6.5,
    num_inference_steps=25,
    generator=generator,
    callback_on_step_end=callback,
)

out.images[0].save("official_callback.png")