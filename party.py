'''
http://fivethirtyeight.com/features/the-perplexing-puzzle-of-the-proud-partygoers/
'''
import numpy
import random

N = 100

results = {}

class Person(object):
    def __init__(self, name):
        self.name = name
        self.friend_list = []

    def is_proud(self):
        if not self.friend_list: return False

        num_friends = len(self.friend_list)
        avg_num_friends = (
            sum(len(f.friend_list) for f in self.friend_list) / num_friends
        )

        return num_friends > avg_num_friends

    def __repr__(self):
        output_str = 'Name: {}\nFriends: {}\n'.format(self.name, len(self.friend_list))
        for friend in self.friend_list:
            output_str += '-- Friend {} has {} friends\n'.format(friend.name, [f.name for f in friend.friend_list])

        return output_str


def run_simulation(num_people):
    global results
    person_list = []
    for i in range(num_people):
        new_person = Person(i)
        for person in person_list:
            if bool(random.getrandbits(1)):
                person.friend_list.append(new_person)
                new_person.friend_list.append(person)

        person_list.append(new_person)

    percentage = sum(1 for person in person_list if person.is_proud()) / num_people
    if percentage > results.setdefault(num_people, percentage):
        results[num_people] = percentage

    return percentage

def iterate_simulations_gen(num_iterations, max_people):
    simulation_values_gen = (run_simulation(num_people)
                             for _ in range(num_iterations)
                             for num_people in range(1, max_people + 1))

    yield max(simulation_values_gen)

print(max(iterate_simulations_gen(400000, 10)))
print(results)