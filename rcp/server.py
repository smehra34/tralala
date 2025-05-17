import os
import base64
from PIL import Image
import imageio
import trimesh
import open3d as o3d
from flask import Flask, request, jsonify
from flask_cors import CORS

from trellis.pipelines import TrellisTextTo3DPipeline, TrellisImageTo3DPipeline
from trellis.utils import postprocessing_utils

print("Creating model!")
pipeline = TrellisTextTo3DPipeline.from_pretrained("larsquaedvlieg/TRELLIS-text-large-fork")
pipeline.cuda()
pipeline_img = TrellisImageTo3DPipeline.from_pretrained("larsquaedvlieg/TRELLIS-image-large-fork")
pipeline_img.cuda()
app = Flask(__name__)
CORS(app)
glb_cache = "cache/temp.glb"
ply_cache = "cache/temp.ply"
png_cache = "cache/temp.png"


def rm(path):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


@app.route("/generate", methods=["POST"])
def count_characters():
    rm(glb_cache)
    rm(ply_cache)
    rm(png_cache)

    data = request.get_json()
    if data.get("images", None) is not None:
        print("Generating from images!")
        imgs = []
        for encoded_img in data["images"]:
            with open(png_cache, "wb+") as f:
                f.write(base64.b64decode(encoded_img))
            imgs.append(Image.open(png_cache))
        output = pipeline_img.run_multi_image(imgs, seed=1234)
    else:
        assert "prompt" in data
        prompt = data["prompt"]
        print("Generating with prompt:", prompt)
        if data.get("glb") is not None:
            print("Refining from glb!")
            glb = data["glb"]
            glb = base64.b64decode(data["glb"])
            with open(glb_cache, "wb+") as f:
                f.write(glb)
            mesh = trimesh.load(glb_cache)
            mesh.export(ply_cache)
            mesh = o3d.io.read_triangle_mesh(ply_cache)
            output = pipeline.run_variant(mesh, prompt, seed=1234)
        else:
            output = pipeline.run(prompt, seed=1234)

    glb = postprocessing_utils.to_glb(output["gaussian"][0], output["mesh"][0],
                                      simplify=0.95, texture_size=1024)
    glb.export(glb_cache)
    with open(glb_cache, "rb") as f:
        glb = f.read()
    return {"glb": base64.b64encode(glb).decode("utf-8")}



if __name__ == "__main__":
    print("Listening!")
    app.run(host="0.0.0.0", port=8080)
