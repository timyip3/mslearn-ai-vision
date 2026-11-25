import os
import json

# Add references
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI
import requests
import base64

def main(): 

    # Clear the console
    #os.system('cls' if os.name=='nt' else 'clear')
        
    try: 
    
        # Get configuration settings 
        load_dotenv()
        endpoint = os.getenv("ENDPOINT")
        model_deployment =  os.getenv("MODEL_DEPLOYMENT")

        
        # Initialize the client
        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(), 
            "https://cognitiveservices.azure.com/.default"
        )

        token = token_provider()
        
        url = f"{endpoint}/providers/blackforestlabs/v1/flux-2-flex?api-version=preview"

         
        img_no = 0
        # Loop until the user types 'quit'
        while True:
            # Get input text
            input_text = input("Enter the prompt (or type 'quit' to exit): ")
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a prompt.")
                continue

            payload = {
                        "model": model_deployment,
                        "prompt": input_text,
                        "width": 1024,
                        "height": 1024,
                        "output_format": "jpeg",
                        "num_images": 1,
                    }
            response = requests.post(
                url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}",
                },
                json=payload
            )

            response.raise_for_status()

            json_response = response.json()
            image_data = json_response["data"][0].get("b64_json")
            image_data_in_bytes = base64.b64decode(image_data)

            # save the image
            img_no += 1
            file_name = f"image_{img_no}.png"
            save_image(image_data_in_bytes, file_name)


    except Exception as ex:
        print(f"Error: {ex}")

def save_image (image_data, file_name):
    # Set the directory for the stored image
    image_dir = os.path.join(os.getcwd(), 'images')

    # If the directory doesn't exist, create it
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)

    # Initialize the image path (note the filetype should be png)
    image_path = os.path.join(image_dir, file_name)

    # Save the generated image
    with open(image_path, "wb") as image_file:
        image_file.write(image_data)
    print (f"Image saved as {image_path}")


if __name__ == '__main__': 
    main()