
# read all files
from pathlib import Path
import os.path, time
import tarfile


import exifread


file_bins = {}

p = Path(Path.cwd())

for i, child in enumerate(p.glob('**/../../Pictures/*')):
    if child.is_file() and not child.name.endswith('.xmp'):
        with open(child, 'rb') as fh:
            #print(child)
            tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal")
            try:
                dateTaken = tags["EXIF DateTimeOriginal"]
                #import pdb; pdb.set_trace()
                year = dateTaken.values.split(":")[0]
                month = dateTaken.values.split(":")[1]
                yearmonth = '{}-{}'.format(year, month)
            except KeyError:
                # NO EXIF
                yearmonth = 'NODATA'
        #when = os.stat(child).st_ctime
        #year = time.ctime(when).split()[-1]
        #month = time.ctime(when).split()[1]
        #yearmonth = '{}-{}'.format(year, month)
        if yearmonth in file_bins:
            file_bins[yearmonth].append(child)
        else:
            file_bins[yearmonth] = [child]


# Make tar
for key in file_bins:
    tar = tarfile.open(key+'.tar', "w")
    for item in file_bins[key]:
        tar.add(item)
    tar.close()

print([len(file_bins[x]) for x in file_bins])
print(i)


export AWS_ACCESS_KEY=AKIAVAJ6QXZZ5RPI4EMH
export AWS_SECRET_KEY=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
export AWS_DEFAULT_REGION=us-east-1
