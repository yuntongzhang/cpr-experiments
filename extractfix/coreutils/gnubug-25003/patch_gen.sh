project_name=coreutils
bug_id=gnubug-25003
dir_name=$1/extractfix/$project_name/$bug_id

project_url=https://github.com/coreutils/coreutils.git
commit_id=68c5eec


current_dir=$PWD
mkdir -p $dir_name
cd $dir_name
git clone $project_url src
cd src
git checkout $commit_id

fix_file=src/split.c
backup_file=backup.c

cp $fix_file $backup_file

sed -i '985d' src/split.c
sed -i '985i if(10 <= k)' src/split.c

diff -u $backup_file $fix_file > $2/$bug_id/cpr.patch
