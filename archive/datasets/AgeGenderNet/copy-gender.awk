{
	if(NR > 1) {
		if($6 == "f") {
			fem = sprintf("aligned/%s/landmark_aligned_face.%s.%s",$1,$3,$2)
			female[fem] = fem
		} else if ($6 == "m") {
			mal = sprintf("aligned/%s/landmark_aligned_face.%s.%s",$1,$3,$2)
			male[mal] = mal
		}
	}
}

END{
	females = length(female)
	males = length(male)
	print "We found ", females, " females and ", males, " males"
	copycmd = "cp "
	for ( i in female) {
		system(copycmd sprintf("%s ",female[i]) " f/")
	}

	for ( i in male	) {
                system(copycmd sprintf("%s ",male[i]) " m/")
	}
}
