import os
import csv
import math


def create_solution_dictionary(solution):
    """ Read solution file, return a dictionary with key EventId and value (weight, label).
    Solution file headers: EventId, Label, Weight """

    solnDict = {}
    with open(solution, 'r') as f:
        soln = csv.reader(f)
        next(soln)  # header
        for row in soln:
            if row[0] not in solnDict:
                solnDict[row[0]] = (row[1], row[2])
    return solnDict


def check_submission(submission, Nelements):
    """ Check that submission RankOrder column is correct:
        1. All numbers are in [1, NTestSet]
        2. All numbers are unique """
    rankOrderSet = set()
    with open(submission, 'r') as f:
        sub = csv.reader(f)
        next(sub)  # header
        for row in sub:
            rankOrderSet.add(row[1])

    if len(rankOrderSet) != Nelements:
        print('RankOrder column must contain unique values')
        exit()
    elif not rankOrderSet.isdisjoint(set(range(1, Nelements + 1))):
        print('RankOrder column must contain all numbers from [1..NTestSet]')
        exit()
    else:
        return True


def AMS(s, b):
    """ Approximate Median Significance defined as:
        AMS = sqrt(
                2 { (s + b + br) log[1 + (s/(b + br))] - s}
              )
    where br = 10, b = background, s = signal, log is the natural logarithm """

    br = 10.0
    radicand = 2 * ((s + b + br) * math.log(1.0 + s / (b + br)) - s)
    if radicand < 0:
        print('radicand is negative. Exiting')
        exit()
    else:
        return math.sqrt(radicand)


def AMS_metric(solution, submission):
    """ Prints the AMS metric value to the screen.
    Solution File header: EventId, Class, Weight
    Submission File header: EventId, RankOrder, Class """

    numEvents = 550000  # number of events = size of test set

    # solutionDict: key = eventId, value = (label, class)
    solutionDict = create_solution_dictionary(solution)

    signal = 0.0
    background = 0.0
    if check_submission(submission, numEvents):
        with open(submission, 'r') as f:
            sub = csv.reader(f)
            next(sub)  # header row
            for row in sub:
                if row[2] == 's':  # only events predicted to be signal are scored
                    if solutionDict[row[0]][0] == 's':
                        signal += float(solutionDict[row[0]][1])
                    elif solutionDict[row[0]][0] == 'b':
                        background += float(solutionDict[row[0]][1])

        print(f'signal = {signal}, background = {background}')
        print(f'AMS = {AMS(signal, background)}')


if __name__ == "__main__":

    # enter path and file names here
    path = "./"
    solutionFile = "solution.csv"
    submissionFile = "submission.csv"

    AMS_metric(solutionFile, submissionFile)
