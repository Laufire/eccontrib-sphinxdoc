
# Info
__author__ = 'Laufire Technologies'
__email__ = 'laufiretechnologies@gmail.com'
__version__ = '0.0.3'

# Imports
import os
from os.path import basename, abspath
import random
import string
from imp import load_source
from docutils import nodes
from docutils.nodes import paragraph
from docutils.parsers.rst import Directive
from docutils.core import publish_doctree
from sphinx.addnodes import desc, desc_name, desc_addname, desc_content, desc_signature, desc_parameterlist, desc_parameter, desc_optional, compact_paragraph
from ec.interface import setBase

# State
startingCWD = os.getcwd()

# Helpers
def getRandomChars(size=16, chars=string.ascii_uppercase):
  return ''.join(random.choice(chars) for _ in range(size))

def getNodeTreeFromStr(string):
  """Gets a node tree from the given string.

  Check:

    * Is there a better implementation? The current one seems a bit hackish.
  """
  document = publish_doctree(string)

  return list([node for node in document.traverse()[1:] if node.parent == document]) # we've to return the chidren of the document, as returning the document itself, seems to duplicate the content of the current file being processed.

def getArgDesc(Arg):
  _type = Arg.get('type')

  return Arg.get('desc', Arg['type_str'])

def getReadableValue(val):
  if val == '':
    return "''"

  if val is None:
    return '<None>'

  return val

def getArgLabel(Arg):
  if 'default' in Arg:
    return desc_optional('', '{}={}'.format(Arg['name'], getReadableValue(Arg['default'])))

  else:
    return (desc_parameter if not 'default' in Arg else desc_optional)('', Arg['name'])

def getArgsContent(Args):
  Container = desc('', desc_signature(text='Args'), objtype="Args")

  for name, Arg in Args.items():
    Content = desc_content()
    Content.append(desc_name(text='%s: ' % name))
    Content.append(compact_paragraph(text=getArgDesc(Arg)))
    Container.append(Content)

  return Container

def getArgList(Args):
  return desc_parameterlist('', '', *[getArgLabel(Arg) for Arg in Args.values()])

def getMemberContent(Member, *Children):
  Config = Member.Config
  Content = desc_content(*Children)

  doc = Member.Underlying.__doc__
  if doc:
    Content.insert(0, getNodeTreeFromStr(doc)) # add the parsed docstring to the content.

  if 'desc' in Config:
    Content.insert(0, paragraph(text=Config['desc']))

  return Content

def getMemberTitle(Config):
  return '%s%s' % (Config['name'], ', %s' % Config['alias'] if 'alias' in Config else '')

def getSignature(Config):
  return desc_signature(text=getMemberTitle(Config))

def getTaskTree(Task, id):
  Config = Task.Config

  Elms = [nodes.target('', '', ids=[id])]

  content = getMemberContent(Task)
  signature = getSignature(Config)
  signature.append(getArgList(Task.Args))

  if Task.Args:
    content.append(getArgsContent(Task.Args))

  Elms.append(desc(id, signature, content, id=id, objtype='Task'))

  return Elms

def getChildren(Parent, prefix):
  Children = []

  for name, Child in Parent.Members.iteritems():
    if Child.Config.get('alias') == name: # don't process aliases
      continue

    id = '%s.%s' % (prefix, name)

    if hasattr(Child, 'Members'):
      Children += desc_content(prefix, *getGroupTree(Child, id))

    else:
      Children += desc_content(prefix, *getTaskTree(Child, id))

  return Children

def getGroupTree(Group, prefix):
  return [
    nodes.target('', '', ids=[prefix]),
    desc(prefix,
      getSignature(Group.Config),
      getMemberContent(Group, *getChildren(Group, prefix)),
      id=prefix, objtype='Group'
    )
  ]

def getModuleTree(Module, prefix, title):
  Elms = [nodes.target('', '', ids=[prefix])]

  Section = nodes.section()
  Section  += nodes.title(text=title)
  Section += getMemberContent(Module, *getChildren(Module, prefix))

  return Elms + [Section]

# Main
from ec import interface #Note: Importing this makes any imported ec scripts to be configured, automatically.

def setup(app):
  app.add_directive('ec_module', EcModuleDirective)

  return {'version': __version__}

class EcModuleDirective(Directive):

  has_content = True # this alllows for passing content with the directive

  def run(self):
    env = self.state.document.settings.env
    module_path = self.content[0]
    os.chdir(startingCWD) #Note: Allow for relative imports.
    module = load_source(getRandomChars(16), module_path) #ToDo: Ensure that the random string is a available-module-name.
    setBase(module) #Fix: This is a hot-fix for force-configuring the loaded scripts, as ec hooks only into module imports.
    moduleID = "ec-%d-%s" % (env.new_serialno('ec'), module.__ec_member__.Config['name'])

    return getModuleTree(module.__ec_member__, moduleID, basename(module_path)) #ToDo: Pass optional titles through the directives.
