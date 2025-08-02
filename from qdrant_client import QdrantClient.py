from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

load_dotenv()

print(os.getenv("QDRANT_HOST"))
print(os.getenv("QDRANT_API_KEY"))

qdrant_client = QdrantClient(
        url=os.getenv("QDRANT_HOST"),
       api_key=os.getenv("QDRANT_API_KEY")
)

print(qdrant_client.get_collections())