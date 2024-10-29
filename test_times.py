import times
import pytest
import yaml
import ast

def test_given_input():
    #standard input time ranges
    large = times.time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = times.time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
    #compute overlap
    result = times.compute_overlap_time(large, short)  
    #Compare program with known answer
    expected = [('2010-01-12 10:30:00', '2010-01-12 10:37:00'), ('2010-01-12 10:38:00', '2010-01-12 10:45:00')]   
    assert result == expected
    
def test_no_overlap():
    #time ranges 
    large = times.time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = times.time_range("2010-01-12 14:30:00", "2010-01-12 14:45:00",2,60)
    
    #compute overlap time
    result = times.compute_overlap_time(large, short)
    
    #Program should return empty list if their is no overlap time
    expected = []
    
    assert expected == result
    
    
def test_multi_interval():
    #time ranges 
    large = times.time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00",2,60)
    short = times.time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00",2,60)
    
    #compute overlap time
    result = times.compute_overlap_time(large, short)
    
    #Program should return same result as before 
    expected = [('2010-01-12 10:30:00', '2010-01-12 10:37:00'), ('2010-01-12 10:38:00', '2010-01-12 10:45:00')]
    
    assert expected == result
    
def test_same_time():
    #time ranges 
    large = times.time_range("2010-01-12 10:00:00", "2010-01-12 11:00:00")
    short = times.time_range("2010-01-12 11:30:00", "2010-01-12 12:45:00")
    
    #compute overlap time
    result = times.compute_overlap_time(large, short)
    
    #Program should return empty list containing the starting time as the only two elements
    expected = []
    
    assert expected == result
    
def test_backward_interval():
    expected_error = 'End time is before Start time, backward time input intervals'
    
    with pytest.raises(ValueError, match=expected_error):
        times.time_range("2010-01-12 10:00:00", "2010-01-12 09:00:00")
    
############################################################################################

#Pytest Parametrization#

############################################################################################

@pytest.mark.parametrize("first_range, second_range, expected_overlap", 
                         [
                         #1) test_given_input
                         (
                            times.time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00"), #first_range
                            times.time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60), #second_range
                            [('2010-01-12 10:30:00', '2010-01-12 10:37:00'), ('2010-01-12 10:38:00', '2010-01-12 10:45:00')] #expected results
                                
                         ),
                         #2)test_no_overlap
                         (
                            times.time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00"),
                            times.time_range("2010-01-12 14:30:00", "2010-01-12 14:45:00",2,60),
                            [] 
                         ),
                         #3) test_multi_interval
                         (
                            times.time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00",2,60),
                            times.time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00",2,60),
                            [('2010-01-12 10:30:00', '2010-01-12 10:37:00'), ('2010-01-12 10:38:00', '2010-01-12 10:45:00')]  
                         ),
                         #4)test_same_time
                         (
                            times.time_range("2010-01-12 10:45:00", "2010-01-12 12:00:00"),
                            times.time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00"),
                            [('2010-01-12 10:45:00', '2010-01-12 10:45:00')] 
                         )
                         ])
def test_parameterize_overlap(first_range,second_range,expected_overlap):
    result = times.compute_overlap_time(first_range, second_range)
    assert result == expected_overlap, (f'\nExpected result:{expected_overlap} \n \n Actual result:{result}\nASSERTION MESSAGE END')


############################################################################################

#Pytest Parametrization - Separation of code

############################################################################################

def data_load(file_name):
    with open(file_name, "r")as data_file:
        return yaml.safe_load(data_file)

data = data_load(file_name="fixtures.yml")

data_param = []
for KEY in data.keys():
    add = (
        times.time_range(
            data[KEY]['time_range_1']['start_time'],
            data[KEY]['time_range_1']['end_time'],
            data[KEY]['time_range_1']['number_of_intervals'],
            data[KEY]['time_range_1']['gap_between_intervals'],
        ),
        times.time_range(
            data[KEY]['time_range_2']['start_time'],
            data[KEY]['time_range_2']['end_time'],
            data[KEY]['time_range_2']['number_of_intervals'],
            data[KEY]['time_range_2']['gap_between_intervals'],
        ),
        [ast.literal_eval(i) for i in data[KEY]['expected']]
        
    )
    data_param.append(add)

@pytest.mark.parametrize("first_range,second_range,expected_overlap",data_param)
def test_parameterize_overlap_YAML(first_range,second_range,expected_overlap):
    result = times.compute_overlap_time(first_range, second_range)
    assert result == expected_overlap, (f'\nExpected result:{expected_overlap} \n \n Actual result:{result}\nASSERTION MESSAGE END')

