from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, hour, lag, to_date, avg
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType
from pyspark.sql.window import Window
import logging
import os

# -----------------------------
# ENV SETUP (MUST BE FIRST)
# -----------------------------
os.environ["HADOOP_HOME"] = "C:\\hadoop"
os.environ["PYSPARK_PYTHON"] = r"D:\MarketMaven\venv\Scripts\python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = r"D:\MarketMaven\venv\Scripts\python.exe"

logging.basicConfig(level=logging.INFO)


def run_spark_job():

    logging.info("Starting Spark session...")

    # -----------------------------
    # SPARK SESSION (NO SparkConf)
    # -----------------------------
    spark = SparkSession.builder \
        .appName("MarketMavenSpark") \
        .config("spark.jars.packages",
                "org.apache.hadoop:hadoop-aws:3.3.4,com.amazonaws:aws-java-sdk-bundle:1.12.262") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.hadoop.fs.s3a.endpoint", "s3.ap-south-1.amazonaws.com") \
        .config("spark.hadoop.fs.s3a.region", "ap-south-1") \
        .getOrCreate()

    # -----------------------------
    # CRITICAL FIX: FORCE HADOOP CONFIG IMMEDIATELY
    # -----------------------------
    hadoop_conf = spark.sparkContext._jsc.hadoopConfiguration()

    # overwrite EVERYTHING related to timeout
    for k in list(hadoop_conf):
        if "timeout" in k or "attempts" in k:
            hadoop_conf.set(k, "60000")

    hadoop_conf.set("fs.s3a.connection.timeout", "60000")
    hadoop_conf.set("fs.s3a.socket.timeout", "60000")
    hadoop_conf.set("fs.s3a.attempts.maximum", "3")

    # -----------------------------
    # SCHEMA
    # -----------------------------
    schema = StructType([
        StructField("symbol", StringType(), True),
        StructField("price", DoubleType(), True),
        StructField("volume", IntegerType(), True),
        StructField("timestamp", StringType(), True)
    ])

    # -----------------------------
    # LOAD DATA
    # -----------------------------
    logging.info("Loading raw data...")
    df = spark.read.schema(schema).json("data/raw/market_events.json")

    # -----------------------------
    # CLEANING
    # -----------------------------
    df = df.filter(col("price") > 0)

    # -----------------------------
    # TRANSFORM
    # -----------------------------
    df = df.withColumn("timestamp", to_timestamp(col("timestamp")))

    df = df.withColumn("hour", hour(col("timestamp"))) \
           .withColumn("date", to_date(col("timestamp")))

    window_spec = Window.partitionBy("symbol").orderBy("timestamp")

    df = df.withColumn(
        "price_change",
        col("price") - lag("price").over(window_spec)
    )

    # -----------------------------
    # WRITE TO S3
    # -----------------------------
    logging.info("Writing processed data to S3...")

    df.write \
        .mode("overwrite") \
        .partitionBy("symbol", "date") \
        .parquet("s3a://marketmaven-data-abhas/market_data/")

    # -----------------------------
    # SQL LAYER
    # -----------------------------
    df.createOrReplaceTempView("market")

    result = spark.sql("""
        SELECT symbol,
               AVG(price) as avg_price,
               AVG(volume) as avg_volume
        FROM market
        GROUP BY symbol
    """)

    result.show()

    spark.stop()
    logging.info("Spark job completed!")


if __name__ == "__main__":
    run_spark_job()