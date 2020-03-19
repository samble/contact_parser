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

  dicts = []

  for line in itr:
    l = []
    #print(str(line))

    phone_name_line = None
    street_line = None
    city_line = None
    email_line = None

    if line[0].find('\n') >= 0:
      phone_name_line, street_line, city_line, email_line = parse_line(line[0])
      #print(phone_name_line)
      #print(street_line)
      #print(city_line)
      #print(email_line)
    else:
      while line[0].find('Email:') < 0:
        l.append(line)
        line = next(itr)
      l.append(line)

      #print(l)
      phone_name_line = l[0]
      street_line = None
      if len(l) == 4:
        street_line = [l[1][1]]
      city_line = l[-2]
      email_line = l[-1]

    #print(city_line)
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
  phone = ''
  if not s[0][0].isalpha():
    phone = s[0][0:14]
    name = s[0][14:]
  else:
    name = s[0]

  street = ''
  if len(s) > 3:
    street = s[1]
  
  deets = s[-2]
  deets, city = extract_deets(deets)

  email = s[-1]
  if email.startswith('Email:'):
    email = email[6:]

  return [phone, name], [street], [deets, city], ['Email:', email]


def extract_deets(deets):
  age = ''
  gender = ''
  u_thing = ''
  city = ''

  age = deets[0:deets.find(' ')]

  if age.isnumeric():
    deets = deets[len(age) + 1:]

    if deets[0] in ('M','F'):
      gender = deets[0]
      deets = deets[1:]

    if deets[0] == ' ': #if they have the U
      u_thing = deets[1]
      city = deets[2:]
    else:
      city = deets

  else:
    age = ''
  return ' '.join((age, gender, u_thing)), city


if __name__ == '__main__':
  main()
