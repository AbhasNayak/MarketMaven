from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[*]") \
    .appName("MarketMaven-Test") \
    .getOrCreate()

print("✅ Spark Session Created")

spark.range(5).show()

spark.stop()