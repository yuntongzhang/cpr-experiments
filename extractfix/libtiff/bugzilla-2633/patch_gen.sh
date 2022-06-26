project_name=libtiff
bug_id=bugzilla-2633
dir_name=$1/extractfix/$project_name/$bug_id
project_url=https://github.com/vadz/libtiff.git
commit_id=f3069a5


current_dir=$PWD
mkdir -p $dir_name
cd $dir_name
git clone $project_url src
cd src
git checkout $commit_id

fix_file=tools/tiff2ps.c
backup_file=backup.c

sed -i '2441i if(h == 1) return;' tools/tiff2ps.c

diff -u $backup_file $fix_file > $2/$bug_id/cpr.patch
