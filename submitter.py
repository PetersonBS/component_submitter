#!/usr/bin/python
import toscaparser
from toscaparser.tosca_template import ToscaTemplate
import os
import toscaparser.utils.urlutils
from system_prompt import Prompt
from mapper import Mapper
import sys


class Submitter:
  """Submitter class that is
  going to take care of launching the application from TOSCA descriptor"""

  def __init__(self, path):
    self.path = path
    if os.path.isfile(self.path):
      template = ToscaTemplate(self.path, None, True)
    elif toscaparser.utils.urlutils.UrlUtils.validate_url(self.path):
      template = ToscaTemplate(self.path, dict(), False)
    self.template = template

  def inputs_prompt(self):
    if Prompt("keep all the default value?").query_yes_no():
      print "proceeding to the launch of the application\n"
      Mapper(self.template)
    elif Prompt("change all the default value?").query_yes_no():
      print "proceeding to update of default value\n"
      self.update_all_default()
      Mapper(self.template)
    elif Prompt("input the value you want to modify"):
      print "updating the wanted input\n"
      self.update_inputs_value()
      Mapper(self.template)

  def update_all_default(self):
    self.template.parsed_params = dict()
    print "entering of update value of inputs. Press enter if you want to keep default"
    for item in self.template.inputs:
      print "\n%s should be from %s" % (item.name, item.type)
      value = Prompt("update %s: " % item.name).query_input()

      if value is not None:
        self.template.parsed_params[item.name]=value
      #  self.template.tpl["topology_template"]["inputs"][item.name]["default"] = value
    self.template=ToscaTemplate(self.path, self.template.parsed_params, False)


  def list_inputs(self):
    for item in self.template.inputs:
      print "the value of %s is %s" % (item.name,item.default)

  def update_inputs_value(self):
    print "below list of inputs, type the one you would like to modify:\n"
    for item in self.template.inputs:
      print item.name

    while Prompt("\nwould you like to update an input value").query_yes_no():
      self.update_wanted_input_value()
        
  def update_wanted_input_value(self):
    self.template.parsed_params=dict()
    wanted_input = Prompt("which one would you like to modify? ").query_input()
    for item in self.template.inputs:
      if wanted_input == item.name:
        self.template.parsed_params[wanted_input]=Prompt("%s :"% wanted_input).query_input()
        #self.template.tpl["topology_template"]["inputs"][item.name]["default"] = Prompt("%s :"% wanted_input).query_input()
    self.template=ToscaTemplate(self.path, self.template.parsed_params, False)

if __name__ == '__main__':
    print sys.argv
    print Submitter(sys.argv[1]).inputs_prompt()
