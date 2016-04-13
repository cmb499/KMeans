#import necessary libraries
import sys   
import csv
import random

##stdin processing
k_num_centroid = int(sys.argv[1])

max_iter_allowed = int(sys.argv[3])

##Reading the data from the input file

data = []
for line in open(sys.argv[2]):
    items = line.rstrip('\r\n').split('\t')   # strip new-line characters and split on column delimiter
    items = [float(item.strip()) for item in items]  # strip extra whitespace off data items
    data.append(items)
    
##find the number of columns as conditions or dimensions in the input data. The code works for any number of columns in input data
number_of_dimensions=len(items)


##Reading the centroid data if available
if len(sys.argv)>=5:   ##if centroid data file was input as the 5th argument in stdin
    centroid = []
    for line in open(sys.argv[4]):
        items = line.rstrip('\r\n').split('\t')   # strip new-line characters and split on column delimiter
        items = [float(item.strip()) for item in items]  # strip extra whitespace off data items
        centroid.append(items)
    

    

else:    #else generate the nondeterministric random centroid points within range
    centroid = []     ##initialize the overall centroid list
    temp_centroid=[]   ##initialize the individual centroid list that will make the overall l
    max =0.0
    min=0.0
    #for zz in xrange (k_num_centroid):
    for zz in xrange (k_num_centroid):
        for xx in xrange(number_of_dimensions):
               
               for yy in xrange(len(data)):

                  if data[yy][xx]>max:      ## find min and max of the range in every dimension or column
                     max = data[yy][xx]
                  if data[yy][xx]<min:
                     min = data[yy][xx]
                

               rand = random.random()       ##generation of the centroids are based on random number and not deterministic
               value= min+ rand*(max-min)   ##make sure that the centroids are within the range of input data for every dimension or columns.
                                            ##It is minimum plus a random number times the range i.e max-min
          
               temp_centroid.append(value)  ## build up the centroids
        centroid.append(temp_centroid)      
        temp_centroid=[]                     ##initialize the single centroid list to make sure next centroid list can be built
           
      
##This module calculates the euclidian distance between an observation and a given centroid. The input is data_num index from data list and centroid_num index from centroid list
##It returns the euclidian distance between an observation and a given centroid

def dist_from_centroid(data_num, centroid_num):
    euclid_distance_squared=0
    for aa in xrange (number_of_dimensions):
        euclid_distance_squared= euclid_distance_squared + (data[data_num][aa]- centroid[centroid_num][aa])**2
        
    euclid_distance = euclid_distance_squared**0.5
     
    return euclid_distance

##Build a list with data_point_num, first_dimension_value(for recognition),distance from the nearest ventroid and that centroid index corresponding to the  centroid list
data_point_list=[]
data_point_list_previous=[]    ##data_point_list_previous will store the previous data points configuration to check if it got assigned to a new centroid
new_centroid=centroid       ##do not touch the original centroid.  Work on new and previous centroid list
previous_centroid=new_centroid

knearest_iterations_count =0     ##index to keep track of number of iterations needed


##Now we start the algorithm. We do the iterations based on the stdin input or when the convergence is reached i.e points do not move to other centroid on an iteration
##For an iteration we first assign the points to the nearest centroids
##We then average data in every column or dimensions to find the new centroid.
##With the new centroid we do the next iteration.
##The process is iterated till convergence is reached or a max number of interation as specified is achieved.

for knearest_iterations in xrange(max_iter_allowed):
    flag =0     ##flag tocheck if any points moved to onther centroid with a new iteration
    
    
    previous_centroid=new_centroid
    
    for jj in xrange (len(data)):
        dist_centroid=0
        min_dist_centroid=10**155    ##we set a min centroid distance to a high number
        centroid_num=0              ##record the index of the minimum dist centroid
        
        #distance from centroids
        for zz in xrange (k_num_centroid):
            dist_centroid = dist_from_centroid(jj,zz)     ##call the dist_from_centroid module to find the euclidian distance between an observation and a centroid
            
            if dist_centroid <min_dist_centroid:      ##find the minimum distance cetroid
                min_dist_centroid=dist_centroid
                centroid_num = zz                     ##record the index of the minimum dist centroid
        
  
        data_point_list.append([jj, data[jj][0],min_dist_centroid, centroid_num])  ## build up the data point list with new centroid information
    
    if knearest_iterations!=0:       ##check to see if any points changed centroid assignment
        
        
        for check_data_cen_change_cnt in xrange(len(data_point_list)):    ##check every data if it changed centroid from the previous pass
            
            
            if data_point_list_previous[check_data_cen_change_cnt][3] != data_point_list[check_data_cen_change_cnt][3]:
                flag =1
                
    
    if knearest_iterations!=0:         ##if data pts did not change centroid then flag to stop iteration
        if flag==0:
            break
  
    previous_centroid=new_centroid     ## Now if more iterations are needed save the new centroid list info in another list
    
    data_point_list_previous=data_point_list     ## Now if more iterations are needed save the current data point list info in another list
    
    
    for new_centroids in xrange(k_num_centroid):                ## do this for all centroids
        for dimensions_in_centroid in xrange(number_of_dimensions):         ##    do this for all data columns or dimensions
            dimensional_total=0       ##    initialize the variables for finding new centroids based on dimensional data of the indidual points assigned to it
            average_dimension=0
            number_of_data_in_centroid =0
            for observations_in_data_point_list in xrange(len(data_point_list)):
                if data_point_list[observations_in_data_point_list][3]== new_centroids:
                    
                    number_of_data_in_centroid = number_of_data_in_centroid +1
                    dimensional_total = dimensional_total + data[observations_in_data_point_list][dimensions_in_centroid]
                    
            
            if number_of_data_in_centroid !=0:           ##special treatment if the centroid has zero data to avoid division by zero
                average_dimension = float(dimensional_total)/float(number_of_data_in_centroid)       ## calculate average for centroids per column or dimensions
                
                
                new_centroid[new_centroids][dimensions_in_centroid] = average_dimension   ##generate the new centroids
            else:
                new_centroid[new_centroids][dimensions_in_centroid] = centroid[new_centroids][dimensions_in_centroid]        #keep the cetroid data same if no points are there in the cluster of that centroid
            
    
    data_point_list=[]        ## now once the new centroids are built, initialize the data point list sothat the data points can be reassigned to new centroids

    knearest_iterations_count = knearest_iterations_count+1     ##at thge end of the iteration, increase the iteration counetr so that it can be reported via stdout
  

f = open('outOur.txt','a')  
f.write("Number of iterations : %d\n" %knearest_iterations_count)   

for observations_new in xrange(len(data_point_list)):
    f.write("%d\t"%data_point_list[observations_new][0])
    f.write("%f\t"%data_point_list[observations_new][1])
    f.write("%f\t"%data_point_list[observations_new][2])
    f.write("%d\n"%data_point_list[observations_new][3])

f.close()

