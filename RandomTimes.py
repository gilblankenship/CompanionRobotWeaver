import random
import math

def generate_random_normal_distribution_float_number(min_value, max_value, var):
  normal_distribution = random.normalvariate(0, var)
  random_number = min_value + normal_distribution
  while random_number > max_value:
    normal_distribution = random.normalvariate(0, 0.01)
    random_number = min_value + normal_distribution
  return random_number

random_number = generate_random_normal_distribution_float_number(0, 11,5)
print(format(random_number, f'.{2}f'))
