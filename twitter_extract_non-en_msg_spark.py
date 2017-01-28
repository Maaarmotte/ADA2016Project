import os
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.functions import lit
from pyspark.sql.functions import col
from py4j.protocol import Py4JJavaError

language = 'en'  # Don't extract this language
extract_path = ['_source.source_location', '_source.main', '_source.sentiment', '_source.lang']
extract_cols = ['source_location', 'lang', 'main', 'sentiment']
#base_path = '/home/marmotte/data/ADA2016Project/data/{}/harvest3r_twitter_data_{}-{}_0.json'
#output_path = '/home/marmotte/data/ADA2016Project/processed'
#output_file = 'tweets_non-en_msg_{}.csv'
#months = [('april', '04')]

base_path = 'hdfs:///datasets/goodcitylife/{}/harvest3r_twitter_data_{}-{}_0.json'
output_path = '/home/lhabegge/processed'
output_file = 'tweets_non-en_msg_{}.csv'
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

def path_exists(path):
    try:
        rdd = sc.textFile(path)
        rdd.take(1)
        return True
    except Py4JJavaError as e:
        return False

def parse_month(month_txt, month_nb):
    df_month = None
    
    for i in range(31):
        day = str(i+1).zfill(2)       # Pad with zero
        file_path = base_path.format(month_txt, day, month_nb)
        
        #if os.path.isfile(file_path):
        if path_exists(file_path):
            print('Parsing {}...'.format(file_path))
            
            data = sqlContext.read.json(file_path).select(extract_path)
            data = data.filter(data.lang != language).select(extract_cols)
            
            # To filter by regexp
            #data = sqlContext.read.json(file_path).select(extract_path)
            #data = data.filter(data.lang != language)
            #data = data.filter(col("main").rlike(regexp)).select(extract_cols)
                        
            if not df_month:
                df_month = data
            else:
                df_month = df_month.unionAll(data)
    
    # Regroup the data locally and save to txt file
    if df_month:
        final = df_month.map(toCSV).collect()
        output = '{}/{}'.format(output_path, output_file.format(month_txt))
        save(final, output)
        
def toCSV(row):
    return ','.join('"' + elem.replace("\\", "\\\\").replace('"', '\\"') + '"' if isinstance(elem, str) else '"' + str(elem).replace("\\", "\\\\").replace('"', '\\"') + '"' for elem in row)

def save(lst, filename):
    f = open(filename, 'w')
    for line in lst:
        f.write("{}\n".format(line))
    f.close()

try:
    sc = SparkContext()
except:
    print('sc already exists')
    
sqlContext = SQLContext(sc)

# Extract everything !
for tup in months:
    parse_month(tup[0], tup[1])
    