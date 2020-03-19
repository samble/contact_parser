#!python3

import csv
import sys

def main():
  f = open (sys.argv[1])
  rd = csv.reader(f)
  csvlines = []
  for row in rd:
    #print(row)
    csvlines.append(row)
  itr = iter(csvlines)

  dicts = []

  for line in itr:
    l = []
    #print(str(line))

    phone = None
    name = None
    street = None
    city = None
    age = None
    gender = None
    party = None
    email = None

    if line[0].find('\n') >= 0:
      phone, name, street, city, age, gender, party, email = parse_line(line[0])
      #print(phone_name_line)
      #print(street_line)
      #print(city_line)
      #print(email_line)
    elif len(line) == 1:
      while line[0].find('Party:') < 0:
        l.append(line[0])
        line = next(itr)
      l.append(line[0])

      #print(l)
      phone = l[0][-14:]
      name = l[0][:-15]

      if len(l) == 4:
        street = l[1]

      deets, age = l[-2].rsplit('Age:')
      age = age.strip()

      city, gender = deets.rsplit('Sex:')
      gender = gender.strip()
      city = city.strip()

      email, party = l[-1].rsplit('Party:')
      party = party.strip()
      email = email.strip()

    else:
      while line[1].find('Party:') < 0:
        l.append(line)
        line = next(itr)
      l.append(line)

      #print(l)
      phone = l[0][1]
      name = l[0][0]

      if len(l) == 4:
        street = l[1][0]

      city = l[-2][0]
      deets = l[-2][1]

      deets, age = deets.rsplit('Age:', 1)
      age = age.strip()

      deets, gender = deets.rsplit('Sex:', 1)
      gender = gender.strip()

      email = l[-1][0]
      party = l[-1][1][6:].strip()

    fields = {}
    fields['phone'] = phone
    fields['name'] = name
    fields['addr'] = street
    fields['city'] = city

    fields['age'] = age
    fields['gender'] = gender
    fields['u_thing'] = party

    fields['email'] = email

    #print(fields)
    dicts.append(fields)

  write_csv(dicts)

def write_csv(dicts):
  cols = ['phone', 'name', 'addr', 'city', 'age', 'gender', 'u_thing', 'email']
  with open('outfile.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=cols)
    writer.writeheader()
    for d in dicts:
      writer.writerow(d)

def parse_line(line):
  #phone_name_line, street_line, city_line, email_line = parse_line(line)
  s = line.split('\n')

  name = s[0]
  phone = s[1]
  
  street = ''
  if len(s) > 3:
    street = s[2]
  
  deets = s[-2]
  age, gender, city = extract_deets(deets)

  #print(s)
  email, party = s[-1].split('Party:')
  party = party.strip()

  return phone, name, street, city, age, gender, party, email


def extract_deets(deets):
  age = ''
  gender = ''
  city = ''

  deets, age = deets.rsplit('Age:', 1)
  age = age.strip()

  city, gender = deets.rsplit('Sex:', 1)
  gender = gender.strip()

  return age, gender, city


if __name__ == '__main__':
  main()
