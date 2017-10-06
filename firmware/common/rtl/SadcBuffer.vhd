-------------------------------------------------------------------------------
-- File       : SadcBuffer.vhd
-- Company    : SLAC National Accelerator Laboratory
-- Created    : 2017-10-04
-- Last update: 2017-10-05
-------------------------------------------------------------------------------
-- Description: 
-------------------------------------------------------------------------------
-- This file is part of 'LZ Test Stand Firmware'.
-- It is subject to the license terms in the LICENSE.txt file found in the 
-- top-level directory of this distribution and at: 
--    https://confluence.slac.stanford.edu/display/ppareg/LICENSE.html. 
-- No part of 'LZ Test Stand Firmware', including this file, 
-- may be copied, modified, propagated, or distributed except according to 
-- the terms contained in the LICENSE.txt file.
-------------------------------------------------------------------------------

library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;

use work.StdRtlPkg.all;
use work.AxiPkg.all;
use work.AxiLitePkg.all;
use work.AxiStreamPkg.all;

entity SadcBuffer is
   generic (
      TPD_G            : time                   := 1 ns;
      ADDR_BITS_G      : integer range 12 to 31 := 14;
      AXI_ERROR_RESP_G : slv(1 downto 0)        := AXI_RESP_DECERR_C;
      AXI_BASE_ADDR_G  : slv(31 downto 0)       := (others => '0'));
   port (
      -- ADC interface
      adcClk          : in  sl;
      adcRst          : in  sl;
      adcData         : in  Slv16Array(7 downto 0);
      gTime           : in  slv(63 downto 0);
      extTrigger      : in  sl;
      -- AXI Interface (adcClk domain)
      axiWriteMaster  : out AxiWriteMasterArray(7 downto 0);
      axiWriteSlave   : in  AxiWriteSlaveArray(7 downto 0);
      axiReadMaster   : out AxiReadMasterType;
      axiReadSlave    : in  AxiReadSlaveType;
      -- AxiStream output (axisClk domain)
      axisClk         : in  sl;
      axisRst         : in  sl;
      axisMaster      : out AxiStreamMasterType;
      axisSlave       : in  AxiStreamSlaveType;
      -- AXI-Lite Interface (axilClk domain)
      axilClk         : in  sl;
      axilRst         : in  sl;
      axilReadMaster  : in  AxiLiteReadMasterType;
      axilReadSlave   : out AxiLiteReadSlaveType;
      axilWriteMaster : in  AxiLiteWriteMasterType;
      axilWriteSlave  : out AxiLiteWriteSlaveType);
end SadcBuffer;

architecture mapping of SadcBuffer is

   constant NUM_AXI_MASTERS_C : natural := 10;

   constant AXI_CONFIG_C : AxiLiteCrossbarMasterConfigArray(NUM_AXI_MASTERS_C-1 downto 0) := genAxiLiteConfig(NUM_AXI_MASTERS_C, AXI_BASE_ADDR_G, 20, 16);

   signal axilWriteMasters : AxiLiteWriteMasterArray(NUM_AXI_MASTERS_C-1 downto 0);
   signal axilWriteSlaves  : AxiLiteWriteSlaveArray(NUM_AXI_MASTERS_C-1 downto 0);
   signal axilReadMasters  : AxiLiteReadMasterArray(NUM_AXI_MASTERS_C-1 downto 0);
   signal axilReadSlaves   : AxiLiteReadSlaveArray(NUM_AXI_MASTERS_C-1 downto 0);

   signal hdrDout  : Slv32Array(7 downto 0);
   signal hdrValid : slv(7 downto 0);
   signal hdrRd    : slv(7 downto 0);

   signal memWrAddr : Slv32Array(7 downto 0);
   signal memFull   : slv(7 downto 0);

   signal adcDataTester : Slv32Array(7 downto 0);

begin

   ---------------------
   -- AXI-Lite Crossbar
   ---------------------
   U_XBAR : entity work.AxiLiteCrossbar
      generic map (
         TPD_G              => TPD_G,
         DEC_ERROR_RESP_G   => AXI_ERROR_RESP_G,
         NUM_SLAVE_SLOTS_G  => 1,
         NUM_MASTER_SLOTS_G => NUM_AXI_MASTERS_C,
         MASTERS_CONFIG_G   => AXI_CONFIG_C)
      port map (
         axiClk              => axilClk,
         axiClkRst           => axilRst,
         sAxiWriteMasters(0) => axilWriteMaster,
         sAxiWriteSlaves(0)  => axilWriteSlave,
         sAxiReadMasters(0)  => axilReadMaster,
         sAxiReadSlaves(0)   => axilReadSlave,
         mAxiWriteMasters    => axilWriteMasters,
         mAxiWriteSlaves     => axilWriteSlaves,
         mAxiReadMasters     => axilReadMasters,
         mAxiReadSlaves      => axilReadSlaves);

   -------------------------------
   -- 250 MSPS ADCs Buffer Writers
   -------------------------------
   GEN_VEC : for i in 7 downto 0 generate

      U_Writer : entity work.SadcBufferWriter
         generic map (
            TPD_G         => TPD_G,
            ADDR_BITS_G   => ADDR_BITS_G,
            ADDR_OFFSET_G => toSlv(i*2**ADDR_BITS_G, 32))
         port map (
            -- ADC interface
            adcClk          => adcClk,
            adcRst          => adcRst,
            adcData         => adcData(i),
            gTime           => gTime,
            extTrigger      => extTrigger,
            -- AXI-Lite Interface for local registers 
            axilClk         => axilClk,
            axilRst         => axilRst,
            axilReadMaster  => axilReadMasters(i),
            axilReadSlave   => axilReadSlaves(i),
            axilWriteMaster => axilWriteMasters(i),
            axilWriteSlave  => axilWriteSlaves(i),
            -- AXI Interface (adcClk)
            axiWriteMaster  => axiWriteMaster(i),
            axiWriteSlave   => axiWriteSlave(i),
            -- Trigger information to data reader (adcClk)
            hdrDout         => hdrDout(i),
            hdrValid        => hdrValid(i),
            hdrRd           => hdrRd(i),
            -- Buffer handshake to/from data reader (adcClk)
            memWrAddr       => memWrAddr(i),
            memFull         => memFull(i));

      adcDataTester(i)(31 downto 16) <= (others => '0');
      adcDataTester(i)(15 downto 0)  <= adcData(i);

   end generate GEN_VEC;

   ------------------------------
   -- 250 MSPS ADCs Buffer Reader
   ------------------------------
   U_Reader : entity work.SadcBufferReader
      generic map (
         TPD_G       => TPD_G,
         ADDR_BITS_G => ADDR_BITS_G)
      port map (
         -- ADC Clock Domain
         adcClk          => adcClk,
         adcRst          => adcRst,
         -- AXI-Lite Interface for local registers 
         axilClk         => axilClk,
         axilRst         => axilRst,
         axilReadMaster  => axilReadMasters(8),
         axilReadSlave   => axilReadSlaves(8),
         axilWriteMaster => axilWriteMasters(8),
         axilWriteSlave  => axilWriteSlaves(8),
         -- AXI Interface (adcClk)
         axiReadMaster   => axiReadMaster,
         axiReadSlave    => axiReadSlave,
         -- Trigger information from data writers (adcClk domain)
         hdrDout         => hdrDout,
         hdrValid        => hdrValid,
         hdrRd           => hdrRd,
         -- Buffer handshake to/from data writers (adcClk domain)
         memWrAddr       => memWrAddr,
         memFull         => memFull,
         -- AxiStream output (axisClk domain)
         axisClk         => axisClk,
         axisRst         => axisRst,
         axisMaster      => axisMaster,
         axisSlave       => axisSlave);

   -------------------------------
   -- 250 MSPS ADCs pattern tester
   -------------------------------
   U_Tester : entity work.AdcPatternTester
      generic map (
         TPD_G          => TPD_G,
         ADC_BITS_G     => 16,
         NUM_CHANNELS_G => 8)
      port map (
         -- ADC Interface
         adcClk          => adcClk,
         adcRst          => adcRst,
         adcData         => adcDataTester,
         -- Axi Interface
         axilClk         => axilClk,
         axilRst         => axilRst,
         axilWriteMaster => axilWriteMasters(9),
         axilWriteSlave  => axilWriteSlaves(9),
         axilReadMaster  => axilReadMasters(9),
         axilReadSlave   => axilReadSlaves(9),
         -- Direct status bits
         testDone        => open,
         testFailed      => open);

end mapping;
