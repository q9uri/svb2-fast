import torch

model_root = "pretrain_new"
step = 127000

g_model = torch.load(f"{model_root}/G_{step}.pth", map_location="cpu")
d_model = torch.load(f"{model_root}/D_{step}.pth", map_location="cpu")

g_dict = {}
for key in g_model["model"].keys():
    if key.startswith("emb_g"):
        print(key)
    else:
        g_dict[key] = g_model["model"][key]

d_dict = {}
for key in d_model["model"].keys():
    d_dict[key] = d_model["model"][key]

from safetensors.torch import save_file


save_file(g_dict, f"G_0.safetensors")
save_file (d_dict, f"D_0.safetensors")
