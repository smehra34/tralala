import base64
import requests


def main():
    cache_path = "cache/temp.glb"
    done = False
    while not done:
        try:
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
            print("Writing result in", path)
            with open(cache_path, "wb+") as f:
                f.write(glb)
        except KeyboardInterrupt:
            done = True

if __name__ == "__main__":
    main()

