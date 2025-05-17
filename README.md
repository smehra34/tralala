# RCP (Remote Control Protocol) - 3D Model Generation and Refinement

A powerful system for generating and refining 3D models using text prompts and images, built with Python and Flask.

## Overview

RCP is a server-client application that leverages advanced AI models to generate and refine 3D models. It supports:
- Text-to-3D model generation
- Image-to-3D model generation
- 3D model refinement using text prompts
- Image refinement using text prompts

## Features

- **Text-to-3D Generation**: Convert text descriptions into 3D models
- **Image-to-3D Generation**: Transform 2D images into 3D models
- **Model Refinement**: Refine existing 3D models using text prompts
- **Image Refinement**: Enhance images using text prompts
- **Web Interface**: User-friendly web interface for model manipulation
- **GLB Support**: Full support for GLB file format (binary glTF)
- **Real-time Preview**: Interactive 3D model preview with camera controls

## Prerequisites

- Python 3.x
- CUDA-capable GPU
- Required Python packages:
  - Flask
  - Flask-CORS
  - PIL (Pillow)
  - Together AI client
  - Trimesh
  - Open3D
  - NumPy
  - Trellis pipelines

## Installation

1. Clone the repository
2. Install required packages:
```bash
pip install flask flask-cors pillow together trimesh open3d numpy
```

3. Install Trellis pipelines:
```bash
pip install trellis-pipelines
```

## Usage

### Server

Start the server:
```bash
python server.py
```
The server will run on `http://localhost:8080`

### Client

Run the client:
```bash
python client.py
```

The client provides an interactive command-line interface where you can:
- Input image paths
- Provide text prompts
- Specify GLB files for refinement
- Generate and save 3D models

### Web Interface

The web interface provides a more user-friendly way to interact with the system:
1. Open `index.html` in a web browser
2. Use the interface to:
   - Upload base GLB models
   - Add images
   - Enter text prompts
   - Generate and refine 3D models
   - Download generated models

## API Endpoints

### POST /generate

Generates or refines 3D models based on input data.

Request body:
```json
{
    "prompt": "string",  // Optional text prompt
    "images": ["base64_string"],  // Optional array of base64-encoded images
    "glb": "base64_string"  // Optional base64-encoded GLB file
}
```

Response:
```json
{
    "glb": "base64_string",  // Generated/refined GLB file
    "image": "base64_string"  // Optional generated image
}
```

## Models Used

- TRELLIS text-to-3D pipeline
- TRELLIS image-to-3D pipeline
- FLUX.1-schnell-Free for image generation
- FLUX.1-depth for image refinement

## License

[Specify your license here]

## Contributing

[Add contribution guidelines if applicable] 