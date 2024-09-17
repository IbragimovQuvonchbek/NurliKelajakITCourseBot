import aiohttp


async def get_student_info(params):
    url = f"http://13.60.228.133/api/v1/courseit/results/?ids={params}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()