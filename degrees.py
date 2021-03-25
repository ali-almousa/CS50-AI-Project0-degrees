import csv
import sys
from util import Node, StackFrontier, QueueFrontier

# maps names to a set of corresponding person_ids
names = {}

# maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}

def load_data(directory):
    """Load data from CSV files into memory"""
    # Load people
    # with open("small/people.csv", "r", encoding="utf-8") as file:
    with open(f"{directory}/people.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])
    # Load movies
    # with open("small/movies.csv", "r", encoding="utf-8") as file:
    with open(f"{directory}/movies.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    # with open("small/stars.csv", "r", encoding="utf-8") as file:
    with open(f"{directory}/stars.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass

def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded")

    # source = person_id_for_name("Kevin Bacon")
    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    # target = person_id_for_name("Tom Cruise")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("not connected")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    :param source: (person_id)
    :param target: (person_id)
    :return: the shortest list of (movie_id, person_id) pairs
    that connect the target to the source. Otherwise None if not possible
    """
    # create the path
    solution = []

    # counter for actors explored
    num_explored = 0

    # create a node from Node class that represents the source
    start = Node(state=source, parent=None, action=None)
    # create a frontier object of type Queue
    frontier = QueueFrontier()
    # initialize frontier to the source
    frontier.add(start)

    # create a set of explored nodes
    explored = set()

    while True:
        # empty frontier means no solution
        if frontier.empty():
            solution = None
            return solution

        # choose (remove) a node from the frontier
        node = frontier.remove()
        num_explored += 1
        for movie in people[str(node.state)]["movies"]:
            if str(movie) in people[str(target)]["movies"]:
                if num_explored == 1:
                    solution.append((movie, target))
                    return solution
                solution.append((movie, target))
                while node.parent is not None:
                    solution.append((node.action, node.state))
                    node = node.parent
                solution = solution[::-1]
                return solution


        # add the node to the explored set
        explored.add(node.state)

        # add neighbors to the frontier
        for movie_id, person_id in neighbors_for_person(node.state):
            if not frontier.contains_state(person_id) and person_id not in explored:
                next_node = Node(state=person_id, parent=node, action=movie_id)
                frontier.add(next_node)





def person_id_for_name(name):
    """returns the IMDB id as a string for a,
    person's name resolving ambiguities as needed."""
    # cool get() would grab the value of the passed key in a dict
    person_ids = list(names.get(name.lower(), set()))
    # id not found
    if len(person_ids) == 0:
        return None
    # more than one ids due to the fact that the user could have entered only the first name
    # and many actors share the same first name.
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        # iterate to print all identical first names actors
        for person_id in person_ids:
            # here person would become a dict as the value of key person_id in people dict is a dict in itself
            # {'name': 'Kevin Bacon', 'birth': '1958', 'movies': {'104257', '112384'}}
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        # index 0 included to grab the element out of the list for future use as a string "102"
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    :param person_id:
    :return: (movie_id, person_id) pairs for people
    who starred with a given person.
    """

    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


main()

# if __name__ == "__main__":
#     main()