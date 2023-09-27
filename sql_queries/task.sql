select area
from cell_tower
where mcc = 250
      and radio != 'LTE'
group by area
having count(id) > 2000