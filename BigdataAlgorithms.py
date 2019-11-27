import sys
import time
from rtree import index

def SequentialSearch(dataset,queryDataPoints):
    """
    This function takes two arguments dataset; and query data points read from the file provided by the function 
    and sequentially parses the dataset for each query data point to compute the intersecting points. It then 
    finally writes the output in the SequentialSearchResult.txt file.
    """
    datasetSize = int(dataset[0])
    numberOfQueries= int(len(queryDataPoints))-1

    counter =0
    sequentialScanResult = list()

    totalThen = time.time()

    for i in range(0,numberOfQueries):
        for j in range(1,datasetSize):
            if int(queryDataPoints[i].split()[0]) <= int(dataset[j].split()[1]) and int(queryDataPoints[i].split()[1]) >= int(dataset[j].split()[1])  and int(queryDataPoints[i].split()[2]) <= int(dataset[j].split()[2]) and int(queryDataPoints[i].split()[3]) >= int(dataset[j].split()[2]) :
                counter+=1
        sequentialScanResult.append(counter)
        counter=0
    totalNow = time.time()
    averageQueryTime=(totalNow-totalThen)/100
    print("Total running time taken by sequential scan algorithm for 100 queries:",totalNow-totalThen,"seconds")
    print("Average running time taken by each sequential query:",averageQueryTime,"seconds\n")

    #writing the output to the file
    with open('SequentialSearchResult.txt', 'w+') as outputFile:
        for item in sequentialScanResult:
            outputFile.write(str(item))
            outputFile.write('\n')

    return averageQueryTime


def RTreeImplementation(dataset,queryDataPoints):
    """
    This function takes two arguments dataset; and query data points read from the file provided by the function 
    and uses the Rtree library to compute the intersecting points.
    It then finally writes the output in the RTreeResult.txt
    """
    datasetSize = int(dataset[0])
    numberOfQueries= int(len(queryDataPoints))-1

    RTreeScanResult = list()

    idx2d = index.Index()

    Totalthen = time.time()

    print("Building R tree...")

    #using the insert function to add points in the bounding box from the given dataset
    for i in range(1,datasetSize):
        temp = dataset[i].split()
        idx2d.insert(i,(int(temp[1]),int(temp[2])))
        
    queryThen = time.time()

    #using the intersection function to compute all points lying for each query window in the queryDataPoints list 
    for i in range(0,numberOfQueries):
        RTreeScanResult.append(len(list(idx2d.intersection((int(queryDataPoints[i].split()[0]),int(queryDataPoints[i].split()[2]),int(queryDataPoints[i].split()[1]),int(queryDataPoints[i].split()[3]))))))
        
    queryNow= time.time()
    toalNow = time.time()
    averageQueryTime = (queryNow-queryThen)/numberOfQueries
    print("Total running time taken by R tree scan algorithm for 100 queries:",queryNow-queryThen,"seconds")
    print("Average running time taken by each query using R-tree scan:",averageQueryTime,"seconds")

    #writing the output to the file
    with open('RTreeResult.txt', 'w+') as outputFile:
        for item in RTreeScanResult:
            outputFile.write(str(item))
            outputFile.write('\n')

    return averageQueryTime

def main():
    """
        This function accepts the dataset and querydatapoint filenames from the user and call the SequentialSearch and RTreeImplementation
        functions. It then computes and displays the efficiency of R-Tree algorithm against the Sequential search
    """
    arguments = sys.argv
    
    if len(arguments) == 3: 
    
        datasetFilename = arguments[1]
        dataQueryFilename = arguments[2]

        #reading data from dataset file
        with open(datasetFilename) as f:
            dataset = f.read().split('\n')
    
        #reading data from query file
        with open(dataQueryFilename) as f:
            queryDataPoints = f.read().split('\n')


        print("\nExecuting sequential scan algorithm: \n")
        averageTimeSeq = SequentialSearch(dataset,queryDataPoints)

        print("\nExecuting R Tree algorithm: \n")
        averageTimeRtree = RTreeImplementation(dataset,queryDataPoints)

        print("\n\nR tree scan algorithm is",int (averageTimeSeq/averageTimeRtree), "times faster than sequential scan algorithm\n")

    else:
        print("Please enter the command with 2 agruments. You can refer to the screenshot provided in the report for more details.")

if __name__ == "__main__":
    main()