#!/usr/bin/env python3
# Quick hack to analyze responses to "matrix questions" from Google Forms.
# Edit the MAPPING dictionary below to reflect the matrix column labels.
# Let Google Forms save the responses in Google Drive, then export a CSV file.
# Run this script with the CSV file name as the first parameter.
# Matrix questions will be detected by square brackets in the header columns.
import csv
import re
import sys

MAPPING = {
  'sehr': 2,
  'eher ja': 1,
  'eher nein': -1,
  'gar nicht': -2,
  'weiß nicht': 0
}

if len(sys.argv) != 2:
  print('please specify CSV file name as first parameter')
  sys.exit(42)

filename = sys.argv[1]

headers = None
rows = []

with open(filename) as csvfile:
  reader = csv.reader(csvfile, delimiter=',', quotechar='"')

  for row in reader:
    if not headers:
      headers = row
    else:
      rows.append(row)

matrix_questions = {}

for i, header in enumerate(headers):
  m = re.match(r'(.+) \[(.+)\]', header)

  if m:
    question = m.group(1)
    label = m.group(2)

    if question not in matrix_questions:
      matrix_questions[question] = {}

    matrix_questions[question][i] = label

def calculate_results(columns):
  results = {}

  for row in rows:
    for i, label in columns.items():
      if i not in results:
        results[i] = 0

      results[i] += MAPPING[row[i]]

  return results

results = {}

for question, columns in matrix_questions.items():
  results[question] = calculate_results(columns)

def print_results(columns, results):
  for i, result in sorted(results.items(), key=lambda item: item[1], reverse=True):
    label = columns[i]
    print(f'{result}: {label}')

for question, result in results.items():
  print('========================================')
  print(question)
  print_results(matrix_questions[question], result)

print('========================================')

