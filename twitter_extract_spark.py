import os
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.functions import lit

language = 'en'
extract_path = ['_source.source_location', '_source.sentiment', '_source.lang']
extract_cols = ['source_location', 'sentiment']
#base_path = '/home/marmotte/data/ADA2016Project/data/{}/harvest3r_twitter_data_{}-{}_0.json'
#output_path = '/home/marmotte/data/ADA2016Project/processed'
base_path = 'hdfs:///datasets/goodcitylife/{}/harvest3r_twitter_data_{}-{}_0.json'
output_path = '/home/lhabegge'
output_file = 'tweets_en_{}.csv'
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

def parse_month(month_txt, month_nb):
    df_month = None
    
    for i in range(31):
        day = str(i+1).zfill(2)       # Pad with zero
        file_path = base_path.format(month_txt, day, month_nb)
        
        if os.path.isfile(file_path):
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
        output = '{}/{}'.format(output_path, output_file.format(month_txt))
        save(final, output)
        
def toCSV(row):
    return ','.join(elem.encode('utf-8') if type(elem) == unicode else str(elem) for elem in row)

def save(lst, filename):
    f = open(filename, 'w')
    for line in lst:
        f.write("{}\n".format(line))
    f.close()

if not sc:
    sc = SparkContext()
    
sqlContext = SQLContext(sc)

# Extract everything !
for tup in months:
    parse_month(tup[0], tup[1])
    