from pyspark.sql import SparkSession

# instantiate session
spark = SparkSession.builder.appName(" BigData : read SQL ").getOrCreate()

# path to the desired ressource's file system
parquet_path_1 = "hdfs://localhost:9000/bigdata.parquet"
parquet_path_2 = "hdfs://localhost:9000/est_fr.parquet"

# read those
data_1 = spark.read.parquet(parquet_path_1)
data_2 = spark.read.parquet(parquet_path_2)

# SPARK SQL : data as table
data_1.createOrReplaceTempView("translations_1")
data_2.createOrReplaceTempView("translations_2")

result = spark.sql("""
                    WITH translations as (
                    SELECT *
                    FROM translations_1 t1 
                    UNION ALL
                    SELECT * 
                    FROM translations_2 t2) 
                   
                    SELECT * 
                    FROM translations 
                    WHERE source='estonian'
                    """)

result.coalesce(1).write.save("#",format="csv")