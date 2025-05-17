import base64

import imageio
from flask import Flask, request, jsonify

from trellis.pipelines import TrellisTextTo3DPipeline
from trellis.utils import postprocessing_utils

print("Creating model!")
pipeline = TrellisTextTo3DPipeline.from_pretrained("larsquaedvlieg/TRELLIS-text-large-fork")
pipeline.cuda()
app = Flask(__name__)
glb_cache = "cache/temp.glb"


@app.route("/generate", methods=["POST"])
def count_characters():
    data = request.get_json()
    assert "prompt" in data
    prompt = data["prompt"]
    print("Prompt requested:", prompt)
    output = pipeline.run(prompt, seed=1234)
    glb = postprocessing_utils.to_glb(output["gaussian"][0], output["mesh"][0],
                                      simplify=0.95, texture_size=1024)
    glb.export(glb_cache)
    with open(glb, "rb") as f:
        glb = f.read()
    return {"glb": base64.b64encode(glb).decode("utf-8")}



if __name__ == "__main__":
    print("Listening!")
    app.run(host="0.0.0.0", port=8080)
