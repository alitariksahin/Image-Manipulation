
# return img, nested list
def read_ppm_file(f):
    fp = open(f)
    fp.readline()  # reads P3 (assume it is P3 file)
    lst = fp.read().split()
    n = 0
    n_cols = int(lst[n])
    n += 1
    n_rows = int(lst[n])
    n += 1
    max_color_value = int(lst[n])
    n += 1
    img = []
    for r in range(n_rows):
        img_row = []
        for c in range(n_cols):
            pixel_col = []
            for i in range(3):
                pixel_col.append(int(lst[n]))
                n += 1
            img_row.append(pixel_col)
        img.append(img_row)
    fp.close()
    return img, max_color_value


# Works
def img_printer(img):
    row = len(img)
    col = len(img[0])
    cha = len(img[0][0])
    for i in range(row):
        for j in range(col):
            for k in range(cha):
                print(img[i][j][k], end=" ")
            print("\t|", end=" ")
        print()


filename = input()
operation = int(input())


# DO_NOT_EDIT_ANYTHING_ABOVE_THIS_LINE
#in this code "column" represents a row of pixels, "pixel" represents an element of column, "val" represents red, green and blue.
#min-max normalization
if operation==1:
    #oldMax is equal to max_color_value, oldMin is zero and as inputs i get new max as maximum and
    #new min as mimimum.
    img, oldMax = read_ppm_file(filename)
    oldMin=0
    minimum=int(input())
    maximum=int(input())
    # i used enumerate function in for loop to get both their values and indexes
    for c, column in enumerate(img):
        for p, pixel in enumerate(column):
            for v, oldVal in enumerate(pixel):
                newVal=(oldVal-oldMin)/(oldMax-oldMin)*(maximum-minimum)+minimum
                newVal=round(newVal,4)
                #this part is where the old value is replaced with the new one.
                img[c][p][v]=newVal
    img_printer(img)
#z-score normalization
if operation==2:
    img, max_color_value = read_ppm_file(filename)
    #for each channel i find their mean and standard deviation.
    for val in range(3):
        Channel_Sum = 0
        val_number = 0
        for column in img:
            for pixel in column:
                Channel_Sum+=pixel[val]
                #count how many pixels there are
                val_number+=1
        Channel_Mean=Channel_Sum/val_number
        Mean_Sum=0
        for column in img:
            for pixel in column:
                Mean_Sum+=(pixel[val]-Channel_Mean)**2
        #add 1e-6 to avoid possible 0 cases
        Standard_Deviation=(Mean_Sum/val_number)**0.5+1e-6
        for c,column in enumerate(img):
            for p,pixel in enumerate(column):
                #this is where i update each channel's values one by one
                img[c][p][val]=round(((pixel[val]-Channel_Mean)/Standard_Deviation),4)
    img_printer(img)
#black and white conversion
if operation==3:
    img, max_color_value = read_ppm_file(filename)
    for c, column in enumerate(img):
        for p, pixel in enumerate(column):
            avg_sum=0
            for val in pixel:
                avg_sum+=val
            #just replace the old values in a pixel with the average value of the pixel
            average_val=int(avg_sum/3)
            img[c][p]=[average_val,average_val,average_val]
    img_printer(img)
#convolution
if operation==4:
    img, max_color_value = read_ppm_file(filename)
    file=input()
    stride=int(input())
    # i read the file i get as an input and convert the filter to a nested list
    f=open(file,"r")
    lst_filter=[]
    for i in f.readlines():
        new_lst=i.split()
        line=[]
        for j in new_lst:
            line.append(float(j))
        lst_filter.append(line)
    f.close()
    #this list will give the final list of columns
    output=[]
    #using stride as an increment number in range will handle jumps of the filter
    for column in range(0,len(img)-len(lst_filter)+1,stride):
        #this list will store a column of pixels
        column_lst=[]
        for pixel in range(0,len(img[column])-len(lst_filter)+1,stride):
            #this list will store a single pixel
            temporary_lst=[]
            for rgb in range(3):
                #this sum gives one pixel's one channel,namely r, g or b.
                sum = 0
                for val in range(len(lst_filter)):
                    for lav in range(len(lst_filter)):
                        sum+=img[column+val][pixel+lav][rgb]*lst_filter[val][lav]
                #make sum 0 if it is below zero, make sum max value if it is above max value
                if sum < 0:
                    sum = 0
                if sum > max_color_value:
                    sum = max_color_value
                sum=int(sum)
                temporary_lst.append(sum)
            column_lst.append(temporary_lst)
        output.append(column_lst)
    img_printer(output)
#paddling zeros and convolution
#in this part there is only one part different from the operation 4, which is the paddling part
if operation==5:
    img, max_color_value = read_ppm_file(filename)
    file = input()
    stride = int(input())
    #conversion of file to a nested list
    f = open(file, "r")
    lst_filter = []
    for i in f.readlines():
        new_lst = i.split()
        line = []
        for j in new_lst:
            line.append(float(j))
        lst_filter.append(line)
    f.close()
    #padding part
    zero_pad=[0,0,0]
    #padding "columns" of zeros to the beginning and the end of the img list as seperate columns
    for column in range(len(img)):
        for i in range(int((len(lst_filter)-1)/2)):
            img[column].insert(0,zero_pad)
            img[column].append(zero_pad)
    new_column = [zero_pad] * len(img[0])
    #padding pixels' of zeros to the beginning and the end of the each column
    for i in range(int((len(lst_filter)-1)/2)):
        img.insert(0,new_column)
        img.append(new_column)
    output = []
    #this part is the same as operation 4
    for column in range(0, len(img) - len(lst_filter) + 1, stride):
        column_lst = []
        for pixel in range(0, len(img[column]) - len(lst_filter) + 1, stride):
            temporary_lst = []
            for rgb in range(3):
                sum = 0
                for val in range(len(lst_filter)):
                    for lav in range(len(lst_filter)):
                        sum += img[column + val][pixel + lav][rgb] * lst_filter[val][lav]
                if sum < 0:
                    sum = 0
                if sum > max_color_value:
                    sum = max_color_value
                sum = int(sum)
                temporary_lst.append(sum)
            column_lst.append(temporary_lst)
        output.append(column_lst)
    img_printer(output)
#color quantization
if operation==6:
    img, max_color_value = read_ppm_file(filename)
    rng=int(input())
    # i create a copy of img list, which is composed of empty lists
    #i will use this list in order to be able to avoid calling the same pixel again and again.
    #i will update called empty lists with ["Done"] so that in the next recursive call their path
    #will be eliminated by a base condition i will put
    new_lst=[]
    for column in range(len(img)):
        temp_lst=[]
        for pixel in range(len(img[column])):
            temp_lst.append([])
        new_lst.append(temp_lst)
    def recursive_calls(img,new_lst,column=0,pixel=0,direction="down"):
        #base conditions for edges of our image
        if column>=len(img) or pixel>=len(img[0]) or column<0 or pixel<0:
            return
        #base condition to prevent the recursive call from calling the same pixel again and again
        if new_lst[column][pixel]==["Done"]:
            return
        else:
            new_lst[column][pixel]=["Done"]


        #In these parts, in accordance with directions, it does spesific calculations and comparisons and updates
        if direction == "down":

            if column!=len(img)-1:
                Checker=True
                for i in range(3):
                    #compare two successive pixel to see if they differ less than the range we get from input
                    if (img[column][pixel][i] - img[column+1][pixel][i]) >= rng or (img[column+1][pixel][i] - img[column][pixel][i]) >= rng:
                        Checker=False
                if Checker:
                    #if it is, update the second pixel
                    img[column+1][pixel]=img[column][pixel]

            #this part implies that it will move on to the right pixel and go up
            elif column==len(img)-1:
                Checker = True
                for k in range(3):
                    # compare two successive pixel to see if they differ less than the range we get from input
                    if img[column][pixel + 1][k] - img[column][pixel][k] >= rng or img[column][pixel][k] - img[column][pixel + 1][k] >= rng:
                        Checker = False
                if Checker:
                    # if it is, update the second pixel
                    img[column][pixel + 1] = img[column][pixel]


        if direction == "up":

            if column!=0:
                Checker = True
                for j in range(3):
                    # compare two successive pixel to see if they differ less than the range we get from input
                    if img[column][pixel][j]-img[column-1][pixel][j] >= rng or img[column-1][pixel][j] - img[column][pixel][j] >= rng:
                        Checker = False
                if Checker:
                    # if it is, update the second pixel
                    img[column-1][pixel] = img[column][pixel]

            # this part implies that it will move on to the right pixel and go down
            elif column==0 and pixel<len(img[0])-1:
                Checker = True
                for k in range(3):
                    # compare two successive pixel to see if they differ less than the range we get from input
                    if img[column][pixel + 1][k] - img[column][pixel][k] >= rng or img[column][pixel][k] - img[column][pixel + 1][k] >= rng:
                        Checker = False
                if Checker:
                    # if it is, update the second pixel
                    img[column][pixel + 1] = img[column][pixel]


        #Recursive part
        #directions will determine the way and which calculations will be implemented
        direction="down"
        recursive_calls(img,new_lst,column+1,pixel,direction)
        direction="up"
        recursive_calls(img,new_lst,column-1,pixel,direction)
        #this change is necessary because while moving to the right pixel,
        #it should have the exact direction it will follow next
        if column==len(img)-1:
            direction="up"
        if column==0:
            direction="down"
        recursive_calls(img,new_lst,column,pixel+1,direction)
        return img

    img=recursive_calls(img,new_lst)
    img_printer(img)
#3d color quantization
if operation==7:
    img, max_color_value = read_ppm_file(filename)
    rng = int(input())
    # create a copy of img list made up of empty lists
    new_lst=[]
    for column in range(len(img)):
        temporary_lst=[]
        for pixel in range(len(img[column])):
            lst=[]
            for val in range(3):
                lst.append([])
            temporary_lst.append(lst)
        new_lst.append(temporary_lst)

    def recursive_call(img,new_lst,column=0,pixel=0,index=0,direction="down",rf="right"):
        #base conditions
        if column>=len(img) or pixel>=len(img[0]) or index==3 or column<0 or pixel<0:
            return
        #preventing recalls
        if new_lst[column][pixel][index]==["Done"]:
            return
        else:
            new_lst[column][pixel][index]=["Done"]

        #comparisons and updates according to directions
        if direction=="down":
            if column!=len(img)-1:
                checker=True
                if img[column][pixel][index] - img[column + 1][pixel][index] >= rng or img[column + 1][pixel][index] - img[column][pixel][index] >= rng:
                    checker=False
                if checker:
                    img[column + 1][pixel][index]=img[column][pixel][index]
            #this part is concerned with the edges and moving to right or left at those regions
            if column==len(img)-1:
                if rf == "right":
                    if pixel != len(img[0]) - 1:
                        checker = True
                        if img[column][pixel][index] - img[column][pixel + 1][index] >= rng or img[column][pixel + 1][index] - img[column][pixel][index] >= rng:
                            checker = False
                        if checker:
                            img[column][pixel + 1][index] = img[column][pixel][index]

                    if pixel == len(img[0])-1:
                        # this spesific case may occur only once because index change will occur twice
                        # this parts occurs when recursive function is at the end of both columns and pixels
                        # here in the last pixel we move on to the next channel
                        if index != 2:
                            checker = True
                            if img[column][pixel][index] - img[column][pixel][index+1] >= rng or img[column][pixel][index+1] - img[column][pixel][index] >= rng:
                                checker = False
                                #update the index if difference is less than range
                            if checker:
                                img[column][pixel][index+1] = img[column][pixel][index]
                if rf == "left":
                    if pixel != 0:
                        checker = True
                        if img[column][pixel][index] - img[column][pixel - 1][index] >= rng or img[column][pixel - 1][index] - img[column][pixel][index] >= rng:
                            checker = False
                        if checker:
                            img[column][pixel - 1][index] = img[column][pixel][index]

                    if pixel ==0:
                        # this spesific case may occur only once because index change will occur twice
                        # this parts occurs when recursive function is at the beginning of both columns and pixels
                        # here in the last pixel we move on to the next channel
                        if index != 2:
                            checker = True
                            if img[column][pixel][index] - img[column][pixel][index + 1] >= rng or img[column][pixel][index + 1] - img[column][pixel][index] >= rng:
                                checker = False
                                # update the index if difference is less than range
                            if checker:
                                img[column][pixel][index + 1] = img[column][pixel][index]
        #this time what work with is the upward movement and jumps towards right or left pixel at the edges
        if direction=="up":
            if column!=0:
                checker = True
                #checks to see if the difference between the upper one and itself is less than range
                if img[column][pixel][index] - img[column - 1][pixel][index] >= rng or img[column - 1][pixel][index] - img[column][pixel][index] >= rng:
                    checker = False
                #if so, then update the upper one. Make it same as the first one
                if checker:
                    img[column - 1][pixel][index] = img[column][pixel][index]
            #in this part, i dealth with going right at top.
            if column==0:
                #this part handle moving on to the right
                if rf == "right":
                    if pixel != len(img[0]) - 1:
                        checker = True
                        if img[column][pixel][index] - img[column][pixel + 1][index] >= rng or img[column][pixel + 1][index] - img[column][pixel][index] >= rng:
                            checker = False
                        if checker:
                            img[column][pixel + 1][index] = img[column][pixel][index]
                    # this is another end point where the index is required to be changed, and comparisons and updates are made.
                    if pixel == len(img[0])-1:
                        if index != 2:
                            checker = True
                            if img[column][pixel][index] - img[column][pixel][index+1] >= rng or img[column][pixel][index+1] - img[column][pixel][index] >= rng:
                                checker = False
                            if checker:
                                img[column][pixel][index+1] = img[column][pixel][index]
                # this part handle moving on to the left.
                if rf == "left":
                    if pixel != 0:
                        checker = True
                        if img[column][pixel][index] - img[column][pixel - 1][index] >= rng or img[column][pixel - 1][index] - img[column][pixel][index] >= rng:
                            checker = False
                        if checker:
                            img[column][pixel - 1][index] = img[column][pixel][index]
                    # this is another end point where the index is required to be changed, and comparisons and updates are made.
                    if pixel == 0:
                        if index!=2:
                            checker = True
                            if img[column][pixel][index] - img[column][pixel][index + 1] >= rng or img[column][pixel][index + 1] - img[column][pixel][index] >= rng:
                                checker = False
                            if checker:
                                img[column][pixel][index + 1] = img[column][pixel][index]

        #The recursive part
        #Directions will decide on the comparisons and updates
        direction="down"
        recursive_call(img, new_lst, column + 1, pixel, index, direction,rf)
        direction="up"
        recursive_call(img, new_lst, column - 1, pixel, index, direction,rf)
        #this direction updates are necessary because i want to set the direction accordingly before going on either right or left
        if column == len(img) - 1:
            direction = "up"
        if column == 0:
            direction = "down"
        rf="right"
        recursive_call(img, new_lst, column, pixel + 1, index, direction,rf)
        if column == len(img) - 1:
            direction = "up"
        if column == 0:
            direction = "down"
        rf="left"
        recursive_call(img, new_lst, column, pixel - 1, index, direction,rf)
        #just as direction updates rf (right-left) is essential.
        #in this case i change the channel, but to make comparisons during change both direction and rf have to be determined
        if column == len(img) -1 and pixel == len(img[0]):
            rf="left"
        if column == 0 and pixel == 0:
            rf="right"
        recursive_call(img, new_lst, column, pixel, index + 1, direction,rf)
        return img
    img = recursive_call(img, new_lst)
    img_printer(img)

# DO_NOT_EDIT_ANYTHING_BELOW_THIS_LINE

