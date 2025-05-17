import os
import base64
import requests

# models/gltf/croco.glb
# /home/alehc/Downloads/NationalGeographic_2572187_16x9.jpeg

def rm(path):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass



def main():
    cache_path = "cache/temp.glb"
    output_path = "cache/out.glb"
    done = False
    while not done:
        try:
            rm(cache_path)
            rm(output_path)
            kind = input("Prompt kind? (img/text): ")
            if kind == "img":
                img_paths = input("Comma-separated paths of the images: ").split(",")
                data = {"images": []}
                for path in img_paths:
                    with open(path, "rb") as f:
                        b = f.read()
                    data["images"].append(base64.b64encode(b).decode("utf-8"))
            else:
                assert kind == "text"
                prompt = input("Prompt: ")
                path = input("Path to glb (optional): ")
                data = {"prompt": prompt}
                if path != "":
                    with open(path, "rb") as f:
                        glb = f.read()
                    data["glb"] = base64.b64encode(glb).decode("utf-8")

            response = requests.post("http://localhost:8080/generate", json=data)
            assert response.ok
            response = response.json()
            glb = base64.b64decode(response["glb"])
            print("Writing result in", output_path)
            with open(output_path, "wb+") as f:
                f.write(glb)
        except KeyboardInterrupt:
            done = True

if __name__ == "__main__":
    main()

