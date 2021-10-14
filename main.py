#################################################
# Abrar Abir
#################################################

import ImageWriter

#################################################
# Functions 
#################################################

# Edited version of given convertBlackWhite(pic)
# Not only makes the picture black & white
# but also removes border from left to right
def convertBlackWhite(pic):
    rows = ImageWriter.getHeight(pic)
    columns = ImageWriter.getWidth(pic)
    for i in range(0, rows):
        borderStart = False
        borderEnd = False
        # initializes whether border started or ended- before scanning each row.
        for j in range(0, columns):
            c = ImageWriter.getColor(pic, j, i)
            if sum(c)//3 >= 85:
                borderEnd = borderStart
                # if border has been started, 
                # finding a white pixel ends the border.
                # If border has not been started, 
                # finding a white pixel doesn't end the border.
                c = [255]*3
            else:
                borderStart = True
                c = [255*(borderStart)*(not borderEnd)]*3
                # color = white if border has started but didn't end.
            ImageWriter.setColor(pic, j, i, c)

# removes border from both side
def removeBorder(pic):
    convertBlackWhite(pic)
    # calls convertBlackWhite(pic) to remove border from left to right.
    rows = ImageWriter.getHeight(pic)
    columns = ImageWriter.getWidth(pic)
    for i in range(0, rows):
        borderStart = False
        borderEnd = False
        # initializes whether border started or ended- 
        # before scanning each row.
        for j in range(columns - 1, -1, -1): 
            # -1 for changing the direction of scan.
            c = ImageWriter.getColor(pic,j,i)
            if c == [255]*3:
                borderEnd = borderStart
                # if border has been started, 
                # finding a white pixel ends the border.
                # If border has not been started, 
                # finding a white pixel doesn't end the border.
                if borderEnd:
                    break
                    # If border ended, nothing to do in this row.
            else:
                borderStart = True
                c = [255*(borderStart)*(not borderEnd)]*3
                # color = white if border has started but didn't end.
                ImageWriter.setColor(pic, j, i, c)

def findVerticalBlob(pic,startRow, endRow, startColumn):
    columns = ImageWriter.getWidth(pic)
    startBlob = None
    # stores the starting row for the blob.
    for j in range(startColumn, columns):
        allWhite = True
        # stores if the all pixels of the row are white
        # initializes before scanning every row
        for i in range(startRow ,endRow):
            c = ImageWriter.getColor(pic, j, i)
            if startBlob == None:
                if c == [0]*3:
                    startBlob = j
                    break
                    # if blob hasn't been started 
                    # and a black pixel is found,
                    # the row index is stored, and the loop breaks 
            else:
                allWhite *= (c == [255]*3)
                # if blob has been started, 
                # allWhite stores if each pixel is white 
        if allWhite == True and startBlob != None and j > startBlob:
            endBlob = j
            # if a row is found to be all white after the blob has started, 
            # endBlob stores the last row for the blob 
            return [startBlob, endBlob]
        if j == columns - 1:
            return None    

# removes color from pic within a given range   
def removeColor(pic, startx, starty, endx, endy):
    for i in range(starty, endy + 1):
        for j in range(startx, endx + 1):
            ImageWriter.setColor(pic, j, i, [255]*3)

def horizontalSegmentation(pic):
    rows = ImageWriter.getHeight(pic)
    columns = ImageWriter.getWidth(pic)
    top = bottom = 0
    startBlob = None
    # stores the starting row for the blob.
    for i in range(rows):
        allWhite = True
        # stores if the all pixels of the row are white
        # initializes before scanning every row
        for j in range(columns):
            c = ImageWriter.getColor(pic, j, i)
            if startBlob == None:
                if c == [0]*3:
                    startBlob = i
                    break
                    # if blob hasn't been started and
                    # a black pixel is found,
                    # the row index is stored, 
                    # and the loop breaks 
            else:
                allWhite *= (c == [255]*3)
                # if blob has been started, 
                # allWhite stores if each pixel is white 
        if allWhite == True and startBlob != None and i > startBlob:
            endBlob = i
            # if a row is found to be all white
            #  after the blob has started, 
            # endBlob stores the last row for the blob
            if endBlob - startBlob > bottom - top:
                top, bottom = startBlob, endBlob
                startBlob = None
    return [top, bottom]

def verticalSegmentation(pic):
    horizontalSegment = horizontalSegmentation(pic)
    # only runs on the biggest blob
    blobs = []
    startCol = 0
    verticalSegment = findVerticalBlob(pic, horizontalSegment[0],
                                        horizontalSegment[1], startCol)
    while verticalSegment != None:
        # scans for vetical blobs untill the edge
        blobs.append([verticalSegment, verticalSegment[1] - verticalSegment[0]])
        startCol = verticalSegment[1]
        verticalSegment = findVerticalBlob(pic, horizontalSegment[0], 
                                            horizontalSegment[1], startCol)
    return blobs[:6] # only return 1st 6 blob segments

# 2d list of black pixel ratio in 4 quadrants for each digits.
digitBlackPixels = [
[0.49,	0.51,	0.52,	0.48],
[0.72,	0.34,	0.005,	0.69],
[0.54,	0.30,	0.51,	0.34],
[0.50,	0.24,	0.22,	0.47],
[0.16,	0.28,	0.41,	0.52],
[0.35,	0.69,	0.32,	0.46],
[0.41,	0.64,	0.54,	0.52],
[0.59,	0.32,	0.37,	0.08],
[0.54,	0.54,	0.51,	0.51],
[0.53,	0.54,	0.39,	0.62]]

# Helper function for rounding
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    # You do not need to understand how this function works.
    import decimal
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

# decodes character from image
def decodeCharacter(pic, startRow, endRow, startCol, endCol):
    blackPixelQuad = []
    for quadrant in [1, 0, 2, 3]: # for counterclockwise quadrants
        blackPixelCount = 0
        startRowQuad = roundHalfUp(startRow + 
                                    (endRow - startRow)*(quadrant//2)/2)
        # starting row of the quadrant
        endRowQuad = roundHalfUp(startRow + 
                                    (endRow - startRow)*(quadrant//2 + 1)/2)
        # ending row of the quadrant.
        for i in range(startRowQuad, endRowQuad + 1):
            startColQuad = roundHalfUp(startCol + 
                            (endCol - startCol)*(quadrant % 2)/2)
            # starting column of the quadrant
            endColQuad = roundHalfUp(startCol + 
                            (endCol - startCol)*(quadrant % 2 + 1)/2)
            # ending column of the quadrant
            for j in range(startColQuad, endColQuad + 1):
                if ImageWriter.getColor(pic, j, i) == [0]*3:
                    blackPixelCount += 1
        blackPixelQuad.append(blackPixelCount/
                    ((endRowQuad - startRowQuad)*(endColQuad - startColQuad)))
        # storing black pixel count for each quadrant
    digitBlackQuad = []
    for digit in range(10):
        difference = 0
        for index in range(4):
            difference += abs(blackPixelQuad[index] 
                                    - digitBlackPixels[digit][index])
        digitBlackQuad.append(difference)
        # stroring respective differences in black pixel count
    return digitBlackQuad.index(min(digitBlackQuad)) 

def decodeLicensePlate(filename):
    license = ''
    pic = ImageWriter.loadPicture(filename)
    removeBorder(pic)
    columns = findVerticalBlob(pic,0,ImageWriter.getHeight(pic),0)
    removeColor(pic, columns[0],0,columns[1],ImageWriter.getHeight(pic))
    horizontalSegment = horizontalSegmentation(pic)
    verticalSegment = verticalSegmentation(pic)
    for item in verticalSegment:
        license += str(decodeCharacter(pic, horizontalSegment[0], 
                                horizontalSegment[1], item[0][0], item[0][1]))
        removeColor(pic, item[0][0], horizontalSegment[0], 
                                item[0][1], horizontalSegment[1])
        # removes the decoded digit from the image
    return license
