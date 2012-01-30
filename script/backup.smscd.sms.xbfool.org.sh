p=`date +%Y-%m-%d-%T`
p1=/home/xbfool/backup/smsd-$p.sql
p2=/home/xbfool/backup/smsd-$p.sql.tar.gz
mysqldump -u root -pftp3*8*ing --opt -e smsd > $p1
tar -cvzf $p2 $p1
rm $p1

p=`ls -t1 /home/xbfool/backup/*`
index=10#0
for i in $p
do
  let "index = index + 1"
  if (($index > 10))
  then
    echo "deleting $i"
    rm $i
  fi
done
