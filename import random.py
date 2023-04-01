import pyspark, random
from pyspark.sql import SparkSession
import os
import sys


os.environ['PYSPARK_DRIVER_PYTHON_OPTS']= "notebook"
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable
os.environ['PYSPARK_PYTHON'] = sys.executable


sc = pyspark.SparkContext()

# def inside(p):
#     x, y = random.random(), random.random()
#     return x * x + y * y < 1


# NUM_SAMPLES = 10 ** 7
# count = sc.parallelize(range(NUM_SAMPLES)).filter(inside).count()
# approx_pi = (4.0 * count / NUM_SAMPLES)
# print(f"Pi is roughly {approx_pi}")


