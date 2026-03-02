import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )
    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)

    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
    00/    - Administrative, an integer
    01/   - Administrative_Duration, a floating point number
    02/    - Informational, an integer
    03/    - Informational_Duration, a floating point number
    04/    - ProductRelated, an integer
    05/    - ProductRelated_Duration, a floating point number
    06/    - BounceRates, a floating point number
    07/    - ExitRates, a floating point number
    08/    - PageValues, a floating point number
    09/    - SpecialDay, a floating point number
    10/    - Month, an index from 0 (January) to 11 (December)
    11/    - OperatingSystems, an integer
    12/    - Browser, an integer
    13/    - Region, an integer
    14/    - TrafficType, an integer
    15/    - VisitorType, an integer 0 (not returning) or 1 (returning)
    16/    - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # Read data in from file
    with open("shopping.csv") as f:
        reader = csv.reader(f)
        next(reader)

        data = list()
        for row in reader:
            data.append({
                "evidence": [cell for cell in row[:-1]],
                "label" : 1 if row[-1] == "TRUE" else 0
            })

    # Dictionary access: List / dictionary structure
    #print(data[0])

    for i in range(len(data)):
        for j in range(len(data[i]['evidence'])):
            # int conversion
            if j in (0,2,4,11,12,13,14):
                data[i]['evidence'][j]= int(data[i]['evidence'][j])
            # float conversion
            if j in (1,3,5,6,7,8,9):
                data[i]['evidence'][j]= float(data[i]['evidence'][j])            
            # month conversion to int 0-11: recall month_conversion func
            if j == 10:
                data[i]['evidence'][j] = month_conversion(data[i]['evidence'][j])
            # returning visitor
            if j == 15:                
                data[i]['evidence'][j] = 1 if data[i]['evidence'][j] == 'Returning_Visitor' else 0
            if j == 16:                
                data[i]['evidence'][j] = 1 if data[i]['evidence'][j] == "TRUE" else 0
        mese = data[i]['evidence'][15]
        #print(mese)

    # returning feature, target for element in csv file
    evidence, labels = [], []
    for i in range(len(data)):
        evidence.append(data[i]['evidence'])
        labels.append(data[i]['label'])

    return evidence, labels


# month conversion function without any use of python libraries (calendar, datetime)
def month_conversion(string):
    month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    x = month_list.index(string)
    return x



def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    """
    X_training = [row["evidence"] for row in training]
    y_training = [row["label"] for row in training]
    model.fit(X_training,y_training)
    """
    neigh  = KNeighborsClassifier(n_neighbors=1)
    neigh.fit(evidence,labels)

    return neigh


def evaluate(y_test, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.

    # Make prediction on the testing set
    X_testing = [row["evidence"] for row in testing]
    y_testing = [row["label"] for row in testing]
    prediction = model.predict(X_testing)

    """
    #print(len(y_test))
    #print(len(predictions))


    # Compute how well we performed
    correct = 0 
    incorrect = 0 
    true_positive = 0
    true_negative = 0
    total = 0 

    for y_test, predictions in zip(y_test, predictions):
        total += 1
        if y_test == predictions:
            correct +=1
            if y_test == 1: 
                true_positive +=1
            if y_test == 0: 
                true_negative +=1 


        else:
            incorrect += 1
    
    print(total)


    sensitivity = true_positive/total
    specificity = true_negative/total 

    return sensitivity, specificity


 


if __name__ == "__main__":
    main()
