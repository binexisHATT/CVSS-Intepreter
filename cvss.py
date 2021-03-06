#!/usr/bin/env python3

__author__ = 'Alexis Rodriguez'
__version__ = '1.0'
__email__ = 'rodriguez10011999@gmail.com'

"""
Sources used for scoring descriptions:
  - CompTIA CySa+ Study Guide by Mike Chapple and David Seidl
  - https://www.first.org/cvss/v3.0/specification-document

  Example CVSS v2 : CVSS2#AV:N/AC:L/Au:N/C:C/I:C/A:C
  Example CVSS v3 : CVSS:3.1/AV:N/AC:L/PR:H/UI:N/S:U/C:L/I:L/A:N
"""

try:
  from sys import argv, exit
  from os import _exit
except ImportError as err:
  print(f"Import Error: {err}")

# Metric definitions-----------------------------------------------------------------------------------------------------------------------
access_vector = {
  'L': 'Local (L): The attacker must have physical or logical access to the affected system.',
  'A': 'Adjacent Network (A): The attacker must have access to the local network that the affected system is connected to.',
  'N': 'Network (N): The attacker can remotely exploit the vulnerability.',
  'P': 'The attack requires the attacker to physically touch or manipulate the vulnerable component.'
}

access_complexitiyv2 = {
  'L': 'Low (L): Exploiting the vulnerability does not require specilized conditions.',
  'M': 'Medium (M): Exploiting the vulnerability requires "somewhat specilized" conditions.',
  'H': 'High (H): Exploiting the vulnerability requires "specialized" conditions that would be difficult to find.'
}

access_complexitiyv3 = {
  'H': 'High (H): A successful attack depends on conditions beyond the attacker\'s control. That is, a successful attack cannot be accomplished at will, but requires the attacker to invest in some measurable amount of effort in preparation or execution against the vulnerable component before a successful attack can be expected.',
  'L': 'Low (L): Specialized access conditions or extenuating circumstances do not exist. An attacker can expect repeatable success against the vulnerable component.'
}

privileges_required = {
  'N': 'None (N): The attacker is unauthorized prior to attack, and therefore does not require any access to settings or files of the vulnerable system to carry out an attack.',
  'L': 'Low (L): The attacker requires privileges that provide basic user capabilites that could normally affect only settings and files ownwed by a user. Alternatively, an attacker with Low privileges has the ability to access only non-sensitive resources.',
  'H': 'High (H): The attacker requires privileges that provide significant (e.g., administrative) control over the vulnerable component allowing access to component-wide settings and files.'
}

user_interaction = {
  'N': 'None (N): The vulnerable system can be exploited without interaction from any user.',
  'R': 'Required (R): Successful exploitation of this vulnerability requires a user to take some action before the vulnerability can be exploited. For example, a successful exploit may only be possible during the installation of an application by a system administrator.'
}

scope = {
  'U': 'Unchanged (U): An exploited vulnerability can only affect resources managed by the same security authority. In this case, the vulnerable component and the impacted component are either the same, or both are managed by the same security authority.',
  'C': 'Changed (C): An exploited vulnerability can affect resources beyond the security scope managed by the security authority of the vulnerable component. In this case, the vulnerable component and the impacted component are different and managed by different security authorities.'
}

authentication = {
  'N': 'None (N): Attackers do not need to authenticate to exploit the vulnerability.',
  'S': 'Single (S): Attackers would need to authenticate once to exploit the vulnerability.',
  'M': 'Multiple (M): Attackers would need to authenticate two or more times exploit the vulnerability.'
}

#   Impact Metrics for v2
confidentialityv2 = {
  'N': 'None (N): There is no confidentiality impact.',
  'P': 'Partial (P): Access to some information is possible, but the attacker does not have control over what information is compromised.',
  'C': 'Complete (C): All information on the system is compromised.'
}

integrityv2 = {
  'N': 'None (N): There is no integrity impact.',
  'P': 'Partial (P): Modification of some information is possible, but the attacker does not have control over what information is modified.',
  'C': 'Complete (C): The integrity of the system is totally compromised, and the attacker may change any information at will.'
}

availabilityv2 = {
  'N': 'None (N): There is no availablity impact.',
  'P': 'Partial (P): The performance of the system is degraded.',
  'C': 'Complete (C): The system is completely shut down.'
}

#   Impact Metrics for V3
confidentialityv3 = {
  'H': 'High (H): There is total loss of confidentiality, resulting in all resources within the impacted component being divulged to the attacker.',
  'L': 'Low (L): There is some loss of confidentiality. Access to some restricted information is obtained, but the attacker does not have control over what information is obtained, or the amount or kind of loss is constrained.',
  'N': 'None (N): There is no loss of confidentiality within the impacted component.'
}

integrityv3 = {
  'H': 'High (H): There is a total loss of integrity, or a complete loss of protection.',
  'L': 'Low (L): Modification of data is possible, but the attacker does not have control over the consequence of a modification, or the amount of modification is constrained.',
  'N': 'None (N): There is no loss of integrity within the impacted component.'
}

availabilityv3 = {
  'H': 'High (H): There is total loss of availability, resulting in the attacker being able to fully deny access to resources in the impacted component; this loss is either sustained (while the attacker continues to deliver the attack) or persistent (the condition persists even after the attack has completed).',
  'L': 'Low (L): There is reduced performance or interruptions in resource availability',
  'N': 'None (N): There is no impact to availability within the impacted component.'
}
#  Cvss2 class definition-----------------------------------------------------------------------------------------------------------------------
class Cvss2:
  """CVSS version 2 class definition."""
  def __init__(self, score):
    self.score = score

  def parse_score(self):
    """Parses the CVSS v2 scores into a dictionary.
      Argument:
        None

      Return:
        score_dict (dict): dictionary containing metric identifiers as keys and metric values as values.
    """
    score_metrics = self.score[6:].split('/')
    score_dict = {score[:score.rfind(':')] : score[score.rfind(':') + 1:]  for score in score_metrics}
    return score_dict

  def determine_metrics(self, score_dict):
    """Determine the values corresponding to each metric.
      Argument:
        score_dict (dict): dictionary containing the metrics of the score in key, value pairs.

      Return:
        metric_definitions (dict): dictionary containing the corresponding definitions according the value of each CVSS metric.
    """
    metric_definitions = {}
    for identifier, value in score_dict.items():
        metric_definitions[identifier] = self.check_definition(identifier.lower(), value)
    return metric_definitions

  def check_definition(self, identifier, value):
    """Check the definition for each metric identifieer and its corresponding metric definition.
      Argument:
        identifier (str): the metric to check for e.g. Au
        value (str): the value assigned to the identifier.
      
      Return:
        the definition assigned to value in the dictionary concerned with the identifier.
    """
    if identifier == 'av':
      return access_vector[value]

    elif identifier == 'ac':
      return access_complexitiyv2[value]

    elif identifier == 'au':
       return authentication[value]

    elif identifier == 'c':
      return confidentialityv2[value]

    elif identifier == 'i':
      return integrityv2[value]

    else:
      return availabilityv2[value]
# Cvss3 class definition-----------------------------------------------------------------------------------------------------------------------
class Cvss3:
  """CVSS version 3 class definition."""
  def __init__(self, score):
    self.score = score

  def parse_score(self):
    """Parses the CVSS v3 scores into a dictionary.
      Argument:
        None

      Return:
        score_dict (dict): dictionary containing metric identifiers as keys and metric values as values.
    """
    score_metrics = self.score[self.score.find('/') + 1:].split('/')
    score_dict = {score[:score.rfind(':')] : score[score.rfind(':') + 1:]  for score in score_metrics}
    return score_dict

  def determine_metrics(self, score_dict):
    """Determine the values corresponding to each metric.
      Argument:
        score_dict (dict): dictionary containing the metrics of the score in key, value pairs.

      Return:
        metric_definitions (dict): dictionary containing the corresponding definitions according the value of each CVSS metric.
    """
    metric_definitions = {}
    for identifier, value in score_dict.items():
      metric_definitions[identifier] = self.check_definition(identifier.lower(), value)
    return metric_definitions

  def check_definition(self, identifier, value):
    """Check the definition for each metric identifieer and its corresponding metric definition.
      Argument:
        identifier (str): the metric to check for e.g. Au
        value (str): the value assigned to the identifier.

      Return:
        the definition assigned to value in the dictionary concerned with the identifier.
    """
    if identifier == 'av':
      return access_vector[value]

    elif identifier == 'ac':
      return access_complexitiyv3[value]

    elif identifier == 'pr':
      return privileges_required[value]

    elif identifier == 'ui':
      return user_interaction[value]

    elif identifier == 's':
      return scope[value]

    elif identifier == 'c':
      return confidentialityv3[value]

    elif identifier == 'i':
      return integrityv3[value]

    else:
      return availabilityv3[value]

def main():
  if len(argv) == 1 or len(argv) > 2:
    print("\033[31mUsage: cvss.py [CVSS Score]\033[0m")
    exit(1)

  cvss_score = argv[1].strip()
  if '2' in cvss_score[:6]:
    instance = Cvss2(cvss_score)
  else:
    instance = Cvss3(cvss_score)

  score_dict = instance.parse_score()
  results = instance.determine_metrics(score_dict)

  print('\n')
  for key, val in results.items():
    print('\033[31m\033[1m' + key + '\033[0m -> ', end=' ')
    val_list = val.split()
    print('\x1b[1;33m' + val_list[0] + '\033[0m', end=' ')
    print('\033[33m' + val_list[1] + '\033[0m', end=' ')
    print(' '.join(val_list[2:]))
  print('\n')

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    try:
      exit(1)
    except SystemExit:
      _exit(1)
