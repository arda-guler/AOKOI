from gauss_solver import *

# = = = OBSERVATION INPUT = = = 
obs1_RA = RightAscension(44, 51, 12.05)
obs1_DEC = Declination(-5, 3, 1.01)
obs1_time = 390 # this is in seconds, which can be measured
                # relative to any reference time you wish
                #
                # only the time differences between observations
                # are important
obs1_datetime = "2001-01-01"
obs1 = Observation(obs1_RA, obs1_DEC, obs1_time, obs1_datetime)

obs2_RA = RightAscension()
obs2_DEC = Declination()
obs2_time = 
obs2_datetime = ""
obs2 = Observation(obs2_RA, obs2_DEC, obs2_time, obs2_datetime)

obs3_RA = RightAscension()
obs3_DEC = Declination()
obs3_time = 
obs3_datetime = ""
obs3 = Observation(obs3_RA, obs3_DEC, obs3_time, obs3_datetime)
# = = =   = = =   = = =   = = =

# compute orbit
orbital_elements = gauss(obs1, obs2, obs3)

# print result
print(orbital_elements)
