
data=$(cat db.csv | cut -d';' -f1,2,6)

dir=inputs
rm -rf $dir
mkdir $dir

echo "$data" | while read line 
do

    IFS=';'
    read -a arr <<<"$line" 

    number=${arr[0]}
    name=$(echo "${arr[1]}" | tr ' ' '_')
    json=${arr[2]}

    echo processing $number $name

    js=$dir/$name.json
    echo "$json" | python -m json.tool --no-ensure-ascii > $js

    #
    # remove empty graphs
    #
    if [ -n "$(cat $js | grep analyses | grep -o '{}')" ]
    then
        rm $js
    fi

done
