from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import sys
import os
import json

def get_stats(df, type_):
    df = df.where(df.sport_type == type_)
    df.createOrReplaceTempView(type_)
    df = spark.sql("""
            SELECT AVG(average_speed) as average_speed, SUM(moving_time) as total_moving_time, MAX(max_speed) as max_speed, SUM(distance) as total_distance, COUNT(DISTINCT(start_date)) as days_doing_activity, COUNT(athlete) as number_of_activities
            from {0}
        """.format(type_))
    df = df.withColumn('activity_type', F.lit(type_))
    return df.first().asDict()

if __name__ == "__main__":
    input_path = sys.argv[1]

    spark = SparkSession.builder \
        .appName("StravaActivitiesJob") \
        .getOrCreate()

    df = spark.read.json(input_path)
    
    runs = get_stats(df, 'Run')
    rides = get_stats(df, 'Ride')
    
    spark.stop()

    output = {"runs": runs, "rides": rides}

    output_path = os.path.dirname(input_path)

    with open(os.path.join(output_path, "aggregated_activities.json"), "w") as f:
        json.dump(output, f)