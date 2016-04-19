

def poi_interaction_ratios(data_dict):
    """
    :param data_dict: List of employees and their features
    :return: Populates the `to_poi_ratio` and `from_poi_ratio` keys for
             each person in the dataset as either a number or `NaN` and returns
             a new data_dict
    """

    features = ['from_poi_to_this_person', 'from_this_person_to_poi', 'from_messages', 'to_messages']
    for k, v in data_dict.iteritems():
        invalid = False
        for feature in features:
            if v[feature] == 'NaN':
                v['to_poi_ratio'] = 'NaN'
                v['from_poi_ratio'] = 'NaN'
                invalid = True # If any of the fields are NaN, we skip that person
                break
        if v['poi'] == True:
            v['to_poi_ratio'] = 'NaN' # This person is a POI, so we set to NaN to avoid double counting
            v['from_poi_ratio'] = 'NaN'
        if v['poi'] == False and not invalid:
            if v['from_messages'] < v['from_poi_to_this_person'] or v['to_messages'] < v['from_this_person_to_poi']:
                # Some people (James Bannatine for instance) have more e-mails from POI than from_messages overall
                # This doesn't make sense, so we set to NaN to avoid having inflated numbers
                v['to_poi_ratio'] = 'NaN'
                v['from_poi_ratio'] = 'NaN'
                continue
            else:
                total_emails_received = v['from_messages']
                total_emails_sent = v['to_messages']
                v['to_poi_ratio'] = float(v['from_this_person_to_poi']) / total_emails_sent
                v['from_poi_ratio'] = float(v['from_poi_to_this_person']) / total_emails_received
    return data_dict

def financial_data_feature(data_dict):

    """
    :param data_dict: List of employees and their features
    :return: Populates the `financial_data` key for each person in the dataset as either a number or `NaN`
            and returns a new data_dict
    """

    features = ["total_stock_value", "total_payments"]
    for k, v in data_dict.iteritems():
        data_dict[k]['stock_and_payments'] = 0
        for feature in features:
            if v[feature] == 'NaN':
                # Checks if any of the four features are NaN -- we want an aggregate sum of all 4
                data_dict[k]['stock_and_payments'] = 'NaN'
                break
            else:
                data_dict[k]['stock_and_payments'] += v[feature]
    return data_dict