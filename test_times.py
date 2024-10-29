import times
import pytest

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
    large = times.time_range("2010-01-12 10:45:00", "2010-01-12 12:00:00")
    short = times.time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00")
    
    #compute overlap time
    result = times.compute_overlap_time(large, short)
    
    #Program should return empty list containing the starting time as the only two elements
    expected = [('2010-01-12 10:45:00', '2010-01-12 10:45:00')]
    
    assert expected == result
    