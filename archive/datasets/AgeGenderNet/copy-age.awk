{
	if(NR > 1) {
 		if($4 ~ /\(/) {
			lower = $4
			upper = $5
			sub(/\(/,"",lower)
			sub(/,/,"",lower)
			sub(/\)/,"",upper)
		
			copycmd = "cp "
			system(copycmd sprintf("aligned/%s/landmark_aligned_face.%s.%s %s-%s/",$1,$3,$2,lower,upper))

			bin = sprintf("%s-%s",lower,upper)
			if(bin in counts) {
				counts[bin]++
			} else {
				counts[bin] = 1
			}
		}
	}
}

END{
#	females = length(female)
#	males = length(male)
	print "We found the following categories:"
	for (bin in counts) {
		print bin, counts[bin]
	}
#	copycmd = "cp "
#	for ( i in female) {
#		system(copycmd sprintf("%s ",female[i]) " f/")
#	}
#
#	for ( i in male	) {
#		system(copycmd sprintf("%s ",male[i]) " m/")
#	}
}
