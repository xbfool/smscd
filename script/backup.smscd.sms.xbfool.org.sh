p=`date +%Y-%m-%d-%T`
p1=~/home/xbfool/backup/smsd-$p.sql
p2=~/home/xbfool/backup/smsd-$p.sql.tar.gz
mysqldump -u root -pftp3*8*ing --opt -e smsd > $p1
tar -cvzf $p2 $p1
rm $p1
