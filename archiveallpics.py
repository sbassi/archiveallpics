
# read all files
from pathlib import Path
import os.path, time
import tarfile


import exifread

INPUT_DIR = '**/../../../Documents/vikifotos/*'
#INPUT_DIR = '/Users/t_basss/Documents/vikifotos/*'

file_bins = {}

p = Path(Path.cwd())

# '**/../../Pictures/*'

for i, child in enumerate(p.glob(INPUT_DIR)):
    if child.is_file() and not child.name.endswith('.xmp'):
        with open(child, 'rb') as fh:
            tags = exifread.process_file(fh, stop_tag="EXIF DateTimeOriginal")
            try:
                dateTaken = tags["EXIF DateTimeOriginal"]
                year = dateTaken.values.split(":")[0]
                month = dateTaken.values.split(":")[1]
                yearmonth = '{}-{}'.format(year, month)
            except KeyError:
                # NO EXIF
                yearmonth = 'NODATA'
                # USE VALUES IN FS get year/month
                date_taken = os.path.getmtime(child)
                yearmonth = time.strftime('%Y-%m', time.localtime(date_taken))
        if yearmonth in file_bins:
            file_bins[yearmonth].append(child)
        else:
            file_bins[yearmonth] = [child]

# Make tar
for key in file_bins:
    tar = tarfile.open(key + '.tar', "w")
    for item in file_bins[key]:
        tar.add(item.resolve())
    tar.close()

print([len(file_bins[x]) for x in file_bins])
print(i)


#export AWS_ACCESS_KEY=
#export AWS_SECRET_KEY=
#export AWS_DEFAULT_REGION=us-east-1
