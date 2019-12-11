import subprocess
file_in  = '../data/states.csv'
file_out = '../data/station-coords/num-by-state.csv'
search   = '../data/station-coords/allgas-geocode-success.csv'
st8z = [x.strip() for x in open(file_in, 'r').readlines()]
with open(file_out, 'w') as fout:
   for st8 in st8z:
      num = subprocess.check_output(f'grep -n "{st8}" {search} | wc -l', shell=True)
      fout.write(f"{st8},{int(num.strip())}\n")
