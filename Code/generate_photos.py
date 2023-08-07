# Load libraries
from diffusers import DiffusionPipeline, StableDiffusionPipeline
import torch
import pandas as pd
import os


# Load profiles
profiles = pd.read_json('./Data/profils.json')
profiles = pd.concat([profiles.drop(['profils'], axis=1), profiles['profils'].apply(pd.Series)], axis=1)


# Load Model
pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0",
                                         torch_dtype=torch.float16,
                                         use_safetensors=True,
                                         variant="fp16")
pipe.enable_model_cpu_offload()

# pipe = StableDiffusionPipeline.from_pretrained("dreamlike-art/dreamlike-photoreal-2.0",
#                                                 torch_dtype=torch.float16)
# pipe.enable_model_cpu_offload()


# Prepare seed
seed = torch.Generator()

# Fix negative prompt
neg_prompt = "(deformed iris, deformed pupils, multiple, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime:1.4), text, cropped, out of frame, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck"

# Create dir for images if not exist
os.makedirs('./Data/Images/', mode=0o777, exist_ok=True)


# Loop over profiles
for ind in profiles.index:
    
    # Create dir  for images profile if not exist
    os.makedirs(f"./Data/Images/{profiles.loc[ind,'nom']}_{profiles.loc[ind,'age']}", mode=0o777, exist_ok=True)
    
    # Fix seed with age
    seed.manual_seed(int(profiles.loc[ind,'age']*profiles.loc[ind,'taille']*profiles.loc[ind,'poids']))
    
    # List 4 differents prompt
    prompt1 = f"""Une photo debout face caméra de {profiles.loc[ind,'nom']}, bel homme bien habillé de {profiles.loc[ind,'age']} ans.
    Il est d'origine {profiles.loc[ind,'nationalite']} avec la peau {profiles.loc[ind,'peau']}.
    Ses cheveux sont {profiles.loc[ind,'cheveux']}, il a les yeux {profiles.loc[ind,'yeux']}.
    (high detailed skin:1.2), 8k uhd, dslr, soft lighting, high quality"""
    
    prompt2 = f"""Une photo de vacance de {profiles.loc[ind,'nom']}, bel homme de {profiles.loc[ind,'age']} ans.
    Il est d'origine {profiles.loc[ind,'nationalite']} avec la peau {profiles.loc[ind,'peau']}.
    Ses cheveux sont {profiles.loc[ind,'cheveux']}, il a les yeux {profiles.loc[ind,'yeux']}.
    (high detailed skin:1.2), 8k uhd, dslr, soft lighting, high quality"""
    
    prompt3 = f"""Un selfie de {profiles.loc[ind,'nom']}, bel homme de {profiles.loc[ind,'age']} ans.
    Il est d'origine {profiles.loc[ind,'nationalite']} avec la peau {profiles.loc[ind,'peau']}.
    Ses cheveux sont {profiles.loc[ind,'cheveux']}, il a les yeux {profiles.loc[ind,'yeux']}.
    (high detailed skin:1.2), 8k uhd, dslr, soft lighting, high quality"""
    
    prompt4 = f"""Une photo de {profiles.loc[ind,'nom']} pratiquant du {profiles.loc[ind,'sport']}, bel homme de {profiles.loc[ind,'age']} ans.
    Il est d'origine {profiles.loc[ind,'nationalite']}, peau {profiles.loc[ind,'peau']}.
    Ses cheveux sont {profiles.loc[ind,'cheveux']}, il a les yeux {profiles.loc[ind,'yeux']}.
    (high detailed skin:1.2), 8k uhd, dslr, soft lighting, high quality"""
    
    prompts = [prompt1, prompt2, prompt3, prompt4]
    
    # Generate 4 images
    for ind_prompt, prompt in enumerate(prompts):
        
        if os.path.exists(f"./Data/Images/{profiles.loc[ind,'nom']}_{profiles.loc[ind,'age']}/photo_{ind_prompt}.png"):
            continue
        
        print(f"Generating image {ind_prompt} for {profiles.loc[ind,'nom']} {profiles.loc[ind,'age']} y.o, waiting....")

    
        images = pipe(prompt=prompt,
                      num_images_per_prompt=1,
                      negative_prompt=neg_prompt,
                      generator=seed,
                      ).images
        images[0].save(f"./Data/Images/{profiles.loc[ind,'nom']}_{profiles.loc[ind,'age']}/photo_{ind_prompt}.png")












