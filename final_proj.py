import json
import re


f = open("mytree.json", 'r')
tree = json.load(f)
f.close()


class Node(object):
    def __init__(self, val = None, left = None, right = None):
        self.val = val
        self.left = left
        self.right = right


# insert questions
root = Node(tree[0])
root.left = Node(val = tree[1][0])
root.left.left = Node(val = tree[1][1][0])
root.left.right = Node(val = tree[1][1][0])
root.left.left.left = Node(val = tree[1][1][1][0])
root.left.right.right = Node(val = tree[1][1][1][0])
root.left.left.right = Node(val = tree[1][1][1][0])
root.left.right.left = Node(val = tree[1][1][1][0])
root.right = Node(val = tree[1][0])
root.right.left = Node(val = tree[1][1][0])
root.right.right = Node(val = tree[1][1][0])
root.right.left.left = Node(val = tree[1][1][1][0])
root.right.right.right = Node(val = tree[1][1][1][0])
root.right.left.right = Node(val = tree[1][1][1][0])
root.right.right.left = Node(val = tree[1][1][1][0])

# val Nodes
root.left.left.left.left = Node(val = tree[1][1][1][1][0])
root.left.left.left.right = Node(val = tree[1][1][1][2][0])
root.left.left.right.left = Node(val = tree[1][1][2][1][0])
root.left.left.right.right = Node(val = tree[1][1][2][2][0])
root.left.right.left.left = Node(val = tree[1][2][1][1][0])
root.left.right.left.right = Node(val = tree[1][2][1][2][0])
root.left.right.right.left = Node(val = tree[1][2][2][1][0])
root.left.right.right.right = Node(val = tree[1][2][2][2][0])
root.right.left.left.left = Node(val = tree[2][1][1][1][0])
root.right.left.left.right = Node(val = tree[2][1][1][2][0])
root.right.left.right.left = Node(val = tree[2][1][2][1][0])
root.right.left.right.right = Node(val = tree[2][1][2][2][0])
root.right.right.left.left = Node(val = tree[2][2][1][1][0])
root.right.right.left.right = Node(val = tree[2][2][1][2][0])
root.right.right.right.left = Node(val = tree[2][2][2][1][0])
root.right.right.right.right = Node(val = tree[2][2][2][2][0])

def yes(prompt):
    '''Return true or false for yes or no of the question.
    
    Parameters
    ----------
    prompt: the question to ask
    
    Returns
    -------
    True or False
    '''
    inputs = input(prompt+" ")
    yes_pattern = re.compile(r"(?:yeah|y|yes|yup|sure|yep|yay)[^a-zA-Z0-9]*",re.I|re.M)
    no_pattern = re.compile(r"(?:n|no|nope|not|nay)[^a-zA-Z0-9]*",re.I|re.M)
    if yes_pattern.findall(inputs) != []:
        return True
    elif no_pattern.findall(inputs) != []:
        return False
    else:
        print("Not a yes/no answer")


questions = ["Do you prefer a restaurant with rating 4 and higher?",
             "Do you prefer a restaurant with more than 100 reviews?",
             "Do you need the restaurant is currently open?",
             "Do you mind if the restaurant costs 100$ and higher per person?"
            ]


def recommendation(questions):
    '''Return restaurant objects matching the answers of the questions.
    
    Parameters
    ----------
    questions: the list of questions to ask
    
    Returns
    -------
    A list of all restaurant objects matching the answers
    '''
    current_node = root
    for i in questions:
        if yes(i):
            current_node = current_node.left
        else:
            current_node = current_node.right
    return current_node.val




def recommendation_by_city(result, input1):
    '''Return restaurant objects that match question answers by city.
    
    Parameters
    ----------
    result: the list of restaurant objects 
    input1: the city name
    
    Returns
    -------
    A list of all restaurant objects
    '''
    new_result = []
    for restaurant in result:
        if restaurant['city'] == input1:
            new_result.append(restaurant)
    return new_result



def recommendation_info(result):
    '''print restaurant name, category, city ans state.
    
    Parameters
    ----------
    result: the list of restaurant objects 
    
    Returns
    -------
    Restaurant information in one line
    '''
    if len(result) == 0:
        print("Sorry, they are no restaurants matching your options")
    else:
        i = 0
        print("\n Recommended Restaurants\n")
        for i in range(len(result)):
            print(str(i+1) + " " + result[i]['name'] + ", " + result[i]['category'] + ", " +                result[i]['city'] + ", " + result[i]['state'])

       


def input_format(input):
     return "+".join(input.split(" "))

if __name__ == "__main__":

    result = recommendation(questions)
    input_1 = " "
    if len(result) > 100:
        input_1 = input('\n There are many restaurants! Please give a city name: ')
        updated_result = recommendation_by_city(result, input_1)
    else:
        updated_result = result
    recommendation_info(updated_result)
    
    n = 1
    while input_1 != "exit" and input_1 != " ":
        #n += 1
        input_2 = input_format(input('\n Enter a number for more info, choose another city, or exit:'))

        if input_2 == "exit":
            print("Bye!")
            break
            
        elif input_2.isnumeric():
            print("Launching")

            url = updated_result[int(input_2)-1]['url']
            try:
                print("in web browser...")
                import webbrowser
                browser= webbrowser.get('chrome')
                browser.open(url)
            except KeyError:
                print("Sorry, this restaurant has no preview page.")
                
        else:
            updated_result = recommendation_by_city(result, input_2)
            recommendation_info(updated_result)
            

            continue

