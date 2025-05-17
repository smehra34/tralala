import base64
import requests


def main():
    path = "cache/temp.glb"
    done = False
    while not done:
        try:
            response = requests.post("http://localhost:8080/generate", json={"prompt": input("Prompt: ")})
            assert response.ok
            response = response.json()
            glb = base64.b64decode(response["glb"])
            print("Writing result in", path)
            with open(path, "wb+") as f:
                f.write(glb)
        except KeyboardInterrupt:
            done = True

if __name__ == "__main__":
    main()

