from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, hour, avg
import logging

logging.basicConfig(level=logging.INFO)

def run_spark_job():
    logging.info("Starting Spark session...")

    spark = SparkSession.builder \
        .appName("MarketMavenSpark") \
        .getOrCreate()

    # Load raw data
    logging.info("Loading raw data...")
    df = spark.read.json("data/raw/market_events.json")

    # Convert timestamp
    df = df.withColumn("timestamp", to_timestamp(col("timestamp")))

    # Basic cleaning
    df = df.filter(col("price") > 0)

    # Feature engineering
    df = df.withColumn("hour", hour(col("timestamp")))

    # Aggregation example
    agg_df = df.groupBy("symbol").agg(
        avg("price").alias("avg_price"),
        avg("volume").alias("avg_volume")
    )

    logging.info("Showing aggregated data:")
    agg_df.show()

    # Save output
    agg_df.write.mode("overwrite").csv("data/processed/spark_output", header=True)

    logging.info("Spark job completed!")

    spark.stop()


if __name__ == "__main__":
    run_spark_job()
