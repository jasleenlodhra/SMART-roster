update nurses
set current_shift=1
where (nurses.group_num=2 or nurses.group_num=4) AND nurses.id <> 0;