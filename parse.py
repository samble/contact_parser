#!python3

import csv

def main():
  f = open ('tabulated_contacts_bernie_rutherford.csv')
  rd = csv.reader(f)
  csvlines = []
  for row in rd:
    #print(row)
    csvlines.append(row)
  itr = iter(csvlines)

  for line in itr:
    l = []
    print(str(line))

    phone_name_line = None
    street_line = None
    city_line = None
    email_line = None

    if line[0].find('\n') >= 0:
      print('single fields')
      phone_name_line, street_line, city_line, email_line = parse_line(line[0])
    else:
      while line[0].find('Email:') < 0:
        l.append(line)
        line = next(itr)
      l.append(line)

      phone_name_line = l[0]
      street_line = None
      if len(l) == 4:
        street_line = l[1]
      city_line = l[-2]
      email_line = l[-1]

    fields = {}
    fields['phone'] = phone_name_line[0]
    fields['name'] = phone_name_line[1]
    if street_line: fields['addr'] = street_line[0]

    deets = city_line[0].split()
    if len(deets) > 0: fields['age'] = deets[0]
    if len(deets) > 1: fields['gender'] = deets[1]
    if len(deets) == 3: fields['u_thing'] = deets[2]

    fields['city'] = city_line[1]
    email = email_line[1]
    if email: fields['email'] = email

    print(fields)

def parse_line(line):
  #phone_name_line, street_line, city_line, email_line = parse_line(line)
  s = line.split('\n')
  phone = line[0][0:14]
  name = line[0][14:line[0].find('\n')]

  city = s[1]
  fields['addr'] = addr

  deets = s[2]

  age, gender, u_thing, city = extract_deets(deets)
  fields['age'] = age
  fields['gender'] = gender
  fields['u_thing'] = u_thing
  fields['city'] = city

  print(str(fields))
