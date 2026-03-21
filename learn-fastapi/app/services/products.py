import json
from pathlib import Path
from typing import List,Dict
import aiofiles

DATAFILE = Path("..","data","products.json")

async def load_products() -> List[Dict]:
    """Load products from the JSON data file."""
    async with aiofiles.open(DATAFILE, "r", encoding="utf-8") as file:
        content = await file.read()
        products = json.loads(content)
    return products



