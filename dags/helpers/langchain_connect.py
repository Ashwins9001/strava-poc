from langchain.llms import OpenAI
import os
from langchain.tools import tool
from langchain_openai import OpenAI
from openai import OpenAI as OpenAIClient
from dotenv import load_dotenv


def setup():
    load_dotenv()
    env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
    OPEN_API_KEY = os.getenv("OPEN_API_KEY")
    return OPEN_API_KEY

def run_langchain(**kwargs):
    open_api_key = setup()
    ti = kwargs["ti"] 

    runs = ti.xcom_pull(task_ids="push_stats_xcom", key="runs")
    rides = ti.xcom_pull(task_ids="push_stats_xcom", key="rides")

    client = OpenAIClient(api_key=open_api_key)

    # Generate an image
    response = client.images.generate(
        model="dall-e-3",  
        prompt="""Create a Strava wrapped similar to a spotify wrapped for the following user: Ashwin, given the following data: {0} for runs, and {1} for rides. 
        Make sure to include the name of the user on the illustration and clearly list out some interesting statistics, it should be legible.
        Actually make sure all text is written in English words and can be read.
        I also want all the stats that are provided by the runs data to be shown as is in running information.
        I want all the stats that are provided by the rdes data to be shown as is in cycling information.
        I want this to be a pretty infographic that shows the data as-is as a yearly summary of what this athlete has done so far.
        Their name (Ashwin) should be clearly included in the infographic and if there's any graphs or visuals they should clearly appear with the axes labelled and numbers shown for exact reference.
        You can spend extra time generating the image I need it to be clear, readable, and summarize all provided information from the past year for this athlete.
        The total_moving_time is in seconds, average_speed and max_speed is in kilometers-per-hour, and total_distance is in meters, show these stats in those units and label them.""".format(runs, rides),
        size="1024x1024",
        quality="standard",
        n=1
    )

    image_url = response.data[0].url
    print("Generated image URL:", image_url)