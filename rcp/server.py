import os
import base64
from PIL import Image
from together import Together
import imageio
import urllib.parse
import trimesh
import open3d as o3d
from flask import Flask, request, jsonify
from flask_cors import CORS

from trellis.pipelines import TrellisTextTo3DPipeline, TrellisImageTo3DPipeline
from trellis.utils import postprocessing_utils

print("Creating model!")
#pipeline = TrellisTextTo3DPipeline.from_pretrained("larsquaedvlieg/TRELLIS-text-large-fork")
#pipeline.cuda()
#pipeline_img = TrellisImageTo3DPipeline.from_pretrained("larsquaedvlieg/TRELLIS-image-large-fork")
#pipeline_img.cuda()


app = Flask(__name__)
CORS(app)
client = Together()

glb_cache = "cache/temp.glb"
ply_cache = "cache/temp.ply"
png_cache = "cache/temp.png"


def txt2img(prompt: str) -> Image:
    response = client.images.generate(
        prompt=prompt,
        model="black-forest-labs/FLUX.1-schnell-Free",
        width=512,
        height=512,
        steps=1,
        n=1,
        response_format="b64_json",
        stop=[]
    )
    b64_image = response.data[0].b64_json
    with open(png_cache, "wb") as f:
        f.write(base64.b64decode(b64_image))
    return Image.open(png_cache)


def refine(txt: str, img: Image):
    img.save(png_cache)
    img_url = urllib.parse.urljoin("file:", urllib.request.pathname2url(str(png_cache)))
    imageCompletion = client.images.generate(
        model="black-forest-labs/FLUX.1-depth",
        width=1024,
        height=768,
        steps=28,
        prompt="show me this picture as a superhero",
        image_url=img_url,
        response_format="b64_json",
    )
    b64_image = response.data[0].b64_json
    with open(png_cache, "wb") as f:
        f.write(base64.b64decode(b64_image))
    return Image.open(png_cache)


def rm(path: str):
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
    if len(data.get("images", list())) > 0:
        print("Generating from", len(data["images"]), "images!")
        imgs = []
        for encoded_img in data["images"]:
            with open(png_cache, "wb+") as f:
                f.write(base64.b64decode(encoded_img))
            imgs.append(Image.open(png_cache))
        if data.get("prompt", None) is not None:
            prompt = data["prompt"]
            print("Refining images with prompt:", prompt)
            imgs = [refine(prompt, imgs[0])]
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
            imgs = None
        else:
            print("Getting image from prompt!")
            imgs = [txt2img(prompt)]
            output = pipeline.run(imgs, seed=1234)

    ret = {"imgs": []}
    if imgs is not None:
        ret["imgs"] = []
        for img in imgs:
            img.save(png_cache)
            with open(f, "rb") as f:
                ret["imgs"].append(base64.b64encode(f.read()).decode("utf-8"))

    glb = postprocessing_utils.to_glb(output["gaussian"][0], output["mesh"][0],
                                      simplify=0.95, texture_size=1024)
    glb.export(glb_cache)
    with open(glb_cache, "rb") as f:
        glb = f.read()
    ret["glb"] = base64.b64encode(glb).decode("utf-8")
    print("Done, returning")
    print()
    return ret


if __name__ == "__main__":
    print("Listening!")
    app.run(host="0.0.0.0", port=8080)
