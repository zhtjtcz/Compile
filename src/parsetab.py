
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ALBrace LPar NUMBER RBrace RPar Semicolon\tA : A RBrace\n\t  \t  | LBrace\n\t'
    
_lr_action_items = {'LBrace':([0,],[2,]),'$end':([1,2,3,],[0,-2,-1,]),'RBrace':([1,2,3,],[3,-2,-1,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'A':([0,],[1,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> A","S'",1,None,None,None),
  ('A -> A RBrace','A',2,'p_A','yacctest.py',5),
  ('A -> LBrace','A',1,'p_A','yacctest.py',6),
]
