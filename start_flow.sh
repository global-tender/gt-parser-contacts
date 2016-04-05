#!/bin/bash


# region_id=('3' '4')
# fz=('fz223' 'fz94')
# sorting=('PO_NAZVANIYU' 'PO_RELEVANTNOSTI')
# sortDirection=('true' 'false')
# custLev=('F' 'S' 'M' 'NOT_FSM')

region_id=('1')
fz=('fz223')
sorting=('PO_NAZVANIYU')
sortDirection=('true')
custLev=('F')

for region_id_item in "${region_id[@]}"
do
	for fz_item in "${fz[@]}"
	do
		for sorting_item in "${sorting[@]}"
		do
			for sortDirection_item in "${sortDirection[@]}"
			do
				for custLev_item in "${custLev[@]}"
				do
					python manage.py flow $region_id_item $fz_item $sorting_item $sortDirection_item $custLev_item
				done
			done
		done
	done
done