import asyncio
from hume import HumeVoiceClient, MicrophoneInterface

async def main() -> None:
  # Paste your Hume API key here
  HUME_API_KEY = "HUME_API_KEY"
  # Connect and authenticate with Hume
  client = HumeVoiceClient(HUME_API_KEY)

  # Start streaming EVI over your device's microphone and speakers
  async with client.connect(config_id="config-id") as socket:
      await MicrophoneInterface.start(socket)
asyncio.run(main())
