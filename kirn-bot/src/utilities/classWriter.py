import csv
import os

aeroString = "AERO: 201, 290, 371, 390, 417, 431, 444, 446, 455, 462, 464, 465, 471, 472, 480, 481, 482, 483, 485, 486, 487, 490, GENERAL"
bceeString = "BCEE: 231, 342, 343, 344, 345, 371, 451, 452, 455, 464, 465, 466"
biolString = "BIOL: 206, 261"
bldgString = "BLDG: 212, 341, 365, 366, 371, 390, 462, 463, 465, 471, 472, 473, 474, 475, 476, 477, 478, 482, 490, 490A, 490B, 491, 492, 493, 498, GENERAL"
chemString = "CHEM: 205"
civiString = "CIVI: 212, 231, 321, 341, 361, 372, 381, 382, 390, 432, 435, 437, 440, 453, 454, 464, 465, 466, 467, 468, 469, 471, 474, 483, 484, 490, 498, GENERAL"
coenString = "COEN: 212, 231, 243, 244, 311, 313, 315, 316, 317, 320, 345, 346, 352, 390, 413, 421, 422, 424, 432, 433, 434, 445, 446, 447, 451, 490, 498, GENERAL"
compString = "COMP: 108, 201, 208, 218, 228, 232, 233, 248, 249, 326, 333, 335, 339, 345, 346, 348, 352, 353, 354, 361, 367, 371, 376, 425, 426, 428, 432, 442, 444, 445, 451, 465, 472, 473, 474, 476, 477, 478, 479, 490, 492, 495, 498, 499, 6231, 6721, GENERAL"
econString = "ECON: 201, 203"
elecString = "ELEC: 242, 251, 273, 275, 311, 312, 321, 331, 342, 351, 353, 365, 367, 372, 390, 413, 421, 422, 423, 424, 425, 430, 431, 432, 433, 434, 435, 435, 436, 437, 438, 439, 440, 441, 442, 444, 445, 453, 455, 456, 457, 458, 463, 463, 463, 464, 465, 466, 470, 472, 473, 481, 482, 483, 490, 498, GENERAL"
encsString = "ENCS: 272, 282, 393, 483, 484, 498"
engrString = "ENGR: 108, 201, 202, 208, 213, 233, 242, 243, 244, 245, 251, 290, 301, 308, 311, 361, 371, 391, 392, 411, 412, 472, 490, 498"
iadiString = "IADI: 301, 401"
induString = "INDU: 211, 311, 320, 321, 323, 324, 330, 342, 371, 372, 410, 411, 412, 421, 423, 440, 441, 466, 475, 480, 490, 498, GENERAL"
mastString = "MAST: 218"
mechString = "MECH: 321, 343, 344, 351, 352, 361, 368, 370, 371, 375, 390, 411, 412, 414, 415, 421, 422, 423, 424, 425, 426, 444, 447, 448, 452, 453, 454, 460, 461, 462, 463, 471, 472, 473, 474, 476, 490, 498, GENERAL"
miaeString = "MIAE: 211, 215, 221, 311, 313, 380"
physString = "PHYS: 205, 252, 284"
soenString = "SOEN: 228, 287, 321, 331, 341, 342, 343, 344, 345, 357, 363, 384, 385, 387, 390, 422, 423, 448, 449, 471, 487, 490, 491, 498, 499, 6441, GENERAL"

classList = []
classList.append(aeroString)
classList.append(bceeString)
classList.append(biolString)
classList.append(bldgString)
classList.append(chemString)
classList.append(civiString)
classList.append(coenString)
classList.append(compString)
classList.append(econString)
classList.append(elecString)
classList.append(encsString)
classList.append(engrString)
classList.append(iadiString)
classList.append(induString)
classList.append(mastString)
classList.append(mechString)
classList.append(miaeString)
classList.append(physString)
classList.append(soenString)

splitList = []
nameList = []
numberList = []

file = open(os.path.join(os.path.dirname(__file__),
            "resources/classes.csv"), "w", newline="")
txtFile = open("courses.txt", "w")

with file:
    header = ["Full Name", "Class Name", "Class Number"]
    writer = csv.DictWriter(file, fieldnames=header)
    writer.writeheader()

    for x in range(len(classList)):
        splitList = classList[x].split(":")
        nameList = splitList[0].replace(" ", "").split(",")
        numberList = splitList[1].replace(" ", "").split(",")

        for y in range(len(numberList)):
            classNameAndNumber = nameList[0] + "-" + numberList[y]
            writer.writerow({"Full Name": classNameAndNumber,
                            "Class Name": nameList[0], "Class Number": numberList[y]})
            txtFile.write(classNameAndNumber + '\n')
