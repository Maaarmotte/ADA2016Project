# This code is used to aggregate the sentiments found in the twitter data. The 'source_location'
# and 'sentiment' colums are extracted from the data. To simplify counting, a column of 1s is
# added. Then, the data are grouped by (source_location, sentiment) and the sum is computed for
# each of these groups. The results are exported to CSV files (one per month per language).

import os
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.functions import lit
from py4j.protocol import Py4JJavaError

# Input files
base_path = 'hdfs:///datasets/goodcitylife/{}/harvest3r_twitter_data_{}-{}_0.json'

# Where to store the data. It's better to store the results in Hadoop file system. But
# since the output is really small (a few megabytes at most), we can directly write
# to the main node file system
output_path = '/home/lhabegge/processed'

# The name for the CSV (1st argument is language, second is month)
output_file = 'tweets_sentiments_given_{}_{}.csv'

# Couldn't find a better way to check if a file exists in the hadoop file system
def path_exists(path):
    try:
        rdd = sc.textFile(path)
        rdd.take(1)
        return True
    except Py4JJavaError as e:
        return False

# Parse a whole month of data, day by day
def parse_month(month_txt, month_nb, language, extract_path, extract_cols):
    df_month = None
    
    for i in range(31):
        day = str(i+1).zfill(2)       # Pad with zero
        file_path = base_path.format(month_txt, day, month_nb)
        
        #if os.path.isfile(file_path):
        if path_exists(file_path):
            print('Parsing {}...'.format(file_path))
            
            data = sqlContext.read.json(file_path).select(extract_path)
            data = data.filter(data.lang == language).select(extract_cols)
                        
            if not df_month:
                df_month = data
            else:
                df_month = df_month.unionAll(data)
    
    # Regroup the data locally and save to txt file
    if df_month:
        final = df_month.withColumn('count', lit(1)).groupBy(extract_cols).sum().map(toCSV).collect()
        output = '{}/{}'.format(output_path, output_file.format(language, month_txt))
        save(final, output)

# Convert a row of data to a CSV string. Escapes the \ and " characters. Couldn't find
# a better way to do this for Spark 1.6. Should be rewritten to avoid code duplication.
def toCSV(row):
    return ','.join('"' + elem.replace("\\", "\\\\").replace('"', '\\"') + '"' if isinstance(elem, str) else '"' + str(elem).replace("\\", "\\\\").replace('"', '\\"') + '"' for elem in row)

# Write a list of strings into a file
def save(lst, filename):
    f = open(filename, 'w')
    for line in lst:
        f.write("{}\n".format(line))
    f.close()

# Create a new context if none exists
try:
    sc = SparkContext()
except:
    print('sc already exists')
    
sqlContext = SQLContext(sc)

# Extract aggregated sentiments from january to may
languages = ['en', 'fr', 'de']
path = ['_source.source_location', '_source.sentiment', '_source.lang']
cols = ['source_location', 'sentiment']
months = [('january', '01'),
          ('february', '02'),
          ('march', '03'),
          ('april', '04'),
          ('may', '05'),
          ('june', '06'),
          ('july', '07'),
          ('august', '08'),
          ('september', '09'),
          ('october', '10')]

# Extract
for language in languages:
    for tup in months:
        parse_month(tup[0], tup[1], language, path, cols)
        