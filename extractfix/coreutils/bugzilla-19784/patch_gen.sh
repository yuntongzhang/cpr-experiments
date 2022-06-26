project_name=coreutils
bug_id=bugzilla-19784
dir_name=$1/extractfix/$project_name/$bug_id

project_url=https://github.com/coreutils/coreutils.git
commit_id=658529a

current_dir=$PWD
mkdir -p $dir_name
cd $dir_name
git clone $project_url src
cd src
git checkout $commit_id

fix_file=src/make-prime-list.c
backup_file=backup.c

sed -i '214,215d' src/make-prime-list.c
sed -i '214i while((p == limit) && sieve[++i] == 0)' src/make-prime-list.c

diff -u $backup_file $fix_file > $2/$bug_id/cpr.patch
