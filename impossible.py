'''
http://fivethirtyeight.com/features/can-you-solve-the-impossible-puzzle/
'''
def run_simulation(answer_list):
    simulation = ImpossibleScenario()
    label = box_label('INITIAL_STATE')
    print('{label}\n{simulation}'.format(label=label,
                                         simulation=simulation))

    for i, answer_bool in enumerate(answer_list):
        simulation.record_answer(answer_bool)
        name = 'Susan' if i % 2 else 'Pete'
        turn = i // 2 + 1
        label = box_label('After {name}\'s turn {turn}'.format(name=name,
                                                               turn=turn))

        print('{label}\n{simulation}'.format(label=label,
                                             simulation=simulation))

def box_label(label):
    bar_str = (len(label) + 4) * '#'
    return '{}\n# {} #\n{}\n'.format(bar_str, label, bar_str)

def convert_tuple_set_to_str(tuple_set):
    return ', '.join((str(t) for t in tuple_set))

def convert_tuple_set_dict_to_str(input_dict):
    output_line_generator = (
        '{:>5}: {}\n'.format(key, convert_tuple_set_to_str(tuple_set))
        for key, tuple_set in input_dict.items()
    )

    return ''.join(output_line_generator)


class ImpossibleScenario(object):
    def __repr__(self):
        return (
            "Pete's answers: {}\n"
            "Susan's answers: {}\n\n"
            "Pete's number possibilities:\n{}\n"
            "Susan's number possibilities:\n{}\n"
        ).format(
            self.pete_answer_list,
            self.susan_answer_list,
            convert_tuple_set_dict_to_str(self.product_factors_dict),
            convert_tuple_set_dict_to_str(self.sum_components_dict)
        )

    def __init__(self):
        pair_set = set(((x, y) for x in range(1, 10) for y in range(1, x + 1)))
        product_set = set((pair[0] * pair[1] for pair in pair_set))
        sum_set = set((pair[0] + pair[1] for pair in pair_set))

        self.pete_answer_list = []
        self.susan_answer_list = []

        self.product_factors_dict = {
            product: set((p for p in pair_set if p[0] * p[1] == product))
            for product in product_set
        }

        self.sum_components_dict = {
            this_sum: set((p for p in pair_set if p[0] + p[1] == this_sum))
            for this_sum in sum_set
        }

    def record_pete_answer(self, answer_bool):
        self.pete_answer_list.append(answer_bool)

        if answer_bool:
            self.product_factors_dict = {
                key: value
                for key, value in self.product_factors_dict.items()
                if len(value) == 1
            }
        else:
            self.product_factors_dict = {
                key: value
                for key, value in self.product_factors_dict.items()
                if len(value) > 1
            }

        product_dict_tuples = set(
            (item for subset in self.product_factors_dict.values()
                  for item in subset)
        )

        self.sum_components_dict = {
            key: pair_set.intersection(product_dict_tuples)
            for key, pair_set in self.sum_components_dict.items()
            if set(pair_set).intersection(product_dict_tuples)
        }

    def record_susan_answer(self, answer_bool):
        self.susan_answer_list.append(answer_bool)

        if answer_bool:
            self.sum_components_dict = {
                key: value
                for key, value in self.sum_components_dict.items()
                if len(value) == 1
            }
        else:
            self.sum_components_dict = {
                key: value
                for key, value in self.sum_components_dict.items()
                if len(value) > 1
            }

        sum_dict_tuples = set(
            (item for subset in self.sum_components_dict.values()
                  for item in subset)
        )

        self.product_factors_dict = {
            key: set(pair_set).intersection(sum_dict_tuples)
            for key, pair_set in self.product_factors_dict.items()
            if set(pair_set).intersection(sum_dict_tuples)
        }

    def record_answer(self, answer_bool):
        is_pete_answering = (
            len(self.pete_answer_list) <= len(self.susan_answer_list)
        )

        if is_pete_answering:
            self.record_pete_answer(answer_bool)
        else:
            self.record_susan_answer(answer_bool)


if __name__ == '__main__':
    this_scenario_answer_list = [False] * 8 + [True]
    run_simulation(this_scenario_answer_list)
