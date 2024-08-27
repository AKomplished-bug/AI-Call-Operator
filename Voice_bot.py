import asyncio
import os
from hume import HumeVoiceClient, MicrophoneInterface
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

async def main() -> None:
    # Retrieve the Hume API key from the environment variables
    HUME_API_KEY = os.getenv("HUME_API_KEY")
    print(f"HUME_API_KEY: {HUME_API_KEY}")  # Add this line after loading the environment variable

    if not HUME_API_KEY:
        raise ValueError("HUME_API_KEY not found in environment variables.")

    # Connect and authenticate with Hume
    client = HumeVoiceClient(HUME_API_KEY)

    # Establish a connection with EVI using your configuration
    async with client.connect(config_id="e684a326-836e-48c5-8a24-b091051a0114") as socket:
        await MicrophoneInterface.start(socket)

# Run the async main function
asyncio.run(main())
