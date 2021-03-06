import os
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.functions import lit
from pyspark.sql.functions import col
from py4j.protocol import Py4JJavaError

sources_attributes = {'twitter': ['source_location', 'lang', 'main', 'sentiment'],
                      'instagram': ['lang', 'main', 'sentiment', 'tags'], 
                      'news': ['lang', 'title', 'extract', 'sentiment', 'tags']}

base_path = 'hdfs:///datasets/goodcitylife/{month}/harvest3r_{source}_data_{day_num}-{month_num}_{part}.json'
output_path = '/home/lhabegge/processed'
output_file = '{source}_non-en_msg_{month}.csv'

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

def parse_month(source, month_txt, month_num, ignore_language=None):
    df_month = None
    
    for i in range(31):
        for part in range(2):
            day = str(i+1).zfill(2)       # Pad with zero
            file_path = base_path.format(source=source, month=month_txt, day_num=day, month_num=month_num, part=part)

            if path_exists(file_path):
                print('Parsing {}...'.format(file_path))
                
                attributes = sources_attributes[source]
                data = sqlContext.read.json(file_path).select(['_source.' + attr for attr in attributes])
                
                if ignore_language:
                    data = data.filter(data.lang != ignore_language).select(attributes)
                else:
                    data = data.select(attributes)
                            
                if not df_month:
                    df_month = data
                else:
                    df_month = df_month.unionAll(data)
    
    # Regroup the data locally and save to txt file
    if df_month:
        final = df_month.map(toCSV).collect()
        output = os.path.join(output_path, output_file.format(source=source, month=month_txt))
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
for month, month_num in months:
    for source in sources_attributes.keys():
        #parse_month(source, month, month_num, ignore_language='en')
        parse_month(source, month, month_num)
    