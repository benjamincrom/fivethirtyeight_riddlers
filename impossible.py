'''
http://fivethirtyeight.com/features/can-you-solve-the-impossible-puzzle/
'''
class ImpossibleScenario:
    @staticmethod
    def convert_dict_to_str(input_dict):
        output_str = ''
        for key, value_tuple_list in input_dict.iteritems():
            output_str += '     {}: '.format(key)
            for value_tuple in value_tuple_list:
                output_str += '{}, '.format(value_tuple)

            output_str = '{}\n'.format(output_str[:-2])

        output_str += '\n'

        return output_str

    def __repr__(self):
        return (
            "Pete's answers: {}\n"
            "Susan's answers: {}\n\n"
            "Pete's number possibilities: \n{}"
            "Susan's number possibilities: \n{}"
        ).format(
            self.pete_answer_list,
            self.susan_answer_list,
            self.convert_dict_to_str(self.product_factors_dict),
            self.convert_dict_to_str(self.sum_components_dict)
        )

    def __init__(self):
        pair_list = [(x, y) for x in range(1, 10) for y in range(1, x + 1)]

        product_set = set([pair[0] * pair[1] for pair in pair_list])
        sum_set = set([pair[0] + pair[1] for pair in pair_list])

        self.pete_answer_list = []
        self.susan_answer_list = []

        self.product_factors_dict = {
            this_product: [p for p in pair_list if p[0] * p[1] == this_product]
            for this_product in product_set
        }

        self.sum_components_dict = {
            this_sum: [p for p in pair_list if p[0] + p[1] == this_sum]
            for this_sum in sum_set
        }

    def record_pete_answer(self, answer_bool):
        self.pete_answer_list.append(answer_bool)

        if answer_bool:
            self.product_factors_dict = {
                key: value
                for key, value in self.product_factors_dict.iteritems()
                if len(value) == 1
            }
        else:
            self.product_factors_dict = {
                key: value
                for key, value in self.product_factors_dict.iteritems()
                if len(value) > 1
            }

        product_dict_tuples = [item
                               for sublist in self.product_factors_dict.values()
                               for item in sublist]

        new_components_dict = {}
        for key, pair_list in self.sum_components_dict.iteritems():
            new_pair_list = [pair for pair in pair_list
                             if pair in product_dict_tuples]

            if new_pair_list:
                new_components_dict[key] = new_pair_list

        self.sum_components_dict = new_components_dict

    def record_susan_answer(self, answer_bool):
        self.susan_answer_list.append(answer_bool)
        if answer_bool:
            self.sum_components_dict = {
                key: value
                for key, value in self.sum_components_dict.iteritems()
                if len(value) == 1
            }
        else:
            self.sum_components_dict = {
                key: value
                for key, value in self.sum_components_dict.iteritems()
                if len(value) > 1
            }

        sum_dict_tuples = [item
                           for sublist in self.sum_components_dict.values()
                           for item in sublist]

        new_products_dict = {}
        for key, pair_list in self.product_factors_dict.iteritems():
            new_pair_list = [pair for pair in pair_list
                             if pair in sum_dict_tuples]

            if new_pair_list:
                new_products_dict[key] = new_pair_list

        self.product_factors_dict = new_products_dict

    def record_answer(self, answer_bool):
        is_pete_answering = (
            len(self.pete_answer_list) <= len(self.susan_answer_list)
        )

        if is_pete_answering:
            self.record_pete_answer(answer_bool)
        else:
            self.record_susan_answer(answer_bool)

if __name__ == '__main__':
    simulation = ImpossibleScenario()

    print '#################'
    print '# INITIAL STATE #'
    print '#################\n'
    print simulation

    for i in range(4):
        simulation.record_answer(False)
        print '########################'
        print '# After Pete\'s turn {} #'.format(i + 1)
        print '########################\n'
        print simulation

        simulation.record_answer(False)
        print '#########################'
        print '# After Susan\'s turn {} #'.format(i + 1)
        print '#########################\n'
        print simulation

    simulation.record_answer(True)
    print '#######################'
    print '# After Pete\'s turn 5 #'
    print '#######################\n'
    print simulation
