project_name=libtiff
bug_id=bugzilla-2611
dir_name=$1/extractfix/$project_name/$bug_id
project_url=https://github.com/vadz/libtiff.git
commit_id=9a72a69

current_dir=$PWD
mkdir -p $dir_name
cd $dir_name
git clone $project_url src
cd src
git checkout $commit_id

fix_file=libtiff/tif_ojpeg.c
backup_file=backup.c

cp $fix_file $backup_file

sed -i '816i if(sp->bytes_per_line == 0) return -1;\n' libtiff/tif_ojpeg.c

diff -u $backup_file $fix_file > $2/$bug_id/cpr.patch
