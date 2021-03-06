#!/usr/bin/env python
#-----------------------------------------------------------------------------
# Title      : PyRogue AXI Version Module
#-----------------------------------------------------------------------------
# File       : 
# Author     : Maciej Kwiatkowski
# Created    : 2016-09-29
# Last update: 2017-01-31
#-----------------------------------------------------------------------------
# Description:
#-----------------------------------------------------------------------------
# This file is part of the rogue software platform. It is subject to 
# the license terms in the LICENSE.txt file found in the top-level directory 
# of this distribution and at: 
#    https://confluence.slac.stanford.edu/display/ppareg/LICENSE.html. 
# No part of the rogue software platform, including this file, may be 
# copied, modified, propagated, or distributed except according to the terms 
# contained in the LICENSE.txt file.
#-----------------------------------------------------------------------------
import pyrogue as pr
import collections

class LztsPowerRegisters(pr.Device):
   def __init__(self, **kwargs):
      """Create the configuration device for Power Controller"""
      super().__init__(description='Power Configuration Registers', **kwargs)
      
      # Creation. memBase is either the register bus server (srp, rce mapped memory, etc) or the device which
      # contains this object. In most cases the parent and memBase are the same but they can be 
      # different in more complex bus structures. They will also be different for the top most node.
      # The setMemBase call can be used to update the memBase for this Device. All sub-devices and local
      # blocks will be updated.
      
      #############################################
      # Create block / variable combinations
      #############################################
      
      
      #Setup registers & variables
      self.add((pr.RemoteVariable(name='SysRst',     description='SysRst',     offset=0x00000008, bitSize=1, bitOffset=0,  base=pr.Bool, mode='RW')))
      
      self.add((
         pr.RemoteVariable(name='EnDcDcAm6V',   description='PowerEnAll', offset=0x00000000, bitSize=1, bitOffset=0,  base=pr.Bool, mode='RW'),
         pr.RemoteVariable(name='EnDcDcAp5V4',  description='PowerEnAll', offset=0x00000000, bitSize=1, bitOffset=1,  base=pr.Bool, mode='RW'),
         pr.RemoteVariable(name='EnDcDcAp3V7',  description='PowerEnAll', offset=0x00000000, bitSize=1, bitOffset=2,  base=pr.Bool, mode='RW'),
         pr.RemoteVariable(name='EnDcDcAp2V3',  description='PowerEnAll', offset=0x00000000, bitSize=1, bitOffset=3,  base=pr.Bool, mode='RW'),
         pr.RemoteVariable(name='EnDcDcAp1V6',  description='PowerEnAll', offset=0x00000000, bitSize=1, bitOffset=4,  base=pr.Bool, mode='RW'),
         pr.RemoteVariable(name='EnLdoSlow',    description='PowerEnAll', offset=0x00000000, bitSize=1, bitOffset=5,  base=pr.Bool, mode='RW'),
         pr.RemoteVariable(name='EnLdoFast',    description='PowerEnAll', offset=0x00000000, bitSize=1, bitOffset=6,  base=pr.Bool, mode='RW'),
         pr.RemoteVariable(name='EnLdoAm5V',    description='PowerEnAll', offset=0x00000000, bitSize=1, bitOffset=7,  base=pr.Bool, mode='RW')))
      
      self.add(pr.RemoteVariable(
         name       = 'TempAlert',     
         description= 'External Temperature Alerts from I2C devices',     
         offset     = 0x00000010, 
         bitSize    = 2, 
         bitOffset  = 0,  
         base       = pr.UInt, 
         mode       = 'RO',
      ))
      
      self.add(pr.RemoteVariable(
         name       = 'TempFault',     
         description= 'Temperature Fault State',     
         offset     = 0x00000014, 
         bitSize    = 2, 
         bitOffset  = 0,  
         base       = pr.UInt, 
         mode       = 'RO',
      ))   

      self.add(pr.RemoteVariable(
         name       = 'IgnTempAlert',     
         description= 'Mask for ignoring the External Temperature Alerts',     
         offset     = 0x00000018, 
         bitSize    = 2, 
         bitOffset  = 0,  
         base       = pr.UInt, 
         mode       = 'RW',
      ))  

      self.add(pr.RemoteVariable(
         name       = 'LatchTempFault',     
         description= 'Flag to latch the TempFault event',     
         offset     = 0x0000001C, 
         bitSize    = 1, 
         bitOffset  = 0,  
         base       = pr.Bool, 
         mode       = 'RW',
      ))
      
      self.add(pr.RemoteVariable(
         name       = 'FaultTempLoc',     
         description= 'Local Temperature at Fault Event',     
         offset     = 0x00000020, 
         bitSize    = 8, 
         bitOffset  = 0,  
         base       = pr.UInt, 
         mode       = 'RO',
      ))
      
      self.add(pr.RemoteVariable(
         name       = 'FaultTempRem',     
         description= 'Remote Temperature at Fault Event',     
         offset     = 0x00000024, 
         bitSize    = 8, 
         bitOffset  = 0,  
         base       = pr.UInt, 
         mode       = 'RO',
      ))
      
      self.add(pr.RemoteVariable(
         name       = 'FaultTempPtr',     
         description= 'Fault Buffer Pointer',
         offset     = 0x00000028, 
         bitSize    = 8, 
         bitOffset  = 0,  
         base       = pr.UInt, 
         mode       = 'RO',
      ))
      
      self.add((
         pr.RemoteVariable(name='PokDcDcDp6V',     description='PowerOkAll', offset=0x00000004, bitSize=1, bitOffset=0,  base=pr.Bool, mode='RO'),
         pr.RemoteVariable(name='PokDcDcAp6V',     description='PowerOkAll', offset=0x00000004, bitSize=1, bitOffset=1,  base=pr.Bool, mode='RO'),
         pr.RemoteVariable(name='PokDcDcAm6V',     description='PowerOkAll', offset=0x00000004, bitSize=1, bitOffset=2,  base=pr.Bool, mode='RO'),
         pr.RemoteVariable(name='PokDcDcAp5V4',    description='PowerOkAll', offset=0x00000004, bitSize=1, bitOffset=3,  base=pr.Bool, mode='RO'),
         pr.RemoteVariable(name='PokDcDcAp3V7',    description='PowerOkAll', offset=0x00000004, bitSize=1, bitOffset=4,  base=pr.Bool, mode='RO'),
         pr.RemoteVariable(name='PokDcDcAp2V3',    description='PowerOkAll', offset=0x00000004, bitSize=1, bitOffset=5,  base=pr.Bool, mode='RO'),
         pr.RemoteVariable(name='PokDcDcAp1V6',    description='PowerOkAll', offset=0x00000004, bitSize=1, bitOffset=6,  base=pr.Bool, mode='RO'),
         pr.RemoteVariable(name='PokLdoA0p1V8',    description='PowerOkAll', offset=0x00000004, bitSize=1, bitOffset=7,  base=pr.Bool, mode='RO'),
         pr.RemoteVariable(name='PokLdoA0p3V3',    description='PowerOkAll', offset=0x00000004, bitSize=1, bitOffset=8,  base=pr.Bool, mode='RO'),
         pr.RemoteVariable(name='PokLdoAd1p1V2',   description='PowerOkAll', offset=0x00000004, bitSize=1, bitOffset=9,  base=pr.Bool, mode='RO'),
         pr.RemoteVariable(name='PokLdoAd2p1V2',   description='PowerOkAll', offset=0x00000004, bitSize=1, bitOffset=10, base=pr.Bool, mode='RO'),
         pr.RemoteVariable(name='PokLdoA1p1V9',    description='PowerOkAll', offset=0x00000004, bitSize=1, bitOffset=11, base=pr.Bool, mode='RO'),
         pr.RemoteVariable(name='PokLdoA2p1V9',    description='PowerOkAll', offset=0x00000004, bitSize=1, bitOffset=12, base=pr.Bool, mode='RO'),
         pr.RemoteVariable(name='PokLdoAd1p1V9',   description='PowerOkAll', offset=0x00000004, bitSize=1, bitOffset=13, base=pr.Bool, mode='RO'),
         pr.RemoteVariable(name='PokLdoAd2p1V9',   description='PowerOkAll', offset=0x00000004, bitSize=1, bitOffset=14, base=pr.Bool, mode='RO'),
         pr.RemoteVariable(name='PokLdoA1p3V3',    description='PowerOkAll', offset=0x00000004, bitSize=1, bitOffset=15, base=pr.Bool, mode='RO'),
         pr.RemoteVariable(name='PokLdoA2p3V3',    description='PowerOkAll', offset=0x00000004, bitSize=1, bitOffset=16, base=pr.Bool, mode='RO'),
         pr.RemoteVariable(name='PokLdoAvclkp3V3', description='PowerOkAll', offset=0x00000004, bitSize=1, bitOffset=17, base=pr.Bool, mode='RO'),
         pr.RemoteVariable(name='PokLdoA0p5V0',    description='PowerOkAll', offset=0x00000004, bitSize=1, bitOffset=18, base=pr.Bool, mode='RO'),
         pr.RemoteVariable(name='PokLdoA1p5V0',    description='PowerOkAll', offset=0x00000004, bitSize=1, bitOffset=19, base=pr.Bool, mode='RO')))
      
      self.add((pr.RemoteVariable(name='SADCRst',     description='SADCRst',     offset=0x00000200, bitSize=4, bitOffset=0,  base=pr.UInt, mode='RW')))
      self.add((pr.RemoteVariable(name='SADCCtrl1',   description='SADCCtrl1',   offset=0x00000204, bitSize=4, bitOffset=0,  base=pr.UInt, mode='RW')))
      self.add((pr.RemoteVariable(name='SADCCtrl2',   description='SADCCtrl2',   offset=0x00000208, bitSize=4, bitOffset=0,  base=pr.UInt, mode='RW')))
      self.add((pr.RemoteVariable(name='SAMPEn',      description='SAMPEn',      offset=0x0000020C, bitSize=4, bitOffset=0,  base=pr.UInt, mode='RW')))
      
      #self.add((pr.RemoteVariable(name='DDRRstN',     description='DDRRstN',     offset=0x00000280, bitSize=1, bitOffset=0,  base=pr.Bool, mode='RW')))
      
      self.add((pr.RemoteVariable(name='FADCPdn',     description='FADCPdn',     offset=0x00000300, bitSize=4, bitOffset=0,  base=pr.UInt, mode='RW')))
      
      self.add((pr.RemoteVariable(name='DcDcSyncAll',       description='DcDcSyncAll',       offset=0x00000400, bitSize=1,  bitOffset=0,  base=pr.Bool, mode='RW')))
      
      self.add((pr.RemoteVariable(name='DcDcHalfClkAp6V',   description='DcDcHalfClkAp6V',   offset=0x00000500, bitSize=32, bitOffset=0,  base=pr.UInt, mode='RW')))
      self.add((pr.RemoteVariable(name='DcDcHalfClkAm6V',   description='DcDcHalfClkAm6V',   offset=0x00000504, bitSize=32, bitOffset=0,  base=pr.UInt, mode='RW')))
      self.add((pr.RemoteVariable(name='DcDcHalfClkAp5V4',  description='DcDcHalfClkAp5V4',  offset=0x00000508, bitSize=32, bitOffset=0,  base=pr.UInt, mode='RW')))
      self.add((pr.RemoteVariable(name='DcDcHalfClkAp3V7',  description='DcDcHalfClkAp3V7',  offset=0x0000050C, bitSize=32, bitOffset=0,  base=pr.UInt, mode='RW')))
      self.add((pr.RemoteVariable(name='DcDcHalfClkAp2V3',  description='DcDcHalfClkAp2V3',  offset=0x00000510, bitSize=32, bitOffset=0,  base=pr.UInt, mode='RW')))
      self.add((pr.RemoteVariable(name='DcDcHalfClkAp1V6',  description='DcDcHalfClkAp1V6',  offset=0x00000514, bitSize=32, bitOffset=0,  base=pr.UInt, mode='RW')))
      self.add((pr.RemoteVariable(name='DcDcHalfClkDp6V',   description='DcDcHalfClkDp6V',   offset=0x00000518, bitSize=32, bitOffset=0,  base=pr.UInt, mode='RW')))
      self.add((pr.RemoteVariable(name='DcDcHalfClkDp3V3',  description='DcDcHalfClkDp3V3',  offset=0x0000051C, bitSize=32, bitOffset=0,  base=pr.UInt, mode='RW')))
      self.add((pr.RemoteVariable(name='DcDcHalfClkDp1V8',  description='DcDcHalfClkDp1V8',  offset=0x00000520, bitSize=32, bitOffset=0,  base=pr.UInt, mode='RW')))
      self.add((pr.RemoteVariable(name='DcDcHalfClkDp1V2',  description='DcDcHalfClkDp1V2',  offset=0x00000524, bitSize=32, bitOffset=0,  base=pr.UInt, mode='RW')))
      self.add((pr.RemoteVariable(name='DcDcHalfClkDp0V95', description='DcDcHalfClkDp0V95', offset=0x00000528, bitSize=32, bitOffset=0,  base=pr.UInt, mode='RW')))
      self.add((pr.RemoteVariable(name='DcDcHalfClkMgt1V0', description='DcDcHalfClkMgt1V0', offset=0x0000052C, bitSize=32, bitOffset=0,  base=pr.UInt, mode='RW')))
      self.add((pr.RemoteVariable(name='DcDcHalfClkMgt1V2', description='DcDcHalfClkMgt1V2', offset=0x00000530, bitSize=32, bitOffset=0,  base=pr.UInt, mode='RW')))
      self.add((pr.RemoteVariable(name='DcDcHalfClkMgt1V8', description='DcDcHalfClkMgt1V8', offset=0x00000534, bitSize=32, bitOffset=0,  base=pr.UInt, mode='RW')))
      
      self.add((pr.RemoteVariable(name='DcDcPhaseAp6V',     description='DcDcPhaseAp6V',     offset=0x00000600, bitSize=32, bitOffset=0,  base=pr.UInt, mode='RW')))
      self.add((pr.RemoteVariable(name='DcDcPhaseAm6V',     description='DcDcPhaseAm6V',     offset=0x00000604, bitSize=32, bitOffset=0,  base=pr.UInt, mode='RW')))
      self.add((pr.RemoteVariable(name='DcDcPhaseAp5V4',    description='DcDcPhaseAp5V4',    offset=0x00000608, bitSize=32, bitOffset=0,  base=pr.UInt, mode='RW')))
      self.add((pr.RemoteVariable(name='DcDcPhaseAp3V7',    description='DcDcPhaseAp3V7',    offset=0x0000060C, bitSize=32, bitOffset=0,  base=pr.UInt, mode='RW')))
      self.add((pr.RemoteVariable(name='DcDcPhaseAp2V3',    description='DcDcPhaseAp2V3',    offset=0x00000610, bitSize=32, bitOffset=0,  base=pr.UInt, mode='RW')))
      self.add((pr.RemoteVariable(name='DcDcPhaseAp1V6',    description='DcDcPhaseAp1V6',    offset=0x00000614, bitSize=32, bitOffset=0,  base=pr.UInt, mode='RW')))
      self.add((pr.RemoteVariable(name='DcDcPhaseDp6V',     description='DcDcPhaseDp6V',     offset=0x00000618, bitSize=32, bitOffset=0,  base=pr.UInt, mode='RW')))
      self.add((pr.RemoteVariable(name='DcDcPhaseDp3V3',    description='DcDcPhaseDp3V3',    offset=0x0000061C, bitSize=32, bitOffset=0,  base=pr.UInt, mode='RW')))
      self.add((pr.RemoteVariable(name='DcDcPhaseDp1V8',    description='DcDcPhaseDp1V8',    offset=0x00000620, bitSize=32, bitOffset=0,  base=pr.UInt, mode='RW')))
      self.add((pr.RemoteVariable(name='DcDcPhaseDp1V2',    description='DcDcPhaseDp1V2',    offset=0x00000624, bitSize=32, bitOffset=0,  base=pr.UInt, mode='RW')))
      self.add((pr.RemoteVariable(name='DcDcPhaseDp0V95',   description='DcDcPhaseDp0V95',   offset=0x00000628, bitSize=32, bitOffset=0,  base=pr.UInt, mode='RW')))
      self.add((pr.RemoteVariable(name='DcDcPhaseMgt1V0',   description='DcDcPhaseMgt1V0',   offset=0x0000062C, bitSize=32, bitOffset=0,  base=pr.UInt, mode='RW')))
      self.add((pr.RemoteVariable(name='DcDcPhaseMgt1V2',   description='DcDcPhaseMgt1V2',   offset=0x00000630, bitSize=32, bitOffset=0,  base=pr.UInt, mode='RW')))
      self.add((pr.RemoteVariable(name='DcDcPhaseMgt1V8',   description='DcDcPhaseMgt1V8',   offset=0x00000634, bitSize=32, bitOffset=0,  base=pr.UInt, mode='RW')))
      
      #####################################
      # Create commands
      #####################################
      
      # A command has an associated function. The function can be a series of
      # python commands in a string. Function calls are executed in the command scope
      # the passed arg is available as 'arg'. Use 'dev' to get to device scope.
      # A command can also be a call to a local function with local scope.
      # The command object and the arg are passed
   
   @staticmethod   
   def frequencyConverter(self):
      def func(dev, var):         
         return '{:.3f} kHz'.format(1/(self.clkPeriod * self._count(var.dependencies)) * 1e-3)
      return func
