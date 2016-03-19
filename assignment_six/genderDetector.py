from gender_detector import GenderDetector 

detector = GenderDetector('us')

with open('UserNames.txt') as f: 
    lines = f.readlines()
    lines = [x.strip('\n') for x in lines]

for guesses in lines:
    value = detector.guess(guesses)
    print value
