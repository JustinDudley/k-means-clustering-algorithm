import math
import random
import matplotlib.pyplot as plt
import csv	# For working CSV files in python, there is an inbuilt module called csv

# data1953.csv    lines 2-197
# data2008.csv    lines 2-197
# dataBoth.csv	  lines 2-393



def welcome():	# Welcome note to user
	print("This program reads from a file which contains health data from 196 countries. " 
	+ "\nEach country's birth rate and life expectancy is mapped on an xy-plane, and "
	+ "\na surprisingly straightforward iterative algorithm is performed which divides "
	+ "\nthe data handily into clusters.")

def choose_file():	# User chooses between the 3 files
	file_num = int(input("\nWhich file would you like to examine?  Enter 1,2, or 3: \n1  1953 statistics \n2  2008 statistics \n3  1953 + 2008 statistics \n\n"))
	print("")
	if file_num == 1:
		filename = "data1953.csv"
		filelength = 196
	elif file_num == 2:
		filename = "data2008.csv"
		filelength = 196
	elif file_num == 3:
		filename = "dataBoth.csv"
		filelength = 392
	return filename

def get_num_foci():	# retrieve user choice of number of clusters/foci
	return int(input("Alright, how many clusters would you like the data divided into? (must be "
	+"\nless than 196.  4 or 5 works nicely... "))
	
def get_num_iter():	# retrieve from user the number of times to iterate the algorithm
	message = int(input("\n...and finally, how many times would you like the algorithm to repeat (iterate)? "
	+ "\nIt doesn't take more than 2 or 3 iterations to settle into its final state, but you can "
	+ "\nchoose as many as you like: "))
	print("")
	return message


# read file to list
def read_csv(filename):
	with open(filename, 'r') as csvfile:
		data = csv.reader(csvfile)
		
		nation_data = []
		nation_coors = []
		for row in data:
			nation_data.append(row) 
		return nation_data[1:]	# eliminate top row of field strings

# take full list of all file data, convert all numbers to type float
def cast_to_double(full_data):
	name_and_doub = []
	for item in full_data:
		name_and_doub.append([ item[0], float(item[1]), float(item[2]) ])
	return name_and_doub # return original list, but with numbers converted from string to float
		
# take full list of all file data, convert all numbers to type float AND remove the country strings to each item in list, so only numbers remain
def extract_coord(full_data):
	coord = []
	for item in full_data:
		coord.append([ float(item[1]), float(item[2]) ])
	return(coord)	# return a list of coordinates.  No country name attached.  data type float.  
		

# SHOW GRAPH TO USER
def draw_graph(cluster_list):
	counter = 0
	for i in range(len(cluster_list)):
		X = []
		Y = []
		for j in range(len(cluster_list[i])):		#eg. 6 coordinates --> i = 0,1,2,3,4,5    --- the first cluster---  (then the 2nd,...)
			X.append(cluster_list[i][j][1])		# Append one integer.  The 3rd bracket is 1 because after country name at index 0, the x-coordinate comes next (index 1) in the x-y pair.
			Y.append(cluster_list[i][j][2])		# Append one integer. The 3rd bracket is 2 because after country name at index 0, the y-coordinate comes at index 2 in the x-y pair.
	
		col_list = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']	# colors
		color = col_list[counter % 8]	# 8 colors.  After they're used up, they will cycle again from the beginning, thanks to %
		plt.scatter(X, Y, c = color)	# create scatterplot
		counter +=1
		
	plt.show()	#display plot to user


# Show data to user
def show_data(all_data, clusters):
	print("\n\n")
	print("HIT <ENTER> AT THE BOTTOM TO SEE A GRAPHICAL REPRESENTATION OF YOUR CLUSTERS.")
	
	# print info:  Cluster No., the countries in the cluster, avg birth, avg life expectancy
	for i in range(len(clusters)):		# == for i in range(k)
	#so, first i == 0...
		
		print("\nCluster No. " + str(i + 1) + ": ")
		for item in clusters[i]:
			print(item[0], end = ", ")
		print("")
		
		print("Average birth rate for this cluster", end = ": ")
		sumbirth = 0
		for item in clusters[i]:
			sumbirth += item[1]
		print(sumbirth / len(clusters[i]))
		
		print("Average life expectancy for this cluster", end = ": ")
		sumlife = 0
		for item in clusters[i]:
			sumlife += item[2]
		print(sumlife / len(clusters[i]))
	
	# Ask user to hit <ENTER> to see graph	
	input("\nThe graph that follows is primitive, but it's still pretty interesting.  And don't forget to try running "
	+ "\nthe program again with different cluster and iteration choices.  Thank you for using this program today. "
	+ " \n\n    HIT <ENTER> TO SEE THIS INFORMATION GRAPHED.  ")


def sum_the_squares(clusters, foci):
	sum_sq = 0
	for clus in clusters:		# eg. clus[0]
		
		
		
		for n in clus:
			for foc in foci:
				dist = math.pow( math.pow(n[2] - foc[1], 2)  +   math.pow(n[1] - foc[0], 2),  0.5)	#Euclidean/Pythagorean distance formula
				sum_sq += math.pow(dist, 2)
	return sum_sq


# THIS FUNCTION CALCULATES THE CLUSTERS, DETERMINES THE NEXT SET OF FOCI,
# AND CALLS THE TWO FUNCTIONS THAT DISPLAY INFO AND GRAPH INFO
def calc_foci(nation_doubles, foci, iter_num, count):
	# in this function, the k foci are identified by their position in the list "foci".  So, there is focus 0 at index 0, focus 1 at index 1, etc.
	
	clusters = []
	for item in foci:
		clusters.append([])		# eg. clusters now contains 3 (k) empty lists.
	
	# for item in foci:	# eg. 3 iterations, if number of foci = 3 (k)
	for n in nation_doubles:	# (for each country in the list)
		n_coord = [n[1], n[2]]	# extract just the coordinates from n, remove the country name.  Makes the distance formula a little prettier
		dist_list = []	# a list of numbers.  It has k distances (floats) from a single given coordinate n to each of the k focus points
		for foc in foci:
			dist = math.pow( math.pow(n_coord[1] - foc[1], 2)  +   math.pow(n_coord[0] - foc[0], 2),  0.5)	#Euclidean/Pythagorean distance formula
			dist_list.append(dist)

		nearest_foc = dist_list.index(min(dist_list))	# returns INDEX of min element of dist_list, which gives the identity of a focus (the nearest 
														# focus to n), since dist_list was created by looping through the k foci one by one.
		clusters[nearest_foc].append(n)	# add the coordinate n to the appropriate element of clusters list.  Clusters is a list with k sublists. Each
										# sublist is a collection of the coordinates closest to a particular focus. The first sublist, at index 0, is 
										# the collection of coordinates closest to the focus with index 0, the second, at index 1, ...1, and so on...
	
	
	# (sum of squares:  Is this "R^2"?  Research this later)
	sum_of_squares = sum_the_squares(clusters, foci)
	print(str(sum_of_squares), end = ", ")
	
	
	# CALL FUNCTIONS TO SHOW DATA TO USER
	# AND GRAPH DATA FOR USER
	if count == iter_num:	# can use >=  instead of == just in case user enters 0 for iter_num
		show_data(nation_doubles, clusters)	# CALL A FUNTION *HERE* TO PRESENT DATA TO USER.  HAVE THEM PRESS ENTER TO SEE THE GRAPH
		draw_graph(clusters)	# Draw graph for user
		return foci	# acts like a break
	
	# now, look at each cluster in clusters, and calculate the mean coordinate of that cluster.  These means ARE the next set of foci
	foci.clear()	#deletes all elements of foci list
	for clus in clusters:
		sum_x = 0	# initialize
		sum_y = 0	# initialize
		for coor in clus:
			sum_x += coor[1]	# loop through clus, get sum of all x-coordinates
			sum_y += coor[2]	# loop through clus, get sum of all y-coordinates
		mean_x = sum_x / len(clus)
		mean_y = sum_y / len(clus)
		new_foc = [mean_x, mean_y]
		foci.append([mean_x, mean_y])	# each clus in clusters appends its mean coordinate to the foci list
	
	return foci		# at this point, the foci don't relate to any one country, so I think it's okay to have abandoned country names




# If in future I want to identiry the countries associated with these first random points, I'll need to pass more than just coordinates into this function.
#get/return k random foci from the list of all data.
def get_rand_foci(coors_all, k):	
	# STEP 1: generate a list of k random, distinct integers
	indnum = 0	# for ease of coding, index 0 is always included in the first round of clustering 
	indlist = [indnum]	#initialize list
	for i in range(k-1):	# indnum already includes one element, so we need k-1 more 
		while indnum in indlist:
			indnum = random.randint(0,len(coors_all) - 1) # generate one random integer, continue while-loop until indnum is new and distinct
		indlist.append(indnum)
		indnum = 0

	# STEP 2: generate foci_list.  The elements of foci_list are chosen randomly from elements of coors_all, using the random numbers of indlist
	foci_list = []
	for num in indlist:
		foci_list.append(coors_all[num])
	return foci_list
	

# PROGRAM BEGINS HERE
welcome()
filename = choose_file()

nation_data = read_csv(filename)	# this function eliminates the top row of column headers
nation_doubles = cast_to_double(nation_data)	# numbers cast to double
coord_data = extract_coord(nation_data)			# numbers cast to double, nation names removed leaving coordinates only

num_foci = get_num_foci()	# request number of clusters from user
num_iter = get_num_iter()	# request number of iterations from user
foci = get_rand_foci(coord_data, num_foci)	# First foci list created at random.  

print(" [[  Programmer's note to self:  The progression of the sum of squares should converge when calculated on each iteration:   ]]")

# THIS FUNCTION DOES THE HEAVY LIFTING.  CLUSTERS CALCULATED, NEW FOCI LIST CREATED.
counter = 1
for i in range(num_iter):	# if set to num_iter + 1, can enter a zero() for num_iter, and actually see what happens at low levels of iteration
	foci = calc_foci(nation_doubles, foci, num_iter, counter)	# foci list updated using Euclidean distance algorithms
	counter +=1

'''
In future, show the user what happens at low levels of iteration.  The thing is, they have to be REALLY low to be obvious.  
Ideally, there would be a split screen to show the first 4 iterations. 
'''
