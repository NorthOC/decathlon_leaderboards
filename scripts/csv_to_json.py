import csv
import json
import os
"""
Event 	         Unit

100 m 	        Seconds        
Long jump 	    Metres         
Shot put 	      Metres         
High jump 	    Metres         
400 m 	        Seconds        
110 m hurdles 	Seconds        
Discus throw 	  Metres         
Pole vault 	    Metres         
Javelin throw   Metres         
1500 m 	        Minutes:Seconds


Event 	        A 	      B 	  C

100 m 	        25.4347 	18 	  1.81
Long jump 	    0.14354 	220 	1.4
Shot put 	      51.39 	  1.5 	1.05
High jump 	    0.8465 	  75 	  1.42
400 m 	        1.53775 	82 	  1.81
110 m hurdles 	5.74352 	28.5 	1.92
Discus throw 	  12.91 	  4 	  1.1
Pole vault 	    0.2797 	  100 	1.35
Javelin throw 	10.14 	  7 	  1.08
1500 m 	        0.03768 	480 	1.85

Points = INT(A(B — P)^C) for track events (faster time produces a higher score)
Points = INT(A(P — B)^C) for field events (greater distance or height produces a higher score)

P is the performance by the athlete, measured in seconds (running), 
metres (throwing), or centimetres (jumping)
"""

# each event is either a track 't' or a field 'f' challenge
EVENT_TYPE = ['t', 'f', 'f', 'f', 't', 't', 'f', 'f', 'f', 't']

# scores are calculated with these parameters for each disciple
PARAMETERS_BY_DISCIPLE = [[25.4347, 	18, 	  1.81],
                          [0.14354, 	220, 	  1.4],
                          [51.39, 	  1.5, 	  1.05],
                          [0.8465, 	  75, 	  1.42],
                          [1.53775, 	82, 	  1.81],
                          [5.74352, 	28.5, 	1.92],
                          [12.91, 	  4, 	    1.1],
                          [0.2797, 	  100, 	  1.35],
                          [10.14, 	  7, 	    1.08],
                          [0.03768, 	480, 	  1.85]
                          ]

DECATHLON_KEY_VALUES = ["name", "100m", "long_jump",
"shot_put", "high_jump", "400m",
"110m_hurdles", "discus_throw", "pole_vault",
"javelin_throw", "1500m", "score", "leaderboard"]

# formula to calculate track events INT(A(B — P)^C)
def track_formula(a, b, c, p):
  return int(a*(b-p)**c)

# formula to calculate field events INT(A(P — B)^C)
def field_formula(a, b, c, p):
  return int(a*(p-b)**c)

def convert_to_meters(result):
  result = float(result)
  #print(f"meters: {result}")
  return result

def convert_to_centimeters(result):
  result = float(result) * 100
  #print(f"centimeters: {result}")
  return result

def convert_to_seconds(result):
  time = result.split(".")

  #check whether the result is in seconds:miliseconds or minutes:seconds:milliseconds
  match len(time):
    case 2:
      result = float(result)
    case 3:
      result = float(time[0]) * 60 + float(time[1])
  #print(f"seconds: {result}")
  return result


# returns the total score of a single contestant
def calculate_total_score(contestant):
  
  total_score = 0

  for event in range(1, len(contestant)):

    a, b, c = PARAMETERS_BY_DISCIPLE[event-1]

    # field events are measured in centimenters or meters
    if EVENT_TYPE[event-1] == 'f':

      if event-1 in [1, 3, 7]:
        event_result = convert_to_centimeters(contestant[event])

      else:
        event_result = convert_to_meters(contestant[event])

      score = field_formula(a, b, c, event_result)

    # else it is a track event which is measured in seconds
    else:
      event_result = convert_to_seconds(contestant[event])
      score = track_formula(a, b, c, event_result)

    total_score += score

  return total_score

# used in a sort method to sort by total score
def by_total_score(e):
  return e[-1]

# return a list of contestants with final scores calculated
def generate_final_scores(contestants):
  list_of_contestants = []
    
  for contestant in contestants:
    total_score = str(calculate_total_score(contestant))
    contestant.append(total_score)
    list_of_contestants.append(contestant)

  #sort contestants in ascending order
  list_of_contestants.sort(key=by_total_score, reverse=True)

  return list_of_contestants

# returns a list of contestants with their positions on the leaderboard
def generate_leaderboards(contestants):

    # count all different scores
    counts = dict()

    for contestant in contestants:

      if contestant[-1] in counts:
          counts[contestant[-1]] += 1
      else:
          counts[contestant[-1]] = 1

    place = 1
    i = 0
    while i <= len(contestants)-1:

      final_score = contestants[i][-1]
      no_of_winners = counts[final_score]

      # if there is one winner, just append the number on the leader board
      if no_of_winners == 1:
        contestants[i].append(f"{place}")
        place +=1
        i += 1
      
      # if there are a number of winners append the number to all of them
      else:
        for j in range(0, no_of_winners):
          contestants[i+j].append(f"{place}-{place + no_of_winners-1}")
        i += j + 1
        place += no_of_winners

    return contestants

# generates json dump string with key, value pairs
def generate_json_dump(contestants):
  json_data = []

  for contestant in contestants:
    json_dict = {}

    for i in range(0, len(contestant)):
      json_dict[DECATHLON_KEY_VALUES[i]] = contestant[i]

    json_data.append(json_dict)

  data = json.dumps(json_data, indent=4)

  return data

  
# convert csv to json file
def csv_to_json(path, timestamp, filename, delimiter=";"):
  with open(os.path.join(path, timestamp, filename), mode='r') as csvfile:

    contestants = csv.reader(csvfile, delimiter=delimiter)
    contestants_with_scores = generate_final_scores(contestants=contestants)
    contestants_with_winners = generate_leaderboards(contestants=contestants_with_scores)
    
    json_data = generate_json_dump(contestants_with_winners)

  with open(os.path.join(path,timestamp,'output.json'), mode='x') as output:
      output.write(json_data)