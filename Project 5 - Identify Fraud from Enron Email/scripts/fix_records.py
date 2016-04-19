def fixBhatnagar(data_dict):

    """
    :param data_dict:
    :return: Fixes out of sync records of Sanjay Bhatnagar and returns a data_dict with the
             updated values
    """
    data_dict['BHATNAGAR SANJAY'] = data_dict.fromkeys(data_dict['BHATNAGAR SANJAY'], 'NaN')
    data_dict['BHATNAGAR SANJAY']['expenses'] = 137864
    data_dict['BHATNAGAR SANJAY']['total_payments'] = 137864
    data_dict['BHATNAGAR SANJAY']['exercised_stock_options'] = 15456290
    data_dict['BHATNAGAR SANJAY']['restricted_stock'] = 2604490
    data_dict['BHATNAGAR SANJAY']['restricted_stock_deferred'] = -2604490
    data_dict['BHATNAGAR SANJAY']['total_stock_value'] = 15456290
    data_dict['BHATNAGAR SANJAY']['from_messages'] = 29
    data_dict['BHATNAGAR SANJAY']['to_messages'] = 523
    data_dict['BHATNAGAR SANJAY']['shared_receipt_with_poi'] = 463
    data_dict['BHATNAGAR SANJAY']['from_this_person_to_poi'] = 1
    data_dict['BHATNAGAR SANJAY']['from_poi_to_this_person'] = 0
    data_dict['BHATNAGAR SANJAY']['poi'] = False
    return data_dict

def fixBelfer(data_dict):
    """
    :param data_dict:
    :return: Fixes out of sync records of Robert Belfer and returns a data_dict with the
             updated values
    """
    data_dict['BELFER ROBERT'] = data_dict.fromkeys(data_dict['BELFER ROBERT'], 'NaN')
    data_dict['BELFER ROBERT']['deferred_income'] = -102500
    data_dict['BELFER ROBERT']['expenses'] = 3285
    data_dict['BELFER ROBERT']['director_fees'] = 102500
    data_dict['BELFER ROBERT']['total_payments'] = 3285
    data_dict['BELFER ROBERT']['restricted_stock'] = 44093
    data_dict['BELFER ROBERT']['restricted_stock_deferred'] = -44093
    data_dict['BELFER ROBERT']['poi'] = False
    return data_dict