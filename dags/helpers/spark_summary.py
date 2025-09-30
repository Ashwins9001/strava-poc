from pyspark.sql import SparkSession
import sys

if __name__ == "__main__":
    input_path = sys.argv[1]

    spark = SparkSession.builder \
        .appName("StravaActivitiesJob") \
        .getOrCreate()

    # Read JSON file into DataFrame
    df = spark.read.json(input_path)

    print(input_path)

    print("✅ Loaded Strava activities:")
    df.show(10, False)

    spark.stop()