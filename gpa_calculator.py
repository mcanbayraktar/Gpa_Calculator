
import re, sys


courses, repeat_courses, credits, sum_grades = {}, [], 0, 0

anyNew = raw_input("Var mi eklemek istedigin ders?(Y|N)")	# due to python2, I used raw_input method (in python3: input() is OK)
if anyNew is "Y" or anyNew is "y":
	print("--------------------------------------------------------------------")
	print("Sana zahmet su formatta girsene derslerini:")
	print("Dept&Code    Grade    Credit    (Repeat ya da Withdraw durumu varsa:    R(W)    Dept&Code)")
	print("ex: CMPEXXX AA 3 ")
	print("ex: CMPEXXX AA 3 R CMPEXXX")
	print("Bi de isin bitince  N ya da n gir de hesapliyim GPA'ini")
	print("--------------------------------------------------------------------")
	newCourse = raw_input("")
	with open(sys.argv[1], "r+") as f:
		while newCourse:
			f.write(newCourse + "\n")
			newCourse = raw_input("")
			if newCourse is "N" or newCourse is "n":
				f.close()

with open(sys.argv[1]) as f:
	for line in f:
		# Returns course name without section using regex
		reg_ID = re.match(r"\A\D{3,4}\d{3}", line)
		if not reg_ID:
			continue
		ID = reg_ID.group()
		reg_grade = re.search(r"\s((AA)|(BA)|(BB)|(CB)|(CC)|(DC)|(DD)|(P)|(F)|(W))\s", line)
		grade = reg_grade.group(1)
		reg_credit = re.search(r"\s((1)|(2)|(3)|(4))\s", line)
		credit = reg_credit.group(1)
		reg_repeat = re.search(r"\s(R)\s*(\D{3,4}\d{3})", line)
		if reg_repeat:
			repeat_course = reg_repeat.group(2)
			if grade != "F" and ID != repeat_course:
				repeat_courses.append(repeat_course)
		if ID not in courses.keys() and ID not in repeat_courses:
			courses[ID] = (grade, credit)
	for i in sorted(courses.keys()):
		if int(courses[i][1]) != 1:
			credits += int(courses[i][1])
		coef = 0.00
		if courses[i][0] == "AA": coef = 4.00
		if courses[i][0] == "BA": coef = 3.50
		if courses[i][0] == "BB": coef = 3.00
		if courses[i][0] == "CB": coef = 2.50
		if courses[i][0] == "CC": coef = 2.00
		if courses[i][0] == "DC": coef = 1.50
		if courses[i][0] == "DD": coef = 1.00
		sum_grades += int(courses[i][1]) * coef
		if courses[i][0] != "F":
			print("Completed: " + str(i))
		else:
			print("Repeat: " + str(i))
	print("Overall Points:" + str(sum_grades))
	print("Overall Attempted: " + str(credits))
	GPA = float(sum_grades) / float(credits)
	print(GPA)
