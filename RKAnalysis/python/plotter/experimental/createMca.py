from os import walk
import argparse


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("-p","--paths", dest="paths", nargs='+', type=str, help="paths of files")
  parser.add_argument("-o","--outputName", dest="output", default="testmca", type=str, help="output txt name (dont put .txt exists)")

  args = parser.parse_args()
  lines=""
  for path in args.paths:
    for (dirpath, dirnames, filenames) in walk(path):
       for fl in dirnames:
         lines+=dirpath+"/"+fl+"/*.root\n"

  with open(args.output+".txt","w") as out:
    out.write(lines)
  out.close()
    
   
