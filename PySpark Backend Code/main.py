from pyspark.sql import SparkSession
from pyspark.sql.functions import col

#create source path to read data from aws s3 bucket
S3_DATA_SOURCE_PATH = 's3://aws-db-2023/data-source/Combined_Flights_2018.csv'
#create output path to add output in aws s3 bucket
S3_DATA_OUTPUT_PATH = 's3://aws-db-2023/data-output'

#create main fuction to run the spark job on the EMR cluster
def main():
    #To run the spark job, create app name and include it into the EMR cluster.
    spark = SparkSession.builder.appName('JinmeisterDemoApp').getOrCreate()
    #To read the data from the aws s3 bucket.
    all_data = spark.read.csv(S3_DATA_SOURCE_PATH, header=True)
    #To give the name of the table
    all_data.createOrReplaceTempView("flights_dataset")
    #To write the three SQL query which will give the output on the aws s3 bucket.
    departuredelay_data =spark.sql("""SELECT Airline,Origin,Dest,DepDelayMinutes FROM flights_dataset WHERE DepDelayMinutes >= 60 AND Airline = 'American Airlines Inc.' LIMIT 100""")
    dest_origin = spark.sql("""SELECT Airline,Origin,Dest,AirTime FROM flights_dataset WHERE Origin = 'LAX' AND Dest = 'EWR' ORDER BY Airline DESC LIMIT 100""")
    top_airtime = spark.sql("""SELECT Airline,AirTime,Flight_Number_Operating_Airline FROM flights_dataset WHERE AirTime >=100  LIMIT 100""")
    #To witre the sql query output into the aws s3 bucket.
    departuredelay_data.write.option("header", "true").mode('overwrite').csv(S3_DATA_OUTPUT_PATH)
    dest_origin.write.option("header", "true").mode("append").csv(S3_DATA_OUTPUT_PATH)
    top_airtime.write.option("header", "true").mode("append").csv(S3_DATA_OUTPUT_PATH)
    
                                   

#function called
if __name__ == '__main__':
    main()